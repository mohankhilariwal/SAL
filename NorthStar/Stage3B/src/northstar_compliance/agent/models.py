from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class DecisionKind(StrEnum):
    CALL_TOOL = "call_tool"
    COMPLETE = "complete"
    ESCALATE = "escalate"


class RunStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    ESCALATED = "escalated"
    TERMINATED_GUARD = "terminated_guard"


class TerminationReason(StrEnum):
    GOAL_COMPLETE = "goal_complete"
    HUMAN_ESCALATION = "human_escalation"
    INVALID_COMPLETION = "invalid_completion"
    TOOL_FAILURE = "tool_failure"
    ITERATION_LIMIT = "iteration_limit"
    REPEATED_ACTION = "repeated_action"
    NO_PROGRESS = "no_progress"
    INVALID_DECISION = "invalid_decision"


@dataclass(frozen=True)
class AgentGoal:
    goal_id: str
    publication_id: str
    title: str
    objective: str
    jurisdictions: tuple[str, ...]
    business_domains: tuple[str, ...]
    evidence_query: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["jurisdictions"] = list(self.jurisdictions)
        data["business_domains"] = list(self.business_domains)
        return data


@dataclass(frozen=True)
class AgentDecision:
    kind: DecisionKind
    reason_summary: str
    expected_progress: str
    tool_id: str | None = None
    tool_version: str | None = None
    arguments: dict[str, Any] | None = None

    def validate(self) -> None:
        if not self.reason_summary.strip() or not self.expected_progress.strip():
            raise ValueError("reason_summary and expected_progress are required")
        if self.kind == DecisionKind.CALL_TOOL:
            if not self.tool_id or not self.tool_version or self.arguments is None:
                raise ValueError("call_tool requires tool_id, tool_version and arguments")
        elif self.tool_id is not None or self.tool_version is not None or self.arguments is not None:
            raise ValueError("terminal decisions cannot include tool fields")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["kind"] = self.kind.value
        return data


@dataclass(frozen=True)
class AgentObservation:
    iteration: int
    tool_id: str
    tool_status: str
    action_signature: str
    progress_before: tuple[str, ...]
    progress_after: tuple[str, ...]
    result_summary: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["progress_before"] = list(self.progress_before)
        data["progress_after"] = list(self.progress_after)
        return data


@dataclass
class AgentRunState:
    schema_version: str
    run_id: str
    agent_id: str
    goal: AgentGoal
    status: RunStatus = RunStatus.RUNNING
    iteration: int = 0
    max_iterations: int = 10
    repeat_limit: int = 2
    no_progress_limit: int = 2
    progress_milestones: list[str] = field(default_factory=list)
    decisions: list[AgentDecision] = field(default_factory=list)
    observations: list[AgentObservation] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    last_action_signature: str | None = None
    consecutive_repeats: int = 0
    consecutive_no_progress: int = 0
    termination_reason: TerminationReason | None = None
    termination_summary: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "agent_id": self.agent_id,
            "goal": self.goal.to_dict(),
            "status": self.status.value,
            "iteration": self.iteration,
            "max_iterations": self.max_iterations,
            "repeat_limit": self.repeat_limit,
            "no_progress_limit": self.no_progress_limit,
            "progress_milestones": list(self.progress_milestones),
            "decisions": [d.to_dict() for d in self.decisions],
            "observations": [o.to_dict() for o in self.observations],
            "artifacts": self.artifacts,
            "last_action_signature": self.last_action_signature,
            "consecutive_repeats": self.consecutive_repeats,
            "consecutive_no_progress": self.consecutive_no_progress,
            "termination_reason": self.termination_reason.value if self.termination_reason else None,
            "termination_summary": self.termination_summary,
        }


@dataclass(frozen=True)
class AgentRunOutcome:
    run_id: str
    agent_id: str
    status: RunStatus
    termination_reason: TerminationReason
    summary: str
    iterations: int
    progress_milestones: tuple[str, ...]
    artifact_references: dict[str, Any]
    human_review_required: bool
    final_disposition: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["termination_reason"] = self.termination_reason.value
        data["progress_milestones"] = list(self.progress_milestones)
        return data
