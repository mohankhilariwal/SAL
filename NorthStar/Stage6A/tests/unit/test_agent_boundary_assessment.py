from dataclasses import replace
from pathlib import Path
import pytest
from northstar_compliance.architecture_decision import AgentBoundaryAssessor,AgentBoundaryPolicy,AgentBoundaryQuestionnaire
ROOT=Path(__file__).resolve().parents[2];P=AgentBoundaryPolicy.from_path(ROOT/'config/architecture/agent-boundary-policy.json');A=AgentBoundaryAssessor(P);B=AgentBoundaryQuestionnaire(assessment_id='T',case_family='regulatory-impact')
def test_243_questionnaire_validates_accepted_baseline():B.validate()
def test_244_questionnaire_rejects_unknown_agent():
 with pytest.raises(ValueError):replace(B,current_agent_id='AGT-002').validate()
def test_245_questionnaire_rejects_graph_drift():
 with pytest.raises(ValueError):replace(B,graph_version='2.0.0').validate()
def test_246_selects_one_agent_specialized_graph_profiles():assert A.assess(B).selected_option=='one_agent_specialized_graph_profiles'
def test_247_selected_agent_count_is_one():assert A.assess(B).selected_agent_count==1
def test_248_no_promotion_without_boundary_or_measurement():assert not A.assess(B).multi_agent_promotion_allowed
def test_249_independent_authority_triggers_review():assert A.assess(replace(B,independent_authority_required=True)).multi_agent_promotion_allowed
def test_250_representative_measured_gain_triggers_review():assert A.assess(replace(B,evidence_status='representative',prompt_node_remediation_exhausted=True,measured_quality_gain_pct=12,measured_handoff_error_pct=1)).multi_agent_promotion_allowed
def test_251_synthetic_gain_rejected():assert not A.assess(replace(B,evidence_status='synthetic',prompt_node_remediation_exhausted=True,measured_quality_gain_pct=20,measured_handoff_error_pct=0)).multi_agent_promotion_allowed
def test_252_low_gain_rejected():assert not A.assess(replace(B,evidence_status='representative',prompt_node_remediation_exhausted=True,measured_quality_gain_pct=5,measured_handoff_error_pct=1)).multi_agent_promotion_allowed
def test_253_high_handoff_error_rejected():assert not A.assess(replace(B,evidence_status='representative',prompt_node_remediation_exhausted=True,measured_quality_gain_pct=20,measured_handoff_error_pct=5)).multi_agent_promotion_allowed
def test_254_all_candidates_have_reasons():assert all(x.reasons for x in A.assess(B).candidates)
def test_255_manager_surface_is_counted():
 x=next(x for x in A.assess(B).candidates if x.option=='manager_bounded_agents');assert x.coordination_edges==6 and x.authority_surfaces==7
