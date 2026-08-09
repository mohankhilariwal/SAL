from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
report = json.loads((ROOT / "reports/stage8c-bias-lab.json").read_text())
required = [
    ROOT / "docs/stages/NorthStar-Stage-8C-Judge-Bias-Laboratory.md",
    ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md",
    ROOT / "docs/architecture/diagrams/GRAPH-001-v1.7.0.mmd",
]
assert all(p.exists() for p in required)
assert report["authority_effect"] == "none"
assert report["model_route_activated"] is False
assert report["live_model_called"] is False
all_text = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "docs/source-of-truth").glob("*.md"))
for token in ["AGT-001", "CMP-003", "CMP-005", "CMP-006", "CMP-007", "CMP-008", "DATA-155", "DATA-164", "INT-121", "INT-129", "ADR-083", "ADR-088"]:
    assert token in all_text, token
assert all_text.count("only active agent") >= 1
print("PASSED WITH RECORDED EXCEPTIONS: ISS-096, ISS-114-139")
