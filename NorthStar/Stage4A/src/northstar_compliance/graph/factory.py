from __future__ import annotations

import uuid
from pathlib import Path

from northstar_compliance.agent.decision import DeterministicDecisionProvider
from northstar_compliance.agent.models import AgentRunState, PrincipalContext, RuntimeBudget
from northstar_compliance.state.checkpoint import LocalCheckpointStore
from northstar_compliance.tools.gateway import ToolGateway
from .definition import load_graph
from .models import TypedGraphExecutionState
from .nodes import NodeContext
from .runtime import GraphRuntime


def build_state(*, run_id: str | None = None, principal: PrincipalContext | None = None, budget: RuntimeBudget | None = None) -> TypedGraphExecutionState:
    run_id = run_id or f"RUN-{uuid.uuid4().hex[:12].upper()}"
    rs = AgentRunState(
        schema_version="1.1.0",
        run_id=run_id,
        agent_id="AGT-001",
        goal="Prepare an evidence-backed preliminary regulatory impact assessment and queue human review.",
        principal=principal or PrincipalContext(),
        allowed_tools=tuple(f"TOOL-{i:03d}" for i in range(1, 7)),
        budget=budget or RuntimeBudget(),
    )
    return TypedGraphExecutionState(
        schema_version="1.0.0",
        graph_id="GRAPH-001",
        graph_version="1.0.0",
        current_node="N00_VALIDATE_CONTEXT",
        run_state=rs,
    )


def build_runtime(
    repo_root: Path,
    *,
    gateway: ToolGateway | None = None,
    checkpoint_dir: Path | None = None,
    cancelled=None,
) -> tuple[GraphRuntime, ToolGateway]:
    graph = load_graph(repo_root / "config/graph/stage4a-regulatory-impact-graph.json")
    gateway = gateway or ToolGateway()
    context = NodeContext(gateway, DeterministicDecisionProvider(), cancelled=cancelled)
    store = LocalCheckpointStore(checkpoint_dir) if checkpoint_dir else None
    return GraphRuntime(graph, context, store), gateway
