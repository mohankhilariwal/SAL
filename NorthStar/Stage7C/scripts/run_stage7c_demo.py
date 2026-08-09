#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from dataclasses import asdict
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from northstar_compliance.inference.io import load_deployment, load_workload
from northstar_compliance.inference.models import EvidenceKind, InferenceBenchmarkScenario, QualityParityRecord
from northstar_compliance.inference.planner import build_recommendation, build_selected_policy
from northstar_compliance.inference.simulation import simulate_inference_candidate
from northstar_compliance.inference.evaluation import evaluate_candidate

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('--profile', default='config/workloads/WP-002.json')
    p.add_argument('--deployment', default='config/inference/INF-003.json')
    p.add_argument('--acceptance-rate', type=float, default=.85)
    args=p.parse_args()
    workload=load_workload(ROOT/args.profile)
    deployment=load_deployment(ROOT/args.deployment)
    policy=build_selected_policy(workload,deployment)
    scenario=InferenceBenchmarkScenario('IBS-DEMO',workload,deployment,policy,EvidenceKind.SIMULATED,100,42,'representative','DATASET-S07C-QUALITY-001')
    quality=QualityParityRecord('QPR-DEMO','DATASET-S07C-QUALITY-001','a'*64,'b'*64,1.0,1.0,0.0,0.0,True,True,('synthetic local parity evidence',))
    observation=simulate_inference_candidate(scenario,quality,assumed_acceptance_rate=args.acceptance_rate)
    evaluations=evaluate_candidate(observation,policy,quality)
    payload={'recommendation':asdict(build_recommendation(workload,deployment,policy)),'policy':asdict(policy),'observation':asdict(observation),'evaluations':[asdict(x) for x in evaluations]}
    print(json.dumps(payload,indent=2,default=str))
    return 0 if all(x.passed for x in evaluations) else 2
if __name__=='__main__': raise SystemExit(main())
