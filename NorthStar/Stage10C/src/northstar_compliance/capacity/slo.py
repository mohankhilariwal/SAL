from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class SLIKind(StrEnum):
    AVAILABILITY = "availability"
    LATENCY = "latency"
    KNOWN_DISPOSITION = "known_disposition"
    EVIDENCE_COMPLETENESS = "evidence_completeness"
    TASK_SUCCESS = "task_success"


@dataclass(frozen=True)
class SLOProposal:
    slo_id: str
    name: str
    sli_kind: SLIKind
    target: Decimal
    window_days: int
    approved: bool = False
    excludes_control_violations: bool = False
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if not (Decimal("0") < self.target <= Decimal("1")):
            raise ValueError("target must be in (0,1]")
        if self.window_days <= 0:
            raise ValueError("window must be positive")


@dataclass(frozen=True)
class SLIObservation:
    eligible_events: int
    good_events: int
    control_violation_events: int = 0

    @property
    def ratio(self) -> Decimal | None:
        if self.eligible_events == 0:
            return None
        return Decimal(self.good_events) / Decimal(self.eligible_events)


@dataclass(frozen=True)
class ErrorBudgetResult:
    target: Decimal
    allowed_bad_events: Decimal
    observed_bad_events: int
    remaining_bad_events: Decimal
    exhausted: bool
    control_violation_events: int
    control_gate_passed: bool
    authority_effect: str = "none"


def evaluate_error_budget(proposal: SLOProposal, observation: SLIObservation) -> ErrorBudgetResult:
    allowed_bad = Decimal(observation.eligible_events) * (Decimal("1") - proposal.target)
    observed_bad = observation.eligible_events - observation.good_events
    remaining = allowed_bad - Decimal(observed_bad)
    control_gate = observation.control_violation_events == 0
    return ErrorBudgetResult(
        target=proposal.target,
        allowed_bad_events=allowed_bad,
        observed_bad_events=observed_bad,
        remaining_bad_events=remaining,
        exhausted=remaining < 0,
        control_violation_events=observation.control_violation_events,
        control_gate_passed=control_gate,
    )
