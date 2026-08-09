from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    required = [
        "docs/source-of-truth/00-Project-Constitution.md",
        "docs/source-of-truth/01-Business-and-User-Story-Baseline.md",
        "docs/source-of-truth/02-Requirements-Register.md",
        "docs/source-of-truth/03-Architecture-Baseline.md",
        "docs/source-of-truth/04-Component-and-Agent-Catalogue.md",
        "docs/source-of-truth/05-Data-and-Schema-Register.md",
        "docs/source-of-truth/06-ADR-Register.md",
        "docs/source-of-truth/07-Repository-Manifest.md",
        "docs/source-of-truth/08-Risk-Assumption-and-Issue-Register.md",
        "docs/source-of-truth/09-Stage-Handoff-Pack.md",
        "docs/stages/NorthStar-Stage-11-Final-Capstone.md",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    if missing:
        raise SystemExit(f"missing required files: {missing}")

    schemas = sorted((ROOT / "schemas").glob("DATA-*.schema.json"))
    if len(schemas) != 12:
        raise SystemExit(f"expected 12 schemas, got {len(schemas)}")
    for path in schemas:
        data = json.loads(path.read_text())
        assert data["properties"]["authority_effect"]["const"] == "none"

    assessment = json.loads((ROOT / "config/capstone/final-assessment.json").read_text())
    assert assessment["production_route_enabled"] is False
    assert assessment["active_agent_count"] == 1
    assert assessment["selected_topology"] == "one_agent_specialized_graph_profiles"
    print("STAGE11 VALIDATION PASSED WITH RECORDED HISTORICAL-MERGE AND PRODUCTION-EVIDENCE EXCEPTIONS")


if __name__ == "__main__":
    main()
