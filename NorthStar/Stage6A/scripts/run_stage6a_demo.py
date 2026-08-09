from dataclasses import asdict
import json
from pathlib import Path
from northstar_compliance.architecture_decision import AgentBoundaryAssessor,AgentBoundaryPolicy,AgentBoundaryQuestionnaire,bind_task_profile,load_task_profiles
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=AgentBoundaryPolicy.from_path(ROOT/'config/architecture/agent-boundary-policy.json')
 q=AgentBoundaryQuestionnaire(assessment_id='ABA-NORTHSTAR-S06A-001',case_family='regulatory-impact-assessment')
 a=AgentBoundaryAssessor(p).assess(q); ps=load_task_profiles(ROOT/'config/agents/AGT-001-task-profiles.json',p)
 bs=[bind_task_profile(run_id='RUN-S06A-DEMO',profile=x) for x in ps]
 out={'stage':'S06A','architecture_version':'1.3.0','selected_option':a.selected_option,'agent_count':a.selected_agent_count,'agent_ids':sorted({x.agent_id for x in ps}),'graph':{'id':'GRAPH-001','version':'1.1.0'},'agent_spec':{'id':'AGT-001-spec','version':'1.1.0'},'multi_agent_promotion_allowed':a.multi_agent_promotion_allowed,'promotion_reasons':list(a.promotion_reasons),'assessment_sha256':a.assessment_sha256,'task_profiles':[asdict(x) for x in ps],'bindings':[asdict(x) for x in bs],'future_capabilities':{'delegation':False,'handoff':False,'shared_agent_memory':False,'concurrent_branches':False,'mcp':False,'a2a':False}}
 print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
