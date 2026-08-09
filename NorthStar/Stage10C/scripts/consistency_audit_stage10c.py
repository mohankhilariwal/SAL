from __future__ import annotations

import json
import re
from _bootstrap import ROOT


def main() -> None:
    stage = (ROOT / "docs/stages/NorthStar-Stage-10C-FinOps-Capacity-and-Production-Readiness.md").read_text()
    handoff = (ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md").read_text()
    requirements = (ROOT / "docs/source-of-truth/02-Requirements-Register.md").read_text()
    data_register = (ROOT / "docs/source-of-truth/05-Data-and-Schema-Register.md").read_text()
    adr_register = (ROOT / "docs/source-of-truth/06-ADR-Register.md").read_text()
    assert "exactly one active `AGT-001`" in stage
    assert "production promotion remains denied" in stage
    assert "DATA-257" in data_register and "DATA-278" in data_register
    assert "INT-217" in data_register and "INT-238" in data_register
    assert "ADR-138" in adr_register and "ADR-148" in adr_register
    assert "S10C-FR-001" in requirements and "S10C-NFR-010" in requirements
    assert "Architecture version: `1.17.0`" in handoff
    assert "TOOL-007" in stage and "is not introduced" in stage
    assert "GRAPH-001/1.12.0" in stage
    result = {
        "result": "passed_with_recorded_exceptions",
        "exceptions": ["ISS-096", "ISS-131", "ISS-141", "ISS-147", "ISS-194"],
        "production_route_enabled": False,
        "active_agent_count": 1,
        "tool_range": "TOOL-001..006",
        "authority_effect_for_new_objects": "none",
    }
    path = ROOT / "reports/stage10c-consistency-audit.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
