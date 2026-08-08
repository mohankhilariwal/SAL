from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
from typing import Iterable
from uuid import uuid4

from .budgets import BudgetExceeded, BudgetManager, CostTariff
from .cancellation import CancellationToken, RunCancelled
from .decision import DecisionProvider, DecisionProviderError, action_signature
from .models import (
    AgentGoal,
    AgentObservation,
    AgentRunOutcome,
    AgentRunState,
    RecoveryRecord,
    REQUIRED_MILESTONES,
    RuntimeBudget,
)
from .recovery import RecoveryManager
from .termination import TerminationEvaluator
from northstar_compliance.state.checkpoint import LocalCheckpointStore
from northstar_compliance.tools.gateway import Principal, ToolGateway, ToolInvocationRequest, ToolResult

class AgentRuntime:
    AGENT_ID = "AGT-001"
    ALLOWED_TOOLS = {f"TOOL-{i:03d}" for i in range(1, 7)}

    def __init__(
        self,
        gateway: ToolGateway,
        providers: Iterable[DecisionProvider],
        checkpoint_store: LocalCheckpointStore,
        *,
        reconciler,
        clock=None,
        tariff: CostTariff = CostTariff(),
        no_progress_window: int = 2,
        repeated_action_limit: int = 2,
    ) -> None:
        self.gateway = gateway
        self.providers = list(providers)
        if not self.providers:
            raise ValueError("at least one decision provider required")
        self.checkpoint_store = checkpoint_store
        self.reconciler = reconciler
        self.clock = clock
        self.tariff = tariff
        self.no_progress_window = no_progress_window
        self.repeated_action_limit = repeated_action_limit
        self.termination = TerminationEvaluator()

    def create_state(self, goal: AgentGoal, budget: RuntimeBudget | None = None, run_id: str | None = None) -> AgentRunState:
        return AgentRunState(
            schema_version="1.1.0",
            run_id=run_id or f"RUN-{uuid4().hex[:12].upper()}",
            agent_id=self.AGENT_ID,
            goal=goal,
            budget=budget or RuntimeBudget(),
        )

    def run(
        self,
        goal: AgentGoal,
        principal: Principal,
        *,
        budget: RuntimeBudget | None = None,
        cancellation: CancellationToken | None = None,
        resume_run_id: str | None = None,
        max_new_iterations: int | None = None,
    ) -> AgentRunOutcome:
        token = cancellation or CancellationToken()
        state = self.checkpoint_store.load(resume_run_id) if resume_run_id else self.create_state(goal, budget)
        if resume_run_id and state.status != "running":
            return self._outcome(state)
        bm = BudgetManager(state, tariff=self.tariff, **({"clock": self.clock} if self.clock else {}))
        recovery = RecoveryManager(self.gateway, bm, state, reconciler=self.reconciler)
        recovery_context: dict = {"replan_number": state.ledger.replans}
        start_iterations = state.ledger.iterations

        while state.status == "running":
            try:
                token.raise_if_cancelled()
                bm.before_iteration()
                if max_new_iterations is not None and state.ledger.iterations - start_iterations >= max_new_iterations:
                    self._checkpoint(state)
                    return self._outcome(state, interim=True)

                envelope = self._decide_with_fallback(goal, state, recovery_context, bm)
                decision = envelope.decision
                decision.validate()
                state.decisions.append(asdict(decision) | {
                    "provider_attempts": envelope.provider_attempts,
                    "provider_fallback_used": envelope.fallback_used,
                })
                self._checkpoint(state)

                if decision.kind == "escalate":
                    self._terminate(state, "escalated", "human_escalation")
                    break
                if decision.kind == "complete":
                    if self.termination.completion_valid(state):
                        self._terminate(state, "completed", "goal_complete")
                    else:
                        self._terminate(state, "escalated", "invalid_completion")
                    break
                if decision.tool_id not in self.ALLOWED_TOOLS:
                    self._terminate(state, "escalated", "invalid_decision")
                    break

                signature = action_signature(decision)
                if signature == state.last_action_signature:
                    state.repeated_action_count += 1
                else:
                    state.repeated_action_count = 1
                    state.last_action_signature = signature

                if signature in state.blocked_action_signatures or state.repeated_action_count > self.repeated_action_limit:
                    if self._request_replan(state, signature, "repeated_action", bm, recovery_context):
                        continue
                    self._terminate(state, "terminated_guard", "repeated_action")
                    break

                request = ToolInvocationRequest(
                    tool_id=decision.tool_id,
                    tool_version=decision.tool_version or "1.0.0",
                    arguments=decision.arguments,
                    principal=principal,
                    idempotency_key=self._idempotency_key(state, decision.tool_id, decision.arguments)
                    if self.gateway.impact(decision.tool_id) == "reversible_write" else None,
                )
                result = recovery.execute(request, token)
                previous_milestones = len(state.milestones)
                observation = self._project_observation(state, result, decision.tool_id)
                state.observations.append(asdict(observation))
                self._checkpoint(state)

                if result.status != "success":
                    reason = "ambiguous_write_unresolved" if result.failure and result.failure.kind == "ambiguous_write" else "tool_failure"
                    self._terminate(state, "escalated", reason)
                    break

                if len(state.milestones) == previous_milestones:
                    state.consecutive_no_progress += 1
                else:
                    state.consecutive_no_progress = 0

                if state.consecutive_no_progress >= self.no_progress_window:
                    if self._request_replan(state, signature, "no_progress", bm, recovery_context):
                        state.consecutive_no_progress = 0
                        continue
                    self._terminate(state, "terminated_guard", "no_progress")
                    break

                bm.check_wall_time()

            except RunCancelled as exc:
                self._terminate(state, "cancelled", str(exc))
                break
            except BudgetExceeded as exc:
                self._terminate(state, "terminated_guard", exc.reason)
                break
            except (ValueError, PermissionError) as exc:
                state.recovery_records.append(asdict(RecoveryRecord("reject_invalid_action", str(exc), 1, outcome="blocked")))
                self._terminate(state, "escalated", "invalid_decision")
                break

        bm.refresh_elapsed()
        self._checkpoint(state)
        return self._outcome(state)

    def _decide_with_fallback(self, goal, state, recovery_context, bm):
        attempts = 0
        last_error: Exception | None = None
        for index, provider in enumerate(self.providers):
            attempts += 1
            try:
                envelope = provider.decide(goal, state, recovery_context)
                bm.settle_model_usage(envelope.usage)
                return type(envelope)(
                    decision=envelope.decision,
                    usage=envelope.usage,
                    provider_attempts=attempts,
                    fallback_used=index > 0,
                )
            except DecisionProviderError as exc:
                last_error = exc
                bm.record_failure()
                # Failed model attempts still consume one model-call slot, but no token usage is fabricated.
                state.ledger.model_calls += 1
                state.recovery_records.append(asdict(RecoveryRecord(
                    action="model_fallback" if index + 1 < len(self.providers) else "model_failure",
                    reason=str(exc),
                    attempt=attempts,
                    outcome="selected" if index + 1 < len(self.providers) and exc.retryable else "unavailable",
                )))
                if not exc.retryable:
                    break
                if index + 1 < len(self.providers):
                    bm.record_retry()
                    continue
                break
        raise ValueError(f"decision_provider_failure: {last_error}")

    def _request_replan(self, state, signature, reason, bm, recovery_context) -> bool:
        try:
            bm.record_replan()
        except BudgetExceeded:
            return False
        if signature not in state.blocked_action_signatures:
            state.blocked_action_signatures.append(signature)
        state.recovery_records.append(asdict(RecoveryRecord(
            action="bounded_replan",
            reason=reason,
            attempt=state.ledger.replans,
            outcome="requested",
        )))
        recovery_context["replan_number"] = state.ledger.replans
        self._checkpoint(state)
        return True

    def _project_observation(self, state: AgentRunState, result: ToolResult, tool_id: str) -> AgentObservation:
        if result.status != "success":
            return AgentObservation(tool_id, "error", {}, fallback_used=result.adapter == "fallback")
        payload = dict(result.payload)
        reconciled = bool(payload.pop("_reconciled", False))
        milestone = None
        if tool_id == "TOOL-001" and payload.get("records"):
            milestone = "regulatory_sources_found"
            state.artifacts["regulatory_sources"] = payload["records"]
        elif tool_id == "TOOL-003" and payload.get("citations"):
            milestone = "authorized_evidence_retrieved"
            state.artifacts["evidence"] = payload["citations"]
        elif tool_id == "TOOL-002" and payload.get("controls"):
            milestone = "control_candidates_found"
            state.artifacts["controls"] = payload["controls"]
        elif tool_id == "TOOL-004" and payload.get("status") == "draft_unapproved":
            milestone = "draft_case_created"
            state.artifacts["draft_case"] = payload
        elif tool_id == "TOOL-005" and payload.get("status") == "candidate_unapproved":
            milestone = "candidate_mapping_saved"
            state.artifacts["candidate_mapping"] = payload
        elif tool_id == "TOOL-006" and payload.get("status") == "queued_for_human_review":
            milestone = "human_review_queued"
            state.artifacts["review_request"] = payload
        if milestone and milestone not in state.milestones:
            state.milestones.append(milestone)
        return AgentObservation(
            tool_id=tool_id,
            status="success",
            payload=payload,
            milestone_added=milestone,
            reconciled=reconciled,
            fallback_used=result.adapter == "fallback",
        )

    def _idempotency_key(self, state, tool_id, arguments) -> str:
        canonical = f"{state.run_id}|{tool_id}|{sorted(arguments.items())}"
        return sha256(canonical.encode("utf-8")).hexdigest()

    def _terminate(self, state, status, reason):
        state.status = status
        state.termination_reason = reason
        self._checkpoint(state)

    def _checkpoint(self, state):
        self.checkpoint_store.save(state)

    def _outcome(self, state, interim: bool = False):
        missing = tuple(m for m in REQUIRED_MILESTONES if m not in state.milestones)
        reason = state.termination_reason or ("checkpointed_running" if interim or state.status == "running" else "unknown")
        return AgentRunOutcome(
            run_id=state.run_id,
            status=state.status,
            termination_reason=reason,
            completed_milestones=tuple(state.milestones),
            missing_milestones=missing,
            artifacts=dict(state.artifacts),
            budget_ledger=asdict(state.ledger),
            recovery_records=tuple(state.recovery_records),
        )
