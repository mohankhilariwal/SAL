from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

AuthorityEffect = Literal["none"]
EvidenceStatus = Literal["present", "missing", "proposed", "local_only", "unapproved", "unexercised"]
Severity = Literal["hard", "soft"]


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    title: str
    status: EvidenceStatus
    source: str
    digest: str | None = None
    authority_effect: AuthorityEffect = "none"

    @property
    def production_sufficient(self) -> bool:
        return self.status == "present"


@dataclass(frozen=True)
class Blocker:
    blocker_id: str
    title: str
    severity: Severity
    evidence_id: str
    remediation_owner: str
    rationale: str
    authority_effect: AuthorityEffect = "none"


@dataclass(frozen=True)
class ReconciliationResult:
    required_ids: tuple[str, ...]
    present_ids: tuple[str, ...]
    missing_ids: tuple[str, ...]
    duplicate_ids: tuple[str, ...]
    invalid_authority_ids: tuple[str, ...]
    complete: bool
    authority_effect: AuthorityEffect = "none"


@dataclass(frozen=True)
class FinalAssessment:
    assessment_id: str
    decision: Literal["denied", "conditional_preproduction_only"]
    production_route_enabled: Literal[False]
    active_agent_count: Literal[1]
    selected_topology: Literal["one_agent_specialized_graph_profiles"]
    hard_blockers: tuple[Blocker, ...] = field(default_factory=tuple)
    soft_gaps: tuple[Blocker, ...] = field(default_factory=tuple)
    rationale: tuple[str, ...] = field(default_factory=tuple)
    authority_effect: AuthorityEffect = "none"


@dataclass(frozen=True)
class TopologyComparison:
    comparison_id: str
    selected_topology: Literal["one_agent_specialized_graph_profiles"]
    single_agent_score: int
    multi_agent_score: int
    measured_quality_gain: float | None
    handoff_error_rate: float | None
    representative_evidence: bool
    reasons: tuple[str, ...]
    authority_effect: AuthorityEffect = "none"
