from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path

from .models import EdgeDefinition, ExecutionGraphDefinition, NodeDefinition


class GraphDefinitionError(ValueError):
    pass


def load_graph(path: Path) -> ExecutionGraphDefinition:
    raw = json.loads(path.read_text(encoding="utf-8"))
    graph = ExecutionGraphDefinition(
        graph_id=raw["graph_id"],
        graph_version=raw["graph_version"],
        entry_node=raw["entry_node"],
        terminal_nodes=tuple(raw["terminal_nodes"]),
        nodes=tuple(NodeDefinition(
            node_id=n["node_id"], node_type=n["node_type"],
            owned_paths=tuple(n["owned_paths"]), description=n["description"]
        ) for n in raw["nodes"]),
        edges=tuple(EdgeDefinition(**e) for e in raw["edges"]),
    )
    validate_graph(graph)
    return graph


def validate_graph(graph: ExecutionGraphDefinition) -> None:
    ids = [n.node_id for n in graph.nodes]
    if len(ids) != len(set(ids)):
        raise GraphDefinitionError("duplicate_node_id")
    nodes = set(ids)
    if graph.entry_node not in nodes:
        raise GraphDefinitionError("entry_node_missing")
    if not set(graph.terminal_nodes).issubset(nodes):
        raise GraphDefinitionError("terminal_node_missing")

    route_keys: set[tuple[str, str]] = set()
    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in graph.edges:
        if edge.source not in nodes:
            raise GraphDefinitionError(f"unknown_edge_source:{edge.source}")
        if edge.target != "__END__" and edge.target not in nodes:
            raise GraphDefinitionError(f"unknown_edge_target:{edge.target}")
        key = (edge.source, edge.route)
        if key in route_keys:
            raise GraphDefinitionError(f"duplicate_route:{edge.source}:{edge.route}")
        route_keys.add(key)
        if edge.target != "__END__":
            adjacency[edge.source].append(edge.target)

    reached = {graph.entry_node}
    q = deque([graph.entry_node])
    while q:
        cur = q.popleft()
        for nxt in adjacency[cur]:
            if nxt not in reached:
                reached.add(nxt); q.append(nxt)
    missing = nodes - reached
    if missing:
        raise GraphDefinitionError("unreachable_nodes:" + ",".join(sorted(missing)))
    for terminal in graph.terminal_nodes:
        if (terminal, "end") not in route_keys:
            raise GraphDefinitionError(f"terminal_missing_end_route:{terminal}")
