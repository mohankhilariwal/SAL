from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
ArchitectureOption = Literal["one_agent_generalist","one_agent_profiled","one_agent_specialized_graph_profiles","manager_bounded_agents","peer_handoff_agents","distributed_autonomous_agents"]
@dataclass(frozen=True, slots=True)
class AgentBoundaryQuestionnaire:
    assessment_id: str; case_family: str
    current_agent_id: str = "AGT-001"; current_agent_spec_version: str = "1.1.0"
    graph_id: str = "GRAPH-001"; graph_version: str = "1.1.0"; state_schema_version: str = "1.1.0"
    shared_authoritative_state: bool = True; shared_tool_gateway: bool = True; shared_human_approval: bool = True; shared_memory_scope: bool = True
    independent_identity_required: bool = False; independent_authority_required: bool = False; independent_lifecycle_required: bool = False
    independent_fault_domain_required: bool = False; independent_termination_required: bool = False; verifier_independence_required: bool = False
    task_dependency: Literal["mostly_sequential","mixed","mostly_parallel"] = "mostly_sequential"
    parallelism_proven: bool = False; prompt_node_remediation_exhausted: bool = False; persistent_tool_confusion: bool = False
    measured_quality_gain_pct: float|None = None; measured_handoff_error_pct: float|None = None
    measured_latency_delta_pct: float|None = None; measured_cost_delta_pct: float|None = None
    evidence_status: Literal["not_measured","synthetic","representative"] = "not_measured"
    def validate(self):
        if self.current_agent_id != "AGT-001": raise ValueError("accepted baseline permits only AGT-001")
        if self.current_agent_spec_version != "1.1.0": raise ValueError("AGT-001-spec drift")
        if (self.graph_id,self.graph_version) != ("GRAPH-001","1.1.0"): raise ValueError("GRAPH-001 drift")
        if self.state_schema_version != "1.1.0": raise ValueError("DATA-009 drift")
        for name in ("measured_quality_gain_pct","measured_handoff_error_pct","measured_latency_delta_pct","measured_cost_delta_pct"):
            value=getattr(self,name)
            if value is not None and not -1000 <= value <= 1000: raise ValueError(name)
@dataclass(frozen=True, slots=True)
class CandidateAssessment:
    option: ArchitectureOption; score: int; eligible: bool; reasons: tuple[str,...]; new_agent_count: int; coordination_edges: int; authority_surfaces: int
@dataclass(frozen=True, slots=True)
class AgentBoundaryAssessment:
    assessment_id: str; selected_option: ArchitectureOption; selected_agent_count: int; multi_agent_promotion_allowed: bool
    promotion_reasons: tuple[str,...]; candidates: tuple[CandidateAssessment,...]; limitations: tuple[str,...]; policy_version: str; assessment_sha256: str = ""
@dataclass(frozen=True, slots=True)
class TaskProfile:
    profile_id: str; profile_version: str; agent_id: str; graph_id: str; graph_version: str; node_key: str; purpose: str; instruction_ref: str
    context_kinds: tuple[str,...]; exposed_tools: tuple[str,...]; output_contract: str; memory_access: Literal["none","via_harness_context_only"]
    can_delegate: bool; can_handoff: bool; can_approve: bool; can_finalize: bool; can_write_memory: bool; concurrent_execution: bool; profile_sha256: str = ""
@dataclass(frozen=True, slots=True)
class TaskProfileBinding:
    binding_id: str; run_id: str; agent_id: str; agent_spec_version: str; graph_id: str; graph_version: str; node_key: str
    profile_id: str; profile_version: str; profile_sha256: str; authority_owner: str; state_owner: str; route_owner: str; memory_owner: str; binding_sha256: str
