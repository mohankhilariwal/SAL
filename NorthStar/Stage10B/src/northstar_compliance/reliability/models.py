from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class FailureClass(StrEnum):
    TRANSIENT = "transient"
    PERMANENT = "permanent"
    AMBIGUOUS_OUTCOME = "ambiguous_outcome"
    OVERLOAD = "overload"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    POLICY = "policy"
    SECURITY = "security"
    DATA_INTEGRITY = "data_integrity"
    HUMAN_TIMEOUT = "human_timeout"
    AUDIT = "audit"
    CONFIGURATION = "configuration"


class EffectClass(StrEnum):
    READ_ONLY = "read_only"
    REVERSIBLE_WRITE = "reversible_write"
    PROTECTED_WRITE = "protected_write"


class RecoveryAction(StrEnum):
    RETRY = "retry"
    FALLBACK = "fallback"
    RECONCILE = "reconcile"
    QUARANTINE = "quarantine"
    DEAD_LETTER = "dead_letter"
    DEGRADE_READ_ONLY = "degrade_read_only"
    SHED_LOAD = "shed_load"
    ESCALATE_HUMAN = "escalate_human"
    FAIL_CLOSED = "fail_closed"
    STOP = "stop"


@dataclass(frozen=True)
class FailureEnvelope:
    failure_id: str
    component_id: str
    operation: str
    failure_class: FailureClass
    effect_class: EffectClass
    retryable: bool
    ambiguous: bool = False
    status_code: str | None = None
    safe_summary: str = ""
    correlation: dict[str, str] = field(default_factory=dict)
    authority_effect: str = "none"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["failure_class"] = self.failure_class.value
        data["effect_class"] = self.effect_class.value
        return data


@dataclass(frozen=True)
class RetryPolicy:
    policy_id: str
    max_attempts: int
    base_delay_seconds: float
    max_delay_seconds: float
    total_budget_seconds: float
    retryable_classes: frozenset[FailureClass]
    require_idempotency_for_writes: bool = True
    authority_effect: str = "none"


@dataclass(frozen=True)
class RecoveryDecision:
    action: RecoveryAction
    reason: str
    may_retry: bool = False
    requires_reauthorization: bool = False
    requires_reconciliation: bool = False
    requires_human: bool = False
    authority_effect: str = "none"


@dataclass(frozen=True)
class ReleaseManifest:
    release_id: str
    environment: str
    architecture_version: str
    repository_version: str
    graph_version: str
    agent_spec_version: str
    config_digest: str
    source_digest: str
    test_report_digest: str
    unresolved_stage_8d: bool = True
    unresolved_stage_9d: bool = True
    production_route_enabled: bool = False
    authority_effect: str = "none"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
