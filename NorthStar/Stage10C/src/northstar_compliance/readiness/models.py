from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class GateStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    NOT_EVALUATED = "not_evaluated"


class ReadinessDecisionValue(StrEnum):
    DENIED = "denied"
    CONDITIONAL_NON_PRODUCTION = "conditional_non_production"
    EVIDENCE_COMPLETE_BUT_BLOCKED = "evidence_complete_but_blocked"


@dataclass(frozen=True)
class ReadinessGate:
    gate_id: str
    name: str
    hard_blocker: bool
    status: GateStatus
    evidence_reference: str | None = None
    owner: str | None = None


@dataclass(frozen=True)
class ProductionReadinessEvidence:
    architecture_version: str
    repository_version: str
    graph_version: str
    agent_spec_version: str
    gates: tuple[ReadinessGate, ...]
    production_route_enabled: bool
    stage8d_resolved: bool
    stage9d_resolved: bool
    authority_effect: str = "none"


@dataclass(frozen=True)
class ProductionReadinessDecision:
    decision: ReadinessDecisionValue
    reasons: tuple[str, ...]
    failed_hard_gates: tuple[str, ...]
    production_route_enabled: bool = False
    authority_effect: str = "none"
