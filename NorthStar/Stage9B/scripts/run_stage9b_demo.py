from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
import json
from northstar_compliance.security.identity.demo import build_demo
from northstar_compliance.security.identity.canonical import _normalize
out=build_demo()
p=Path("reports/stage9b-demo.json")
p.parent.mkdir(exist_ok=True)
p.write_text(json.dumps(_normalize(out),indent=2,sort_keys=True)+"\n")
print(json.dumps(_normalize(out),indent=2,sort_keys=True))
