from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
from .models import AgentBoundaryQuestionnaire
@dataclass(frozen=True, slots=True)
class AgentBoundaryPolicy:
    policy_id: str; version: str; minimum_measured_quality_gain_pct: float; maximum_handoff_error_pct: float
    require_representative_evidence: bool; allowed_agent_ids: tuple[str,...]; allowed_tool_ids: tuple[str,...]; prohibited_capabilities: tuple[str,...]
    @classmethod
    def from_path(cls,path):
        p=json.loads(Path(path).read_text())
        return cls(p["policy_id"],p["version"],float(p["minimum_measured_quality_gain_pct"]),float(p["maximum_handoff_error_pct"]),bool(p["require_representative_evidence"]),tuple(p["allowed_agent_ids"]),tuple(p["allowed_tool_ids"]),tuple(p["prohibited_capabilities"]))
    def hard_boundary_triggers(self,q):
        checks={"independent_identity":q.independent_identity_required,"independent_authority":q.independent_authority_required,"independent_lifecycle":q.independent_lifecycle_required,"independent_fault_domain":q.independent_fault_domain_required,"independent_termination":q.independent_termination_required,"independent_verifier":q.verifier_independence_required}
        return tuple(k for k,v in checks.items() if v)
    def measured_promotion_criteria_met(self,q):
        if q.measured_quality_gain_pct is None or q.measured_handoff_error_pct is None: return False
        if self.require_representative_evidence and q.evidence_status != "representative": return False
        return q.prompt_node_remediation_exhausted and q.measured_quality_gain_pct >= self.minimum_measured_quality_gain_pct and q.measured_handoff_error_pct <= self.maximum_handoff_error_pct
    def multi_agent_review_eligible(self,q):
        triggers=self.hard_boundary_triggers(q); measured=self.measured_promotion_criteria_met(q); reasons=[]
        if triggers: reasons.append("hard_boundary:"+",".join(triggers))
        if measured: reasons.append("representative_measured_gain_after_single_agent_remediation")
        if not reasons: reasons.append("no_independent_boundary_or_representative_measured_gain")
        return bool(triggers or measured),tuple(reasons)
