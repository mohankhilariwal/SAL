from __future__ import annotations

from dataclasses import asdict

from northstar_compliance.state.checkpoint import LocalCheckpointStore
from .models import ExecutionGraphDefinition, GraphTransitionRecord, TypedGraphExecutionState
from .nodes import NODE_FUNCTIONS, NodeContext
from .state import apply_patch


class GraphRoutingError(RuntimeError):
    pass


class GraphRuntime:
    def __init__(self, graph: ExecutionGraphDefinition, context: NodeContext, checkpoint_store: LocalCheckpointStore | None = None) -> None:
        self.graph = graph
        self.context = context
        self.checkpoint_store = checkpoint_store
        self.nodes = {n.node_id: n for n in graph.nodes}
        self.edges = {(e.source, e.route): e.target for e in graph.edges}

    def run(self, state: TypedGraphExecutionState, *, stop_after_transitions: int | None = None) -> TypedGraphExecutionState:
        if state.graph_id != self.graph.graph_id or state.graph_version != self.graph.graph_version:
            raise GraphRoutingError("state_graph_version_mismatch")
        while state.current_node != "__END__":
            if stop_after_transitions is not None and len(state.transitions) >= stop_after_transitions:
                break
            node = self.nodes[state.current_node]
            result = NODE_FUNCTIONS[node.node_id](state, self.context)
            next_state = apply_patch(state, node, result.patch)
            target = self.edges.get((node.node_id, result.route))
            if target is None:
                raise GraphRoutingError(f"unroutable_result:{node.node_id}:{result.route}")
            record = GraphTransitionRecord(
                sequence=len(next_state.transitions) + 1,
                source_node=node.node_id,
                node_type=node.node_type,
                route=result.route,
                target_node=target,
                evidence_summary=result.evidence,
            )
            next_state.transitions.append(asdict(record))
            next_state.current_node = target
            state = next_state
            if self.checkpoint_store:
                self.checkpoint_store.save(state)
        return state
