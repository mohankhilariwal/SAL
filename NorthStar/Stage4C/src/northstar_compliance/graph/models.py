from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AgentRunState:
    """Executable DATA-009 AgentRunState, schema version 1.1.0."""

    run_id: str
    session_id: str
    initiator_id: str
    graph_id: str = "GRAPH-001"
    graph_version: str = "1.1.0"
    schema_version: str = "1.1.0"
    status: str = "created"
    current_node: str = "N00_START"
    disposition: str = "preliminary_grounded_unapproved"
    review_outcome: str | None = None
    review_request_id: str | None = None
    wait_id: str | None = None
    tool006_idempotency_key: str | None = None
    context_digest: str | None = None
    instruction_digest: str | None = None
    milestones: list[str] = field(default_factory=list)
    transitions: list[dict[str, Any]] = field(default_factory=list)
    model_calls: int = 0
    tool_calls: int = 0
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "AgentRunState":
        return cls(**value)


@dataclass(frozen=True)
class RuntimeResult:
    state: AgentRunState
    approval_token: str | None = None

    @property
    def run_id(self) -> str:
        return self.state.run_id
