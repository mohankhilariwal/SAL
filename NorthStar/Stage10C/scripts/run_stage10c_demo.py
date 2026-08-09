from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from _bootstrap import ROOT
from northstar_compliance.capacity.models import WorkloadDemandProfile
from northstar_compliance.capacity.planner import CapacityPlanner
from northstar_compliance.capacity.slo import SLIKind, SLIObservation, SLOProposal, evaluate_error_budget
from northstar_compliance.finops.budget import BudgetEvaluator, BudgetPolicy
from northstar_compliance.finops.costing import CostCalculator, RateCard, failed_run_cost, retry_cost
from northstar_compliance.finops.models import CostCategory, CostEvent, CostRate
from northstar_compliance.readiness.evaluator import ProductionReadinessEvaluator
from northstar_compliance.readiness.models import GateStatus, ProductionReadinessEvidence, ReadinessGate


def load_rate_card() -> RateCard:
    data = json.loads((ROOT / "config/finops/rate-card.example.json").read_text())
    return RateCard(CostRate(CostCategory(item["category"]), Decimal(item["rate"]), item["unit"]) for item in data["rates"])


def main() -> None:
    calculator = CostCalculator(load_rate_card())
    events = [
        CostEvent("RUN-1", "REQ-1", CostCategory.MODEL_INPUT, Decimal("16000"), "token", "WP-001", "Payments", "CA", "preprod", "CASE-1", True),
        CostEvent("RUN-1", "REQ-1", CostCategory.MODEL_OUTPUT, Decimal("2200"), "token", "WP-001", "Payments", "CA", "preprod", "CASE-1", True),
        CostEvent("RUN-1", "REQ-1", CostCategory.TOOL, Decimal("3"), "call", "WP-001", "Payments", "CA", "preprod", "CASE-1", True),
        CostEvent("RUN-2", "REQ-2", CostCategory.MODEL_INPUT, Decimal("9000"), "token", "WP-001", "Lending", "US", "preprod", "CASE-2", False, retry=True),
        CostEvent("RUN-2", "REQ-2", CostCategory.RECOVERY, Decimal("4"), "minute", "WP-001", "Lending", "US", "preprod", "CASE-2", False, recovered=True),
        CostEvent("RUN-3", "REQ-3", CostCategory.HUMAN_REVIEW, Decimal("12"), "minute", "WP-003", "Payments", "CA", "preprod", "CASE-3", True),
        CostEvent("RUN-3", "REQ-3", CostCategory.OBSERVABILITY, Decimal("0.02"), "gb", "WP-003", "Payments", "CA", "preprod", "CASE-3", True),
        CostEvent("RUN-3", "REQ-3", CostCategory.EVALUATION, Decimal("2"), "case", "WP-003", "Payments", "CA", "preprod", "CASE-3", True),
    ]
    report = calculator.report(events, completed_task_ids=["RUN-1", "RUN-3"], document_ids=["DOC-1", "DOC-2"], human_escalation_ids=["CASE-3"])
    profile = WorkloadDemandProfile("WP-001", Decimal("0.20"), Decimal("3"), Decimal("45"), 4, Decimal("0.65"), 16000, 2200, Decimal("0.05"), Decimal("60"))
    envelope = CapacityPlanner().estimate(profile)
    proposal = SLOProposal("SLO-PROP-002", "known disposition", SLIKind.KNOWN_DISPOSITION, Decimal("0.999"), 30)
    error_budget = evaluate_error_budget(proposal, SLIObservation(10000, 9992, 0))
    budget = BudgetEvaluator().evaluate(BudgetPolicy(Decimal("25"), Decimal("40")), report.total_cost, Decimal("5"), protected_effect_in_progress=False)
    gates = tuple(ReadinessGate(f"PRG-{i}", name, True, GateStatus.FAIL, owner=owner) for i, (name, owner) in enumerate([
        ("Stage 8D unresolved", "Sofia Alvarez"), ("Stage 9D unresolved", "Priya Raman"), ("production route disabled", "Liam O'Connor")
    ], start=1))
    readiness = ProductionReadinessEvaluator().evaluate(ProductionReadinessEvidence("1.17.0", "1.17.0", "GRAPH-001/1.12.0", "AGT-001/1.1.0", gates, False, False, False))
    output = {
        "currency": report.currency,
        "total_cost": str(report.total_cost),
        "cost_per_request": str(report.cost_per_request),
        "cost_per_completed_task": str(report.cost_per_completed_task),
        "failed_run_cost": str(failed_run_cost(events, calculator)),
        "retry_cost": str(retry_cost(events, calculator)),
        "capacity": {"required_workers": envelope.required_workers, "peak_rps": str(envelope.peak_rps), "protected_write_limit": envelope.protected_write_concurrency_limit},
        "error_budget": {"allowed_bad_events": str(error_budget.allowed_bad_events), "observed_bad_events": error_budget.observed_bad_events, "exhausted": error_budget.exhausted, "control_gate_passed": error_budget.control_gate_passed},
        "budget_action": budget.action,
        "production_readiness": readiness.decision,
        "failed_hard_gates": readiness.failed_hard_gates,
        "authority_effect": "none",
    }
    path = ROOT / "reports/stage10c-demo-output.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2, default=str) + "\n")
    print(json.dumps(output, indent=2, default=str))

if __name__ == "__main__":
    main()
