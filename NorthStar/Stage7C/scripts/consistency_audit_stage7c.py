#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]

def main()->int:
    stage=(ROOT/'docs/stages/NorthStar-Stage-7C-Inference-Optimization-and-Speculative-Decoding.md').read_text()
    handoff=(ROOT/'docs/source-of-truth/09-Stage-Handoff-Pack.md').read_text()
    graph=(ROOT/'docs/architecture/diagrams/GRAPH-001-v1.4.0.mmd').read_text()
    errors=[]
    checks={
        'stage begins with context': '## 1. Context Carried Forward' in stage,
        'version 1.8.0': all('1.8.0' in text for text in (stage,handoff)),
        'graph 1.4.0': all('GRAPH-001/1.4.0' in text for text in (stage,handoff)),
        'one active agent claim': 'only active agent' in (stage+' '+handoff).lower(),
        'wp008 inactive': 'WP-008' in stage and 'inactive_future' in stage,
        'semantic cache prohibited': 'semantic caching of regulatory conclusions is prohibited' in (stage+' '+handoff),
        'advisory no admission': 'cannot mutate `DATA-106`' in (stage+' '+handoff),
        'new data ids': all(f'DATA-{i}' in stage for i in range(122,131)),
        'new interface ids': all(f'INT-{i:03d}' in stage for i in range(94,103)),
        'new ADR ids': all(f'ADR-{i:03d}' in stage for i in range(67,72)),
        'test range': 'TEST-450' in stage and ('TEST-507' in stage or '`507`' in stage),
        'evaluation range': 'EVAL-101' in stage and 'EVAL-115' in stage,
        'graph components preserved': all(f'CMP-{i:03d}' in graph for i in range(1,12)),
        'no future model selection claimed': 'No managed provider or target model is selected' in stage,
        'production disclaimer': 'not a production speedup' in stage.lower() or 'not an endpoint benchmark' in stage.lower(),
    }
    errors=[name for name,ok in checks.items() if not ok]
    if re.search(r'AGT-00[2-9].*active',stage,re.I): errors.append('unexpected additional active agent')
    if errors:
        print('Stage 7C consistency audit: FAILED')
        for error in errors: print('-',error)
        return 2
    print('Stage 7C consistency audit: PASSED WITH RECORDED EXCEPTIONS ISS-096, ISS-105..113')
    for name in checks: print('-',name)
    return 0
if __name__=='__main__': raise SystemExit(main())
