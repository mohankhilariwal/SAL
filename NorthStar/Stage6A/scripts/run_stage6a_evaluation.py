from dataclasses import replace
import json
from pathlib import Path
from northstar_compliance.architecture_decision import AgentBoundaryAssessor,AgentBoundaryPolicy,AgentBoundaryQuestionnaire,load_task_profiles
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=AgentBoundaryPolicy.from_path(ROOT/'config/architecture/agent-boundary-policy.json'); x=AgentBoundaryAssessor(p)
 q=AgentBoundaryQuestionnaire(assessment_id='EVAL-S06A',case_family='regulatory-impact'); a=x.assess(q); ps=load_task_profiles(ROOT/'config/agents/AGT-001-task-profiles.json',p)
 h=x.assess(replace(q,assessment_id='HARD',independent_authority_required=True)); m=x.assess(replace(q,assessment_id='MEASURED',evidence_status='representative',prompt_node_remediation_exhausted=True,measured_quality_gain_pct=12.5,measured_handoff_error_pct=1.0))
 r={'stage':'S06A','evaluations':{
 'EVAL-055':{'passed':a.selected_option=='one_agent_specialized_graph_profiles','detail':'deterministic selection'},
 'EVAL-056':{'passed':len(ps)==6 and {z.agent_id for z in ps}=={'AGT-001'},'detail':'task-profile coverage'},
 'EVAL-057':{'passed':all(not any((z.can_delegate,z.can_handoff,z.can_approve,z.can_finalize,z.can_write_memory,z.concurrent_execution)) for z in ps),'detail':'authority boundary'},
 'EVAL-058':{'passed':h.multi_agent_promotion_allowed and m.multi_agent_promotion_allowed,'detail':'counterfactual triggers'},
 'EVAL-059':{'passed':all(z.reasons for z in a.candidates),'detail':'coordination/failure evidence'},
 'EVAL-060':{'passed':bool(a.assessment_sha256) and all(z.profile_sha256 for z in ps),'detail':'deterministic digests'},
 'EVAL-061':{'passed':a.selected_agent_count==1 and not a.multi_agent_promotion_allowed,'detail':'change-review gate'}},'limitations':['local deterministic evaluation; no live model or multi-agent quality benchmark']}
 r['passed']=all(z['passed'] for z in r['evaluations'].values()); print(json.dumps(r,indent=2,sort_keys=True)); return 0 if r['passed'] else 1
if __name__=='__main__': raise SystemExit(main())
