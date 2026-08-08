from __future__ import annotations

from dataclasses import asdict
from typing import Any
import time

from northstar_compliance.agent.budgets import BudgetExceeded, BudgetManager
from northstar_compliance.agent.decision import DeterministicDecisionProvider
from northstar_compliance.agent.models import WRITE_TOOLS
from northstar_compliance.agent.termination import completion_valid
from northstar_compliance.tools.gateway import ToolGateway
from .models import GraphNodeResult, GraphStatePatch, TypedGraphExecutionState


class NodeContext:
    def __init__(self, gateway: ToolGateway, provider: DeterministicDecisionProvider, cancelled: callable | None = None) -> None:
        self.gateway = gateway
        self.provider = provider
        self.cancelled = cancelled or (lambda: False)
        self.started_monotonic = time.monotonic()


def validate_context(state: TypedGraphExecutionState, ctx: NodeContext) -> GraphNodeResult:
    rs = state.run_state
    ok = rs.agent_id == "AGT-001" and rs.final_disposition == "preliminary_grounded_unapproved" and rs.human_review_required
    if ok:
        return GraphNodeResult("valid", GraphStatePatch({}), {"invariants": "preserved"})
    return GraphNodeResult("invalid", GraphStatePatch({"run_state.status": "escalated", "run_state.termination_reason": "context_invariant_failed"}))


def guard_check(state: TypedGraphExecutionState, ctx: NodeContext) -> GraphNodeResult:
    if ctx.cancelled():
        return GraphNodeResult("cancelled", GraphStatePatch({"run_state.status": "cancelled", "run_state.termination_reason": "cancelled_by_caller"}))
    if len(state.transitions) >= state.run_state.budget.max_graph_transitions:
        return GraphNodeResult("guard_stop", GraphStatePatch({"run_state.status": "terminated_guard", "run_state.termination_reason": "graph_transition_budget_exhausted"}))
    return GraphNodeResult("continue", GraphStatePatch({}), {"transition_budget_remaining": state.run_state.budget.max_graph_transitions - len(state.transitions)})


def model_decide(state: TypedGraphExecutionState, ctx: NodeContext) -> GraphNodeResult:
    manager = BudgetManager(state.run_state, started_monotonic=ctx.started_monotonic)
    try:
        manager.before_model()
        decision, usage = ctx.provider.decide(state.run_state)
        manager.settle_model(*usage)
    except BudgetExceeded as exc:
        return GraphNodeResult("budget_stop", GraphStatePatch({
            "run_state.ledger": asdict(state.run_state.ledger),
            "run_state.status": "terminated_guard", "run_state.termination_reason": str(exc),
        }))
    decisions = state.run_state.decisions + [asdict(decision)]
    ops = {"pending_decision": asdict(decision), "run_state.decisions": decisions, "run_state.ledger": asdict(state.run_state.ledger)}
    return GraphNodeResult(decision.kind, GraphStatePatch(ops), {"decision_kind": decision.kind, "tool_id": decision.tool_id})


def policy_gate(state: TypedGraphExecutionState, ctx: NodeContext) -> GraphNodeResult:
    decision = state.pending_decision or {}
    tool_id = decision.get("tool_id")
    args = decision.get("arguments", {})
    if tool_id not in state.run_state.allowed_tools:
        return GraphNodeResult("denied", GraphStatePatch({"run_state.status": "escalated", "run_state.termination_reason": "tool_not_agent_allowlisted"}))
    if tool_id in WRITE_TOOLS and not state.run_state.principal.allow_writes:
        return GraphNodeResult("denied", GraphStatePatch({"run_state.status": "escalated", "run_state.termination_reason": "write_scope_denied"}))
    if {"allow_writes", "groups", "approval_granted", "principal_id"}.intersection(args):
        return GraphNodeResult("denied", GraphStatePatch({"run_state.status": "escalated", "run_state.termination_reason": "authority_like_argument_rejected"}))
    return GraphNodeResult("allowed", GraphStatePatch({}), {"preflight_policy": "allowed_gateway_rechecks"})


def tool_execute(state: TypedGraphExecutionState, ctx: NodeContext) -> GraphNodeResult:
    manager = BudgetManager(state.run_state, started_monotonic=ctx.started_monotonic)
    decision = state.pending_decision or {}
    try:
        manager.before_tool()
    except BudgetExceeded as exc:
        return GraphNodeResult("budget_stop", GraphStatePatch({
            "run_state.ledger": asdict(state.run_state.ledger),
            "run_state.status": "terminated_guard", "run_state.termination_reason": str(exc),
        }))
    result = ctx.gateway.invoke(decision["tool_id"], decision["arguments"], state.run_state.principal)
    ops: dict[str, Any] = {"run_state.ledger": asdict(state.run_state.ledger)}
    if result.status == "success":
        ops.update({"pending_result": asdict(result), "pending_failure": None})
        return GraphNodeResult("success", GraphStatePatch(ops), {"tool_id": decision["tool_id"], "adapter": result.adapter})
    ops.update({"pending_failure": asdict(result.failure), "pending_result": None})
    return GraphNodeResult("failure", GraphStatePatch(ops), {"tool_id": decision["tool_id"], "failure_kind": result.failure.kind})


