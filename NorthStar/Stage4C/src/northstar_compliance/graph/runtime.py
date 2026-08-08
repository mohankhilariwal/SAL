from __future__ import annotations

from datetime import datetime

from northstar_compliance.approval.service import ApprovalService
from northstar_compliance.common.jsonutil import isoformat_utc
from northstar_compliance.durable.store import DurableStore, DurableStoreError
from northstar_compliance.graph.models import AgentRunState, RuntimeResult
from northstar_compliance.tools.gateway import ToolGateway


class GraphRuntimeError(RuntimeError):
    pass


REQUIRED_MILESTONES = [
    "regulatory_source_identified",
    "authorized_evidence_retrieved",
    "control_candidates_identified",
    "draft_unapproved_case_created",
    "candidate_unapproved_mapping_saved",
    "human_review_queued",
]


class DurableGraphRuntime:
    """GRAPH-001 v1.1.0. Harness composition must not change its route ownership."""

    graph_id = "GRAPH-001"
    graph_version = "1.1.0"

    def __init__(self, store: DurableStore, gateway: ToolGateway, approvals: ApprovalService, approval_ttl_seconds: int = 3600):
        self.store = store
        self.gateway = gateway
        self.approvals = approvals
        self.approval_ttl_seconds = approval_ttl_seconds

    @staticmethod
    def _transition(state: AgentRunState, source: str, route: str, target: str, now: datetime) -> None:
        state.transitions.append({
            "source": source,
            "route": route,
            "target": target,
            "at": isoformat_utc(now),
            "evidence": "application_owned_route",
        })
        state.current_node = target
        state.updated_at = isoformat_utc(now)

    def start(
        self,
        *,
        run_id: str,
        session_id: str,
        initiator_id: str,
        context_digest: str,
        instruction_digest: str,
        now: datetime,
    ) -> RuntimeResult:
        state = AgentRunState(
            run_id=run_id,
            session_id=session_id,
            initiator_id=initiator_id,
            context_digest=context_digest,
            instruction_digest=instruction_digest,
            created_at=isoformat_utc(now),
            updated_at=isoformat_utc(now),
        )
        self._transition(state, "N00_START", "validated", "N10_PREPARE_CONTEXT", now)
        self._transition(state, "N10_PREPARE_CONTEXT", "context_ready", "N20_AGENT_DECISION", now)
        state.model_calls = 1
        state.milestones.extend(REQUIRED_MILESTONES[:-1])
        self._transition(state, "N20_AGENT_DECISION", "review_required", "N70_COMPLETE_UNAPPROVED_PACKAGE", now)

        state.tool006_idempotency_key = f"{run_id}:TOOL-006:review"
        tool_result = self.gateway.invoke(
            agent_id="AGT-001",
            tool_id="TOOL-006",
            arguments={"disposition": "preliminary_grounded_unapproved", "run_id": run_id},
            idempotency_key=state.tool006_idempotency_key,
        )
        state.tool_calls = 1
        state.review_request_id = tool_result.data["review_request_id"]
        state.milestones.append("human_review_queued")
        self._transition(state, "N70_COMPLETE_UNAPPROVED_PACKAGE", "package_complete", "N75_CREATE_REVIEW_WAIT", now)

        # Persist first so the wait FK can reference the durable run.
        state.status = "creating_review_wait"
        self.store.save_workflow(state)
        wait, token = self.approvals.create_wait(
            run_id=run_id,
            review_request_id=state.review_request_id,
            graph_id=state.graph_id,
            graph_version=state.graph_version,
            required_role="compliance_approver",
            now=now,
            ttl_seconds=self.approval_ttl_seconds,
        )
        state.wait_id = wait["wait_id"]
        state.status = "waiting_for_human_review"
        self._transition(state, "N75_CREATE_REVIEW_WAIT", "wait_persisted", "N80_REVIEW_DECISION_GATE", now)
        self.store.save_workflow(state, expected_revision=1)
        return RuntimeResult(state=state, approval_token=token)

    def resume(self, *, run_id: str, session_id: str, worker_id: str, now: datetime) -> RuntimeResult:
        try:
            self.store.acquire_lease(run_id, worker_id, now)
            state, revision = self.store.load_workflow(run_id)
            if state.session_id != session_id:
                raise GraphRuntimeError("session_mismatch")
            if state.graph_id != self.graph_id or state.graph_version != self.graph_version:
                raise GraphRuntimeError("graph_version_mismatch")
            if state.current_node != "N80_REVIEW_DECISION_GATE":
                return RuntimeResult(state=state)
            wait = self.store.get_wait_by_run(run_id)
            if wait["status"] == "decided":
                decision = self.store.load_decision(wait["decision_id"])
                if decision["decision"] == "approved":
                    self._transition(state, "N80_REVIEW_DECISION_GATE", "approved", "N82_APPROVED_CONTINUATION", now)
                    state.status = "completed"
                    state.review_outcome = "approved"
                    state.disposition = "preliminary_grounded_human_approved"
                else:
                    self._transition(state, "N80_REVIEW_DECISION_GATE", "rejected", "N84_REJECTED_OUTCOME", now)
                    state.status = "completed"
                    state.review_outcome = "rejected"
                    state.disposition = "preliminary_grounded_human_rejected"
                self._transition(state, state.current_node, "terminate", "N90_TERMINATE", now)
            else:
                from northstar_compliance.common.jsonutil import parse_utc
                if parse_utc(wait["expires_at"]) <= now:
                    self.store.mark_wait_expired(wait["wait_id"], isoformat_utc(now))
                    self._transition(state, "N80_REVIEW_DECISION_GATE", "expired", "N86_EXPIRED_ESCALATION", now)
                    state.status = "escalated"
                    state.review_outcome = "expired_escalated"
                    state.disposition = "preliminary_grounded_unapproved"
                    self._transition(state, "N86_EXPIRED_ESCALATION", "terminate", "N90_TERMINATE", now)
                else:
                    state.status = "waiting_for_human_review"
                    return RuntimeResult(state=state)
            self.store.save_workflow(state, expected_revision=revision)
            return RuntimeResult(state=state)
        except DurableStoreError as exc:
            raise GraphRuntimeError(str(exc)) from exc
        finally:
            try:
                self.store.release_lease(run_id, worker_id)
            except Exception:
                pass
