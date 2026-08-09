from __future__ import annotations

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
required = [
    root / "config/reliability/failure-taxonomy.json",
    root / "src/northstar_compliance/reliability/recovery.py",
    root / "deployment/kubernetes/deployment-reference.yaml",
    root / "docs/source-of-truth/09-Stage-Handoff-Pack.md",
]
problems = [str(path.relative_to(root)) for path in required if not path.exists()]
settings = json.loads((root / "config/deployment/environments.json").read_text())
if settings["production"]["enabled"] is not False:
    problems.append("production route unexpectedly enabled")
if problems:
    raise SystemExit("consistency audit failed: " + ", ".join(problems))
print("Stage 10B consistency audit passed with recorded historical-merge exception")
