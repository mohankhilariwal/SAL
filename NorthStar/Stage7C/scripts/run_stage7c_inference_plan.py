#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from dataclasses import asdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from northstar_compliance.inference.io import load_deployment, load_workload
from northstar_compliance.inference.planner import build_recommendation, build_selected_policy

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--deployment',default='config/inference/INF-001.json'); args=p.parse_args()
    dep=load_deployment(ROOT/args.deployment)
    rows=[]
    for path in sorted((ROOT/'config/workloads').glob('WP-*.json')):
        w=load_workload(path)
        if w.status!='active':
            rows.append({'profile_id':w.profile_id,'status':w.status,'decision':'blocked'}); continue
        policy=build_selected_policy(w,dep); rec=build_recommendation(w,dep,policy)
        rows.append({'profile_id':w.profile_id,'deployment_id':dep.deployment_id,'policy':asdict(policy),'recommendation':asdict(rec)})
    print(json.dumps(rows,indent=2,default=str)); return 0
if __name__=='__main__': raise SystemExit(main())
