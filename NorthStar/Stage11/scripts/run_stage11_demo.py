from __future__ import annotations

import json
from pathlib import Path

from northstar_compliance.capstone import Blocker, EvidenceItem, FinalReadinessAssessor, compare_topologies, reconcile_evidence

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    index = json.loads((ROOT / "config/capstone/evidence-index.json").read_text())
    assessment_cfg = json.loads((ROOT / "config/capstone/final-assessment.json").read_text())
    items = [EvidenceItem(**item) for item in index["items"]]
    blockers = [Blocker(**item) for item in assessment_cfg["blockers"]]
    reconciliation = reconcile_evidence(items, index["required_evidence"])
    assessment = FinalReadinessAssessor().evaluate(items, blockers)
    comparison = compare_topologies(
        measured_quality_gain=None,
        handoff_error_rate=None,
        representative_evidence=False,
        independent_authority_boundary=False,
        independent_fault_domain=False,
    )
    report = {
        "reconciliation_complete": reconciliation.complete,
        "decision": assessment.decision,
        "production_route_enabled": assessment.production_route_enabled,
        "hard_blocker_count": len(assessment.hard_blockers),
        "soft_gap_count": len(assessment.soft_gaps),
        "selected_topology": comparison.selected_topology,
        "active_agent_count": assessment.active_agent_count,
        "authority_effect": assessment.authority_effect,
    }
    (ROOT / "reports/stage11-demo.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
