from __future__ import annotations

import copy
from dataclasses import asdict
from typing import Any

from northstar_compliance.agent.models import AgentRunState, BudgetLedger
from .models import GraphStatePatch, NodeDefinition, TypedGraphExecutionState


class PatchOwnershipError(PermissionError):
    pass


PROTECTED_PATHS = {
    "run_state.principal", "run_state.allowed_tools", "run_state.budget",
    "run_state.agent_id", "run_state.goal", "run_state.final_disposition",
    "run_state.human_review_required", "graph_id", "graph_version",
}


def apply_patch(state: TypedGraphExecutionState, node: NodeDefinition, patch: GraphStatePatch) -> TypedGraphExecutionState:
    new_state = copy.deepcopy(state)
    allowed = set(node.owned_paths)
    for path, value in patch.operations.items():
        if path in PROTECTED_PATHS or path not in allowed:
            raise PatchOwnershipError(f"node {node.node_id} cannot mutate {path}")
        _set_path(new_state, path, value)
    return new_state


def _set_path(state: TypedGraphExecutionState, path: str, value: Any) -> None:
    if path == "pending_decision": state.pending_decision = value
    elif path == "pending_result": state.pending_result = value
    elif path == "pending_failure": state.pending_failure = value
    elif path == "status": state.status = value
    elif path == "run_state.ledger": state.run_state.ledger = BudgetLedger(**value)
    elif path == "run_state.decisions": state.run_state.decisions = list(value)
    elif path == "run_state.observations": state.run_state.observations = list(value)
    elif path == "run_state.milestones": state.run_state.milestones = list(value)
    elif path == "run_state.artifacts": state.run_state.artifacts = dict(value)
    elif path == "run_state.recovery_records": state.run_state.recovery_records = list(value)
    elif path == "run_state.status": state.run_state.status = value
    elif path == "run_state.termination_reason": state.run_state.termination_reason = value
    elif path == "run_state.checkpoint_sequence": state.run_state.checkpoint_sequence = int(value)
    elif path == "run_state.resumed_from_checkpoint": state.run_state.resumed_from_checkpoint = bool(value)
    else: raise KeyError(path)
