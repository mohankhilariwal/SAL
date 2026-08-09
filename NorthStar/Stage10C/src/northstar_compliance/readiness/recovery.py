from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ImpactTier(StrEnum):
    TIER_A_CRITICAL_CONTROL = "tier_a_critical_control"
    TIER_B_CASE_WORKFLOW = "tier_b_case_workflow"
    TIER_C_DERIVED_INDEX = "tier_c_derived_index"


@dataclass(frozen=True)
class RecoveryObjectiveProposal:
    profile_id: str
    impact_tier: ImpactTier
    rto_minutes: int
    rpo_minutes: int
    business_owner: str
    technical_owner: str
    security_reviewer: str
    governance_reviewer: str
    approved: bool = False
    tested: bool = False
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if self.rto_minutes < 0 or self.rpo_minutes < 0:
            raise ValueError("RTO/RPO must be non-negative")
        if self.authority_effect != "none":
            raise ValueError("recovery proposals cannot create authority")