def recovery(state: TypedGraphExecutionState, ctx: NodeContext) -> GraphNodeResult:
    failure = state.pending_failure or {}
    decision = state.pending_decision or {}
    manager = BudgetManager(state.run_state, started_monotonic=ctx.started_monotonic)
    try:
        manager.failure()
    except BudgetExceeded as exc:
        return GraphNodeResult("unresolved", GraphStatePatch({
            "run_state.ledger": asdict(state.run_state.ledger),
            "run_state.status": "terminated_guard", "run_state.termination_reason": str(exc),
        }))
    records = list(state.run_state.recovery_records)
    if failure.get("kind") == "transient" and decision.get("tool_id") in {"TOOL-001", "TOOL-002", "TOOL-003"}:
        try: manager.retry()
        except BudgetExceeded as exc:
            return GraphNodeResult("unresolved", GraphStatePatch({"run_state.ledger": asdict(state.run_state.ledger), "run_state.status": "terminated_guard", "run_state.termination_reason": str(exc)}))
        result = ctx.gateway.invoke(decision["tool_id"], decision["arguments"], state.run_state.principal, adapter="fallback")
        records.append({"action": "read_fallback", "reason": failure.get("code"), "attempt": 1, "tool_id": decision.get("tool_id"), "outcome": result.status})
        if result.status == "success":
            return GraphNodeResult("recovered", GraphStatePatch({
                "pending_result": asdict(result), "pending_failure": None,
                "run_state.recovery_records": records, "run_state.ledger": asdict(state.run_state.ledger),
            }), {"recovery": "read_fallback"})
    if failure.get("kind") == "ambiguous_write":
        found = ctx.gateway.reconcile(decision["tool_id"], failure["idempotency_key"])
        records.append({"action": "reconcile_write", "reason": failure.get("code"), "attempt": 1, "tool_id": decision.get("tool_id"), "outcome": "committed" if found else "unknown"})
        if found:
            result = {"status": "success", "payload": found, "failure": None, "adapter": "reconciliation"}
            return GraphNodeResult("recovered", GraphStatePatch({
                "pending_result": result, "pending_failure": None,
                "run_state.recovery_records": records, "run_state.ledger": asdict(state.run_state.ledger),
            }), {"recovery": "write_reconciliation"})
    records.append({"action": "escalate", "reason": failure.get("code", "unknown"), "attempt": 1, "tool_id": decision.get("tool_id"), "outcome": "unresolved"})
    return GraphNodeResult("unresolved", GraphStatePatch({
        "run_state.recovery_records": records, "run_state.ledger": asdict(state.run_state.ledger),
        "run_state.status": "escalated", "run_state.termination_reason": "recovery_unresolved",
    }))


def observe(state: TypedGraphExecutionState, ctx: NodeContext) -> GraphNodeResult:
    result = state.pending_result or {}
    payload = result.get("payload", {})
    milestone = payload.get("milestone")
    milestones = list(state.run_state.milestones)
    if milestone and milestone not in milestones:
        milestones.append(milestone)
    observations = state.run_state.observations + [{"tool_id": (state.pending_decision or {}).get("tool_id"), "status": result.get("status"), "payload": payload}]
    artifacts = dict(state.run_state.artifacts)
    artifact_type = payload.get("artifact_type")
    if artifact_type:
        artifacts[artifact_type] = payload
    return GraphNodeResult("observed", GraphStatePatch({
        "run_state.observations": observations,
        "run_state.milestones": milestones,
        "run_state.artifacts": artifacts,
        "pending_result": None,
        "pending_failure": None,
    }), {"milestone": milestone})


def completion_check(state: TypedGraphExecutionState, ctx: NodeContext) -> GraphNodeResult:
    decision = state.pending_decision or {}
    if decision.get("kind") == "complete":
        valid, reason = completion_valid(state.run_state)
        if valid:
            return GraphNodeResult("complete", GraphStatePatch({"run_state.status": "completed", "run_state.termination_reason": reason}))
        return GraphNodeResult("invalid_completion", GraphStatePatch({"run_state.status": "escalated", "run_state.termination_reason": reason}))
    return GraphNodeResult("continue", GraphStatePatch({"pending_decision": None}))


def terminate(state: TypedGraphExecutionState, ctx: NodeContext) -> GraphNodeResult:
    status = state.run_state.status
    if status == "running":
        status = "escalated"
        reason = state.run_state.termination_reason or "terminal_without_disposition"
    else:
        reason = state.run_state.termination_reason
    return GraphNodeResult("end", GraphStatePatch({"status": "terminal", "run_state.status": status, "run_state.termination_reason": reason}), {"status": status, "reason": reason})

NODE_FUNCTIONS = {
    "N00_VALIDATE_CONTEXT": validate_context,
    "N10_GUARD_CHECK": guard_check,
    "N20_MODEL_DECIDE": model_decide,
    "N30_POLICY_GATE": policy_gate,
    "N40_TOOL_EXECUTE": tool_execute,
    "N50_RECOVERY": recovery,
    "N60_OBSERVE": observe,
    "N70_COMPLETION_CHECK": completion_check,
    "N90_TERMINATE": terminate,
}
