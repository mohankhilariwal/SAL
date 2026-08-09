from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


class GuardrailStage(StrEnum):
    INPUT = "input"
    CONTEXT = "context"
    RETRIEVAL = "retrieval"
    PLANNING = "planning"
    TOOL = "tool"
    OUTPUT = "output"
    STATE = "state"
    MEMORY = "memory"
    HUMAN_REVIEW = "human_review"
    RUNTIME = "runtime"


class Outcome(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    QUARANTINE = "quarantine"
    REQUIRE_HUMAN_REVIEW = "require_human_review"


OUTCOME_SEVERITY = {
    Outcome.ALLOW: 0,
    Outcome.REQUIRE_HUMAN_REVIEW: 1,
    Outcome.QUARANTINE: 2,
    Outcome.DENY: 3,
}


@dataclass(frozen=True)
class GuardrailRequest:
    request_id: str
    stage: GuardrailStage
    tenant_id: str
    case_id: str
    run_id: str
    task_id: str
    agent_id: str = "AGT-001"
    agent_spec_version: str = "1.1.0"
    policy_bundle_id: str = "GR-BUNDLE-001"
    policy_bundle_version: str = "1.0.0"
    payload: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ControlFinding:
    control_id: str
    passed: bool
    reason_code: str
    summary: str
    hard: bool
    synchronous: bool
    outcome_on_fail: Outcome
    model_assisted: bool = False


@dataclass(frozen=True)
class GuardrailDecision:
    decision_id: str
    request_id: str
    stage: GuardrailStage
    outcome: Outcome
    reason_codes: tuple[str, ...]
    findings: tuple[ControlFinding, ...]
    obligations: tuple[str, ...]
    policy_bundle_id: str
    policy_bundle_version: str
    policy_bundle_digest: str
    evaluated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    authority_effect: str = "none"
    exception_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
