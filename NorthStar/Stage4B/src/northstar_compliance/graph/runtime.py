from __future__ import annotations

import uuid
from datetime import datetime, timezone

from northstar_compliance.approval.service import ApprovalService
from northstar_compliance.durable.store import DurableStore, LeaseUnavailable, parse_utc
from northstar_compliance.graph.definition import GraphDefinition
from northstar_compliance.graph.models import (
    AgentRunState, GraphExecutionState, GraphTransitionRecord, Principal, RunOutcome, WaitContext,
)
from northstar_compliance.tools.gateway import ToolGateway


class GraphRuntimeError(RuntimeError):
    pass


class DurableGraphRuntime:
    def __init__(self, *, graph: GraphDefinition, store: DurableStore, gateway: ToolGateway,
                 approvals: ApprovalService, wait_timeout_seconds: int = 3600, lease_seconds: int = 30):
        self.graph = graph
        self.store = store
        self.gateway = gateway
        self.approvals = approvals
        self.wait_timeout_seconds = wait_timeout_seconds
        self.lease_seconds = lease_seconds

    def new_state(self, *, initiated_by: str = "maya.chen") -> GraphExecutionState:
        run_id = "RUN-" + uuid.uuid4().hex[:16].upper()
        case_id = "CASE-" + uuid.uuid4().hex[:12].upper()
        run = AgentRunState(
            schema_version="1.1.0", run_id=run_id,
            goal="Produce an evidence-backed regulatory impact package and obtain human review",
            agent_id="AGT-001", principal=Principal(subject_id=initiated_by, roles=["regulatory_analyst"]),
            allowed_tools=["TOOL-001","TOOL-002","TOOL-003","TOOL-004","TOOL-005","TOOL-006"],
            milestones=["publication_identified","obligations_extracted","evidence_retrieved","case_drafted","mapping_saved"],
            artifacts={
                "case": {"case_id": case_id, "status": "draft_unapproved", "requires_human_review": True},
                "mapping": {"case_id": case_id, "status": "candidate_unapproved"},
            },
        )
        return GraphExecutionState(
            schema_version="1.1.0", graph_id=self.graph.graph_id, graph_version=self.graph.graph_version,
            current_node=self.graph.entry_node, run_state=run,
        )

    def start(self, *, now: datetime | None = None, initiated_by: str = "maya.chen") -> RunOutcome:
        now = now or datetime.now(timezone.utc)
        state = self.new_state(initiated_by=initiated_by)
        self.store.create_run(state, now)
        return self._resume(state.run_state.run_id, worker_id="starter", now=now, return_token=True)

    def resume(self, run_id: str, *, worker_id: str = "worker-1", now: datetime | None = None) -> RunOutcome:
        return self._resume(run_id, worker_id=worker_id, now=now or datetime.now(timezone.utc), return_token=False)

    def _transition(self, state: GraphExecutionState, route: str, target: str, evidence: dict | None = None) -> None:
        state.transitions.append(GraphTransitionRecord(
            sequence=len(state.transitions) + 1, source_node=state.current_node,
            route=route, target_node=target, evidence_summary=evidence or {},
        ))
        state.current_node = target

    def _resolve(self, state: GraphExecutionState, route: str) -> str:
        target = self.graph.edges.get((state.current_node, route))
        if target is None:
            raise GraphRuntimeError(f"unroutable_result:{state.current_node}:{route}")
        return target

    def _save(self, state: GraphExecutionState, revision: int, now: datetime) -> int:
        return self.store.save_run(state, revision, now)

    def _outcome(self, state: GraphExecutionState, token: str | None = None) -> RunOutcome:
        wc = state.wait_context
        return RunOutcome(
            run_id=state.run_state.run_id, status=state.graph_status, current_node=state.current_node,
            final_disposition=state.run_state.final_disposition, review_outcome=state.run_state.review_outcome,
            wait_id=wc.wait_id if wc else None, approval_token=token,
            termination_reason=state.run_state.termination_reason,
        )

    def _resume(self, run_id: str, *, worker_id: str, now: datetime, return_token: bool) -> RunOutcome:
        self.store.acquire_lease(run_id, worker_id, now, self.lease_seconds)
        token: str | None = None
        try:
            state, revision = self.store.load_run(run_id)
            if state.graph_id != self.graph.graph_id or state.graph_version != self.graph.graph_version:
                raise GraphRuntimeError("state_graph_version_mismatch")
            while state.current_node != "__END__":
                node = state.current_node
                if node == "N00_VALIDATE_CONTEXT":
                    route = "valid" if state.run_state.agent_id == "AGT-001" else "invalid"
                    target = self._resolve(state, route); self._transition(state, route, target)
                elif node == "N10_GUARDS":
                    target = self._resolve(state, "continue"); self._transition(state, "continue", target)
                elif node == "N20_MODEL_DECIDE":
                    state.run_state.model_calls += 1
                    state.pending_decision = {"kind":"tool","tool_id":"TOOL-006"}
                    target = self._resolve(state, "tool"); self._transition(state, "tool", target, {"agent_id":"AGT-001","tool_id":"TOOL-006"})
                elif node == "N30_POLICY_GATE":
                    allowed = state.pending_decision and state.pending_decision.get("tool_id") in state.run_state.allowed_tools
                    route = "allowed" if allowed else "denied"
                    target = self._resolve(state, route); self._transition(state, route, target)
                elif node == "N40_TOOL_EXECUTE":
                    case_id = state.run_state.artifacts["case"]["case_id"]
                    result = self.gateway.queue_review(run_id=run_id, case_id=case_id, now=now)
                    state.run_state.tool_calls += 1
                    state.pending_result = result
                    target = self._resolve(state, "success"); self._transition(state, "success", target, {"tool_id":"TOOL-006","created":result["created"]})
                elif node == "N60_OBSERVE":
                    result = state.pending_result or {}
                    state.run_state.artifacts["review"] = {
                        "review_request_id": result["review_request_id"], "case_id": result["case_id"],
                        "status": "queued_for_human_review", "requires_human_review": True,
                    }
                    if "review_queued" not in state.run_state.milestones:
                        state.run_state.milestones.append("review_queued")
                    state.run_state.observations.append({"tool_id":"TOOL-006","review_request_id":result["review_request_id"]})
                    target = self._resolve(state, "observed"); self._transition(state, "observed", target)
                elif node == "N70_COMPLETION_CHECK":
                    required = {"publication_identified","obligations_extracted","evidence_retrieved","case_drafted","mapping_saved","review_queued"}
                    valid = required.issubset(state.run_state.milestones) and state.run_state.artifacts["review"]["requires_human_review"]
                    route = "review_ready" if valid else "invalid_completion"
                    target = self._resolve(state, route); self._transition(state, route, target)
                elif node == "N75_CREATE_REVIEW_WAIT":
                    review = state.run_state.artifacts["review"]
                    wait, token = self.approvals.create_wait(
                        run_id=run_id, review_request_id=review["review_request_id"],
                        initiated_by=state.run_state.principal.subject_id, required_role="compliance_approver",
                        graph_id=state.graph_id, graph_version=state.graph_version, now=now,
                        timeout_seconds=self.wait_timeout_seconds,
                    )
                    state.wait_context = WaitContext(
                        wait_id=wait["wait_id"], review_request_id=wait["review_request_id"],
                        required_role=wait["required_role"], expires_at=wait["expires_at"], token_digest=wait["token_digest"],
                    )
                    state.graph_status = "waiting_for_human_review"
                    target = self._resolve(state, "wait"); self._transition(state, "wait", target, {"wait_id":wait["wait_id"],"expires_at":wait["expires_at"]})
                    revision = self._save(state, revision, now)
                    return self._outcome(state, token if return_token else None)
                elif node == "N80_REVIEW_DECISION_GATE":
                    if not state.wait_context:
                        raise GraphRuntimeError("missing_wait_context")
                    wait = self.store.load_wait(wait_id=state.wait_context.wait_id)
                    if wait["status"] == "pending" and parse_utc(wait["expires_at"]) <= now:
                        self.store.expire_wait(wait["wait_id"], now); wait = self.store.load_wait(wait_id=wait["wait_id"])
                    if wait["status"] == "pending":
                        state.graph_status = "waiting_for_human_review"
                        return self._outcome(state)
                    if wait["status"] == "decided":
                        state.review_decision = self.store.load_decision(wait["wait_id"])
                        route = "approved" if state.review_decision.decision == "approved" else "rejected"
                    elif wait["status"] == "expired":
                        route = "expired"
                    else:
                        route = "invalid"
                    target = self._resolve(state, route); self._transition(state, route, target, {"wait_id":wait["wait_id"],"status":wait["status"]})
                    state.graph_status = "running"
                elif node == "N82_APPROVED_BRANCH":
                    state.run_state.review_outcome = "approved"
                    state.run_state.final_disposition = "preliminary_grounded_human_approved"
                    state.run_state.status = "completed"
                    state.run_state.termination_reason = "human_approved"
                    target = self._resolve(state, "complete"); self._transition(state, "complete", target)
                elif node == "N84_REJECTED_BRANCH":
                    state.run_state.review_outcome = "rejected"
                    state.run_state.final_disposition = "preliminary_grounded_human_rejected"
                    state.run_state.status = "completed"
                    state.run_state.termination_reason = "human_rejected"
                    target = self._resolve(state, "complete"); self._transition(state, "complete", target)
                elif node == "N86_EXPIRED_ESCALATION":
                    state.run_state.review_outcome = "expired_escalated"
                    state.run_state.final_disposition = "preliminary_grounded_unapproved"
                    state.run_state.status = "escalated"
                    state.run_state.termination_reason = "approval_timeout"
                    target = self._resolve(state, "escalate"); self._transition(state, "escalate", target)
                elif node == "N90_TERMINATE":
                    state.graph_status = state.run_state.status
                    target = self._resolve(state, "end"); self._transition(state, "end", target)
                else:
                    raise GraphRuntimeError(f"unknown_node:{node}")
                revision = self._save(state, revision, now)
            return self._outcome(state)
        finally:
            self.store.release_lease(run_id, worker_id)
