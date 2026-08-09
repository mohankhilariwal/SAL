from __future__ import annotations
from dataclasses import replace
from .canonical import sha256_hex
from .models import AgentBoundaryAssessment, CandidateAssessment
class AgentBoundaryAssessor:
    def __init__(self,policy): self.policy=policy
    def assess(self,q):
        q.validate(); eligible,reasons=self.policy.multi_agent_review_eligible(q)
        shared=sum((q.shared_authoritative_state,q.shared_tool_gateway,q.shared_human_approval,q.shared_memory_scope))
        boundary=len(self.policy.hard_boundary_triggers(q)); seq=18 if q.task_dependency=="mostly_sequential" else (8 if q.task_dependency=="mixed" else 0)
        multi=72+boundary*6-(12 if q.evidence_status=="not_measured" else 0)-seq-(0 if q.parallelism_proven else 6)-(8 if shared==4 else 0)+(4 if q.prompt_node_remediation_exhausted else 0)
        cs=(
          CandidateAssessment("one_agent_generalist",58-(8 if q.persistent_tool_confusion else 0),True,("preserves_one_identity","insufficient_task_focus"),0,0,1),
          CandidateAssessment("one_agent_profiled",78+min(shared,4),True,("task_specific_instruction_and_context","no_new_identity_or_handoff"),0,0,1),
          CandidateAssessment("one_agent_specialized_graph_profiles",92+min(shared,4)-(4 if q.persistent_tool_confusion else 0),True,("shared_case_state_gateway_approval_and_memory_scope","application_owned_routes_and_state","specialization_without_delegation"),0,0,1),
          CandidateAssessment("manager_bounded_agents",multi,eligible,reasons+("requires_new_identity_handoff_and_termination_contracts",),6,6,7),
          CandidateAssessment("peer_handoff_agents",multi-15,eligible and q.task_dependency!="mostly_sequential",reasons+("peer_handoff_increases_deadlock_surface",),5,10,6),
          CandidateAssessment("distributed_autonomous_agents",max(0,multi-32),False,("outside_current_boundary","not_required_for_one_case_workflow"),6,15,7),
        )
        selected=max((c for c in cs if c.eligible),key=lambda c:(c.score,-c.new_agent_count))
        if selected.new_agent_count>0: selected=next(c for c in cs if c.option=="one_agent_specialized_graph_profiles"); reasons=reasons+("stage6a_does_not_allocate_agents",)
        draft=AgentBoundaryAssessment(q.assessment_id,selected.option,1,eligible,reasons,cs,("fit_scores_are_design_evidence_not_production_benchmarks","no_live_model_or_multi_agent_runtime_measured","review_eligibility_does_not_allocate_an_agent"),self.policy.version)
        return replace(draft,assessment_sha256=sha256_hex(draft))
