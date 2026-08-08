from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

FINAL_DISPOSITION = "preliminary_grounded_unapproved"
REQUIRED_MILESTONES = (
    "regulatory_sources_found",
    "authorized_evidence_retrieved",
    "control_candidates_found",
    "draft_case_created",
    "candidate_mapping_saved",
    "human_review_queued",
)
WRITE_TOOLS = frozenset({"TOOL-004", "TOOL-005", "TOOL-006"})


@dataclass(frozen=True)
class PrincipalContext:
    principal_id: str = "MAYA-CHEN"
    groups: tuple[str, ...] = ("regulatory-analysts",)
    purpose: str = "regulatory-impact-assessment"
    residency: str = "CA"
    allow_writes: bool = True
    publication_scope: str = "PUB-NS-2026-001"


@dataclass(frozen=True)
class RuntimeBudget:
    max_iterations: int = 12
    max_wall_seconds: float = 30.0
    max_input_tokens: int = 3000
    max_output_tokens: int = 1200
    max_total_tokens: int = 4200
    max_cost_micro_cad: int = 15000
    max_tool_calls: int = 10
    max_model_calls: int = 12
    max_failures: int = 4
    max_retries: int = 2
    max_replans: int = 2
    max_graph_transitions: int = 90


@dataclass
class BudgetLedger:
    iterations: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_micro_cad: int = 0
    tool_calls: int = 0
    model_calls: int = 0
    failures: int = 0
    retries: int = 0
    replans: int = 0


@dataclass(frozen=True)
class AgentDecision:
    kind: Literal["tool", "complete", "escalate"]
    reason_summary: str
    tool_id: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FailureEnvelope:
    kind: str
    code: str
    message: str
    retryable: bool
    stage: str
    committed: bool | None
    tool_id: str | None = None
    idempotency_key: str | None = None


@dataclass(frozen=True)
class RecoveryRecord:
    action: str
    reason: str
    attempt: int
    tool_id: str | None
    outcome: str


@dataclass
class AgentRunState:
    schema_version: str
    run_id: str
    agent_id: str
    goal: str
    principal: PrincipalContext
    allowed_tools: tuple[str, ...]
    budget: RuntimeBudget
    ledger: BudgetLedger = field(default_factory=BudgetLedger)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    observations: list[dict[str, Any]] = field(default_factory=list)
    milestones: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    recovery_records: list[dict[str, Any]] = field(default_factory=list)
    blocked_action_signatures: list[str] = field(default_factory=list)
    checkpoint_sequence: int = 0
    resumed_from_checkpoint: bool = False
    status: str = "running"
    termination_reason: str | None = None
    final_disposition: str = FINAL_DISPOSITION
    human_review_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "AgentRunState":
        return cls(
            schema_version=raw["schema_version"],
            run_id=raw["run_id"],
            agent_id=raw["agent_id"],
            goal=raw["goal"],
            principal=PrincipalContext(**raw["principal"]),
            allowed_tools=tuple(raw["allowed_tools"]),
            budget=RuntimeBudget(**raw["budget"]),
            ledger=BudgetLedger(**raw.get("ledger", {})),
            decisions=list(raw.get("decisions", [])),
            observations=list(raw.get("observations", [])),
            milestones=list(raw.get("milestones", [])),
            artifacts=dict(raw.get("artifacts", {})),
            recovery_records=list(raw.get("recovery_records", [])),
            blocked_action_signatures=list(raw.get("blocked_action_signatures", [])),
            checkpoint_sequence=raw.get("checkpoint_sequence", 0),
            resumed_from_checkpoint=raw.get("resumed_from_checkpoint", False),
            status=raw.get("status", "running"),
            termination_reason=raw.get("termination_reason"),
            final_disposition=raw.get("final_disposition", FINAL_DISPOSITION),
            human_review_required=raw.get("human_review_required", True),
        )
