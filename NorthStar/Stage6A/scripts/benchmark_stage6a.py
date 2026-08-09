import json
from pathlib import Path
from statistics import median
from time import perf_counter_ns
from northstar_compliance.architecture_decision import AgentBoundaryAssessor,AgentBoundaryPolicy,AgentBoundaryQuestionnaire,load_task_profiles
ROOT=Path(__file__).resolve().parents[1]
def p95(v):
 s=sorted(v); return s[min(len(s)-1,int(len(s)*.95))]
def main():
 p=AgentBoundaryPolicy.from_path(ROOT/'config/architecture/agent-boundary-policy.json'); a=AgentBoundaryAssessor(p); q=AgentBoundaryQuestionnaire(assessment_id='BENCH',case_family='regulatory-impact'); av=[]; pv=[]
 for _ in range(500):
  t=perf_counter_ns(); a.assess(q); av.append((perf_counter_ns()-t)/1e6)
  t=perf_counter_ns(); load_task_profiles(ROOT/'config/agents/AGT-001-task-profiles.json',p); pv.append((perf_counter_ns()-t)/1e6)
 r={'stage':'S06A','environment':{'python':'3.13.5','runtime_dependencies':'standard_library_only'},'workload':{'iterations':500,'profiles_per_validation':6},'latency_ms':{'assessment_p50':round(median(av),6),'assessment_p95':round(p95(av),6),'profile_validation_p50':round(median(pv),6),'profile_validation_p95':round(p95(pv),6)},'warning':'Local architecture-decision microbenchmark only; not model, workflow, quality, production SLO, concurrency or cost evidence.'}
 print(json.dumps(r,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
