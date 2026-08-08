from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class Principal:
    subject_id: str
    roles: list[str]


@dataclass(slots=True)
class AgentRunState:
    schema_version: str
    run_id: str
    goal: str
    agent_id: str
    principal: Principal
    allowed_tools: list[str]
    milestones: list[str] = field(default_factory=list)
    artifacts: dict[str, dict[str, Any]] = field(default_factory=dict)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    observations: list[dict[str, Any]] = field(default_factory=list)
    model_calls: int = 0
    tool_calls: int = 0
    status: str = "running"
    termination_reason: str | None = None
    final_disposition: str = "preliminary_grounded_unapproved"
    human_review_required: bool = True
    review_outcome: str | None = None


@dataclass(slots=True)
class GraphTransitionRecord:
    sequence: int
    source_node: str
    route: str
    target_node: str
    evidence_summary: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class WaitContext:
    wait_id: str
    review_request_id: str
    required_role: str
    expires_at: str
    token_digest: str


@dataclass(slots=True)
class ReviewDecision:
    schema_version: str
    decision_id: str
    wait_id: str
    run_id: str
    decision: str
    reviewer_id: str
    reviewer_roles: list[str]
    reason: str | None
    issued_at: str
    token_nonce: str


@dataclass(slots=True)
class GraphExecutionState:
    schema_version: str
    graph_id: str
    graph_version: str
    current_node: str
    run_state: AgentRunState
    transitions: list[GraphTransitionRecord] = field(default_factory=list)
    pending_decision: dict[str, Any] | None = None
    pending_result: dict[str, Any] | None = None
    wait_context: WaitContext | None = None
    review_decision: ReviewDecision | None = None
    graph_status: str = "running"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "GraphExecutionState":
        rs = raw["run_state"]
        principal = Principal(**rs.pop("principal"))
        run_state = AgentRunState(principal=principal, **rs)
        transitions = [GraphTransitionRecord(**x) for x in raw.get("transitions", [])]
        wait_context = WaitContext(**raw["wait_context"]) if raw.get("wait_context") else None
        review_decision = ReviewDecision(**raw["review_decision"]) if raw.get("review_decision") else None
        return cls(
            schema_version=raw["schema_version"],
            graph_id=raw["graph_id"],
            graph_version=raw["graph_version"],
            current_node=raw["current_node"],
            run_state=run_state,
            transitions=transitions,
            pending_decision=raw.get("pending_decision"),
            pending_result=raw.get("pending_result"),
            wait_context=wait_context,
            review_decision=review_decision,
            graph_status=raw.get("graph_status", "running"),
        )


@dataclass(slots=True)
class RunOutcome:
    run_id: str
    status: str
    current_node: str
    final_disposition: str
    review_outcome: str | None
    wait_id: str | None = None
    approval_token: str | None = None
    termination_reason: str | None = None
