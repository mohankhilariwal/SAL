from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class GraphDefinitionError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class GraphDefinition:
    graph_id: str
    graph_version: str
    entry_node: str
    terminal_nodes: tuple[str, ...]
    nodes: tuple[str, ...]
    edges: dict[tuple[str, str], str]


def load_graph(path: str | Path) -> GraphDefinition:
    raw: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    nodes = tuple(x["node_id"] for x in raw["nodes"])
    if len(nodes) != len(set(nodes)):
        raise GraphDefinitionError("duplicate_node")
    if raw["entry_node"] not in nodes:
        raise GraphDefinitionError("missing_entry")
    terminals = tuple(raw["terminal_nodes"])
    if any(x not in nodes for x in terminals):
        raise GraphDefinitionError("missing_terminal")
    edges: dict[tuple[str, str], str] = {}
    for edge in raw["edges"]:
        key = (edge["source"], edge["route"])
        if key in edges:
            raise GraphDefinitionError("duplicate_route")
        if edge["source"] not in nodes:
            raise GraphDefinitionError("unknown_source")
        if edge["target"] not in nodes and edge["target"] not in {"__END__", "__SUSPEND__"}:
            raise GraphDefinitionError("unknown_target")
        edges[key] = edge["target"]
    reachable = {raw["entry_node"]}
    changed = True
    while changed:
        changed = False
        for (source, _), target in edges.items():
            if source in reachable and target in nodes and target not in reachable:
                reachable.add(target); changed = True
    if set(nodes) - reachable:
        raise GraphDefinitionError(f"unreachable_nodes:{sorted(set(nodes)-reachable)}")
    for terminal in terminals:
        if edges.get((terminal, "end")) != "__END__":
            raise GraphDefinitionError("terminal_missing_end")
    return GraphDefinition(
        graph_id=raw["graph_id"], graph_version=raw["graph_version"],
        entry_node=raw["entry_node"], terminal_nodes=terminals,
        nodes=nodes, edges=edges,
    )
