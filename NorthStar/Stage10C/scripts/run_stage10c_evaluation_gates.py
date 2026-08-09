from __future__ import annotations

import json
from _bootstrap import ROOT
from northstar_compliance.readiness.evaluator import ProductionReadinessEvaluator
from northstar_compliance.readiness.models import GateStatus, ProductionReadinessEvidence, ReadinessGate


def main() -> None:
    config = json.loads((ROOT / "config/readiness/production-readiness-gates.json").read_text())
    gates = tuple(ReadinessGate(g["gate_id"], g["name"], g["hard_blocker"], GateStatus(g["status"]), owner=g.get("owner")) for g in config["gates"])
    evidence = ProductionReadinessEvidence("1.17.0", "1.17.0", "GRAPH-001/1.12.0", "AGT-001/1.1.0", gates, config["production_route_enabled"], config["stage8d_resolved"], config["stage9d_resolved"])
    decision = ProductionReadinessEvaluator().evaluate(evidence)
    result = {"decision": decision.decision, "failed_hard_gates": decision.failed_hard_gates, "production_route_enabled": decision.production_route_enabled, "authority_effect": decision.authority_effect}
    path = ROOT / "reports/stage10c-evaluation-gates.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, default=str) + "\n")
    assert str(decision.decision) == "denied"
    assert decision.production_route_enabled is False
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()
