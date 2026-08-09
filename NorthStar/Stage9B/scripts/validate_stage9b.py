from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
import json
required=["docs/source-of-truth/00-Project-Constitution.md","docs/source-of-truth/09-Stage-Handoff-Pack.md","docs/stages/NorthStar-Stage-9B-Identity-Authorization-and-Blast-Radius-Controls.md","config/identity/authorization_policy.json","config/identity/blast_radius_policy.json"]
errors=[p for p in required if not (ROOT/p).exists()]
for schema in (ROOT/"schemas").glob("*.schema.json"):
    json.loads(schema.read_text())
if errors: raise SystemExit("missing: "+", ".join(errors))
print(f"validated {len(required)} required files and {len(list((ROOT/'schemas').glob('*.schema.json')))} schemas")
