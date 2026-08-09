from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    demo = json.loads((ROOT / "reports/stage11-demo.json").read_text())
    gates = {
        "EVAL-273": demo["decision"] == "denied",
        "EVAL-274": demo["production_route_enabled"] is False,
        "EVAL-275": demo["active_agent_count"] == 1,
        "EVAL-276": demo["selected_topology"] == "one_agent_specialized_graph_profiles",
        "EVAL-277": demo["hard_blocker_count"] >= 1,
        "EVAL-278": demo["authority_effect"] == "none",
        "EVAL-279": (ROOT / "docs/architecture/diagrams/cumulative-logical-architecture.mmd").exists(),
        "EVAL-280": (ROOT / "docs/threat-model-final-summary.md").exists(),
        "EVAL-281": (ROOT / "docs/evaluation-final-summary.md").exists(),
        "EVAL-282": (ROOT / "docs/runbooks/final-operating-runbook-index.md").exists(),
        "EVAL-283": (ROOT / "docs/certification-assignment.md").exists(),
        "EVAL-284": (ROOT / "docs/references/stage11-annotated-bibliography.md").exists(),
    }
    if not all(gates.values()):
        raise SystemExit(json.dumps(gates, indent=2))
    (ROOT / "reports/stage11-evaluation-gates.json").write_text(json.dumps(gates, indent=2))
    print(f"{sum(gates.values())}/{len(gates)} evaluation gates passed")


if __name__ == "__main__":
    main()
