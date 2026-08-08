from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

TerminalStatus = Literal["running", "completed", "escalated", "terminated_guard", "cancelled"]
DecisionKind = Literal["call_tool", "complete", "escalate"]

REQUIRED_MILESTONES = (
    "regulatory_sources_found",
    "authorized_evidence_retrieved",
    "control_candidates_found",
    "draft_case_created",
    "candidate_mapping_saved",
    "human_review_queued",
)

@dataclass(frozen=True)
class AgentGoal:
    goal_id: str
    publication_id: str
    objective: str
    requested_by: str = "Maya Chen"

@dataclass(frozen=True)
class ModelUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    provider: str = "deterministic-local"
    model: str = "rule-provider-v1"

@dataclass(frozen=True)
class AgentDecision:
    kind: DecisionKind
    reason_summary: str
    expected_progress: str
    tool_id: str | None = None
    tool_version: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if self.kind == "call_tool":
            if not self.tool_id or not self.tool_version:
                raise ValueError("call_tool requires tool_id and tool_version")
        elif self.tool_id is not None or self.tool_version is not None or self.arguments:
            raise ValueError("terminal decision cannot carry tool fields")
        if self.kind not in {"call_tool", "complete", "escalate"}:
            raise ValueError(f"unknown decision kind: {self.kind}")

@dataclass(frozen=True)
class DecisionEnvelope:
    decision: AgentDecision
    usage: ModelUsage
    provider_attempts: int = 1
    fallback_used: bool = False

@dataclass
class RuntimeBudget:
    max_iterations: int = 12
    max_wall_time_ms: int = 30_000
    max_input_tokens: int = 12_000
    max_output_tokens: int = 4_000
    max_total_tokens: int = 16_000
    max_cost_micro_cad: int = 75_000
    max_tool_calls: int = 12
    max_failures: int = 5
    max_retries: int = 3
    max_replans: int = 2
    max_model_calls: int = 14

@dataclass
class BudgetLedger:
    iterations: int = 0
    elapsed_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_micro_cad: int = 0
    tool_calls: int = 0
    model_calls: int = 0
    failures: int = 0
    retries: int = 0
    replans: int = 0

@dataclass(frozen=True)
class FailureEnvelope:
    kind: str
    code: str
    message: str
    retryable: bool
    stage: str
    committed: bool | None = None
    tool_id: str | None = None
    idempotency_key: str | None = None

@dataclass(frozen=True)
class RecoveryRecord:
    action: str
    reason: str
    attempt: int
    tool_id: str | None = None
    outcome: str = "planned"

@dataclass(frozen=True)
class AgentObservation:
    tool_id: str
    status: str
    payload: dict[str, Any]
    milestone_added: str | None = None
    reconciled: bool = False
    fallback_used: bool = False

@dataclass
class AgentRunState:
    schema_version: str
    run_id: str
    agent_id: str
    goal: AgentGoal
    status: TerminalStatus = "running"
    termination_reason: str | None = None
    decisions: list[dict[str, Any]] = field(default_factory=list)
    observations: list[dict[str, Any]] = field(default_factory=list)
    milestones: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    budget: RuntimeBudget = field(default_factory=RuntimeBudget)
    ledger: BudgetLedger = field(default_factory=BudgetLedger)
    recovery_records: list[dict[str, Any]] = field(default_factory=list)
    blocked_action_signatures: list[str] = field(default_factory=list)
    consecutive_no_progress: int = 0
    last_action_signature: str | None = None
    repeated_action_count: int = 0
    checkpoint_sequence: int = 0
    resumed_from_checkpoint: bool = False
    human_review_required: bool = True
    final_disposition: str = "preliminary_grounded_unapproved"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentRunState":
        data = dict(data)
        data["goal"] = AgentGoal(**data["goal"])
        data["budget"] = RuntimeBudget(**data["budget"])
        data["ledger"] = BudgetLedger(**data["ledger"])
        return cls(**data)

@dataclass(frozen=True)
class AgentRunOutcome:
    run_id: str
    status: str
    termination_reason: str
    completed_milestones: tuple[str, ...]
    missing_milestones: tuple[str, ...]
    artifacts: dict[str, Any]
    budget_ledger: dict[str, Any]
    recovery_records: tuple[dict[str, Any], ...]
    human_review_required: bool = True
    final_disposition: str = "preliminary_grounded_unapproved"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
