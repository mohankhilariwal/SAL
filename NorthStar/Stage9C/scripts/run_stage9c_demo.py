from __future__ import annotations
import json
from pathlib import Path
from northstar_compliance.guardrails.demo import run_demo
ROOT=Path(__file__).resolve().parents[1]
results=run_demo(ROOT)
path=ROOT/'reports/stage9c-demo.json'
path.write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
