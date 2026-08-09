#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from northstar_compliance.inference.io import load_deployment, load_workload
from northstar_compliance.inference.planner import build_selected_policy

def require(condition: bool, message: str)->None:
    if not condition: raise AssertionError(message)

def main()->int:
    required=[
        ROOT/'docs/stages/NorthStar-Stage-7C-Inference-Optimization-and-Speculative-Decoding.md',
        ROOT/'NorthStar-Stage-7C-Handoff-Pack.md',
        ROOT/'docs/architecture/diagrams/GRAPH-001-v1.4.0.mmd',
    ]
    required += [ROOT/'docs/source-of-truth'/f'{i:02d}-{name}.md' for i,name in enumerate([
        'Project-Constitution','Business-and-User-Story-Baseline','Requirements-Register','Architecture-Baseline','Component-and-Agent-Catalogue','Data-and-Schema-Register','ADR-Register','Repository-Manifest','Risk-Assumption-and-Issue-Register','Stage-Handoff-Pack'])]
    for path in required: require(path.exists(),f'missing {path.relative_to(ROOT)}')
    for i in range(122,131):
        path=ROOT/'schemas'/f'DATA-{i}.schema.json'; require(path.exists(),f'missing {path.name}'); json.loads(path.read_text())
    workloads=[load_workload(p) for p in sorted((ROOT/'config/workloads').glob('WP-*.json'))]
    require(len(workloads)==8,'expected WP-001..008')
    require(sum(w.status=='active' for w in workloads)==7,'exactly seven executable profiles')
    require(next(w for w in workloads if w.profile_id=='WP-008').status=='inactive_future','WP-008 must be inactive')
    deployments=[load_deployment(p) for p in sorted((ROOT/'config/inference').glob('INF-*.json'))]
    require(len(deployments)==3,'expected three deployment profiles')
    for w in workloads:
        if w.status=='active':
            for d in deployments:
                p=build_selected_policy(w,d)
                require(not p.semantic_response_cache_enabled,'semantic regulatory cache enabled')
                require(not p.automatic_admission_mutation_enabled,'automatic admission mutation enabled')
                require(not p.automatic_model_routing_enabled,'automatic routing enabled')
    print('Stage 7C structural validation: PASSED')
    return 0
if __name__=='__main__': raise SystemExit(main())
