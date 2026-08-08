from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from northstar_compliance.agent.models import AgentRunState

NodeType = Literal["deterministic", "model", "policy", "tool", "recovery", "termination"]


@dataclass(frozen=True)
class NodeDefinition:
    node_id: str
    node_type: NodeType
    owned_paths: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class EdgeDefinition:
    source: str
    route: str
    target: str


@dataclass(frozen=True)
class ExecutionGraphDefinition:
    graph_id: str
    graph_version: str
    entry_node: str
    terminal_nodes: tuple[str, ...]
    nodes: tuple[NodeDefinition, ...]
    edges: tuple[EdgeDefinition, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GraphStatePatch:
    operations: dict[str, Any]


@dataclass(frozen=True)
class GraphNodeResult:
    route: str
    patch: GraphStatePatch
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphTransitionRecord:
    sequence: int
    source_node: str
    node_type: str
    route: str
    target_node: str
    evidence_summary: dict[str, Any]


@dataclass
class TypedGraphExecutionState:
    schema_version: str
    graph_id: str
    graph_version: str
    current_node: str
    run_state: AgentRunState
    transitions: list[dict[str, Any]] = field(default_factory=list)
    pending_decision: dict[str, Any] | None = None
    pending_result: dict[str, Any] | None = None
    pending_failure: dict[str, Any] | None = None
    status: str = "running"

    def to_dict(self) -> dict[str, Any]:
        raw = asdict(self)
        return raw

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "TypedGraphExecutionState":
        return cls(
            schema_version=raw["schema_version"],
            graph_id=raw["graph_id"],
            graph_version=raw["graph_version"],
            current_node=raw["current_node"],
            run_state=AgentRunState.from_dict(raw["run_state"]),
            transitions=list(raw.get("transitions", [])),
            pending_decision=raw.get("pending_decision"),
            pending_result=raw.get("pending_result"),
            pending_failure=raw.get("pending_failure"),
            status=raw.get("status", "running"),
        )
