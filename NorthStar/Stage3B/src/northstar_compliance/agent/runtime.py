from __future__ import annotations

import hashlib
import json
import uuid
from pathlib import Path
from typing import Any

from northstar_compliance.tools.gateway import ToolGateway
from northstar_compliance.tools.models import ToolInvocationRequest, ToolPrincipalContext, ToolResultEnvelope

from .decision import DecisionProvider
from .models import AgentGoal, AgentObservation, AgentRunOutcome, AgentRunState, DecisionKind, RunStatus, TerminationReason
from .termination import TerminationEvaluator


class BoundedSingleAgentRuntime:
    AGENT_ID = "AGT-001"
    ALLOWED_TOOLS = {f"TOOL-{n:03d}" for n in range(1, 7)}

    def __init__(self, gateway: ToolGateway, decision_provider: DecisionProvider, artifact_root: Path):
        self.gateway = gateway
        self.decision_provider = decision_provider
        self.artifact_root = artifact_root
        self.termination = TerminationEvaluator()

    def run(
        self,
        goal: AgentGoal,
        principal: ToolPrincipalContext,
        *,
        max_iterations: int = 10,
        repeat_limit: int = 2,
        no_progress_limit: int = 2,
    ) -> tuple[AgentRunState, AgentRunOutcome, Path]:
        run_id = "RUN-" + uuid.uuid4().hex[:16].upper()
        state = AgentRunState(
            schema_version="1.0.0",
            run_id=run_id,
            agent_id=self.AGENT_ID,
            goal=goal,
            max_iterations=max_iterations,
            repeat_limit=repeat_limit,
            no_progress_limit=no_progress_limit,
        )
        while state.status == RunStatus.RUNNING:
            if self.termination.pre_iteration(state):
                break
            decision = self.decision_provider.decide(goal, state, self.gateway.registry.model_view())
            state.decisions.append(decision)
            state.iteration += 1
            if self.termination.evaluate_decision(state, decision):
                break
            assert decision.kind == DecisionKind.CALL_TOOL
            assert decision.tool_id and decision.tool_version and decision.arguments is not None
            if decision.tool_id not in self.ALLOWED_TOOLS:
                self.termination.terminate(state, RunStatus.ESCALATED, TerminationReason.INVALID_DECISION, f"Agent proposed a non-allowlisted tool: {decision.tool_id}")
                break
            signature = self._action_signature(decision.tool_id, decision.tool_version, decision.arguments)
            if self.termination.register_action_signature(state, signature):
                break
            idempotency_key = None
            if decision.tool_id in {"TOOL-004", "TOOL-005", "TOOL-006"}:
                idempotency_key = f"{run_id}:{decision.tool_id}:{goal.goal_id}"
            request = ToolInvocationRequest(
                tool_id=decision.tool_id,
                tool_version=decision.tool_version,
                arguments=decision.arguments,
                principal=principal,
                idempotency_key=idempotency_key,
            )
            result = self.gateway.invoke(request)
            before = set(state.progress_milestones)
            self._apply_observation(state, result)
            after = set(state.progress_milestones)
            state.observations.append(AgentObservation(
                iteration=state.iteration,
                tool_id=decision.tool_id,
                tool_status=result.status,
                action_signature=signature,
                progress_before=tuple(sorted(before)),
                progress_after=tuple(sorted(after)),
                result_summary=self._result_summary(result),
            ))
            if not result.succeeded:
                self.termination.terminate(state, RunStatus.ESCALATED, TerminationReason.TOOL_FAILURE, f"{decision.tool_id} returned {result.status}: {result.error_code}")
                break
            if self.termination.register_progress(state, before, after):
                break

        if state.termination_reason is None:
            self.termination.terminate(state, RunStatus.ESCALATED, TerminationReason.INVALID_DECISION, "Runtime left the loop without a terminal reason.")
        outcome = AgentRunOutcome(
            run_id=state.run_id,
            agent_id=state.agent_id,
            status=state.status,
            termination_reason=state.termination_reason,
            summary=state.termination_summary or "",
            iterations=state.iteration,
            progress_milestones=tuple(state.progress_milestones),
            artifact_references=dict(state.artifacts),
            human_review_required=True,
            final_disposition="preliminary_grounded_unapproved",
        )
        path = self.gateway.store.write_run(state.run_id, {"state": state.to_dict(), "outcome": outcome.to_dict()})
        return state, outcome, path

    @staticmethod
    def _action_signature(tool_id: str, version: str, arguments: dict[str, Any]) -> str:
        canonical = json.dumps(arguments, sort_keys=True, separators=(",", ":")).encode()
        return f"{tool_id}:{version}:{hashlib.sha256(canonical).hexdigest()}"

    @staticmethod
    def _result_summary(result: ToolResultEnvelope) -> dict[str, Any]:
        return {
            "status": result.status,
            "invocation_id": result.invocation_id,
            "error_code": result.error_code,
            "result_keys": sorted(result.data) if result.data else [],
        }

    @staticmethod
    def _add_milestone(state: AgentRunState, milestone: str) -> None:
        if milestone not in state.progress_milestones:
            state.progress_milestones.append(milestone)

    def _apply_observation(self, state: AgentRunState, result: ToolResultEnvelope) -> None:
        if not result.succeeded or result.data is None:
            return
        if result.tool_id == "TOOL-001":
            state.artifacts["regulatory_sources"] = result.data["records"]
            if result.data["records"]: self._add_milestone(state, "regulatory_sources_found")
        elif result.tool_id == "TOOL-002":
            state.artifacts["controls"] = result.data["controls"]
            if result.data["controls"]: self._add_milestone(state, "control_candidates_found")
        elif result.tool_id == "TOOL-003":
            state.artifacts["retrieval_context"] = result.data
            if result.data["citations"]: self._add_milestone(state, "authorized_evidence_retrieved")
        elif result.tool_id == "TOOL-004":
            state.artifacts["draft_case"] = result.data
            if result.data.get("status") == "draft_unapproved": self._add_milestone(state, "draft_case_created")
        elif result.tool_id == "TOOL-005":
            state.artifacts["candidate_mapping"] = result.data
            if result.data.get("status") == "candidate_unapproved": self._add_milestone(state, "candidate_mapping_saved")
        elif result.tool_id == "TOOL-006":
            state.artifacts["review_request"] = result.data
            if result.data.get("status") == "queued_for_human_review": self._add_milestone(state, "human_review_queued")
