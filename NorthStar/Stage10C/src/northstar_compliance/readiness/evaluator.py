from __future__ import annotations

from .models import (
    GateStatus,
    ProductionReadinessDecision,
    ProductionReadinessEvidence,
    ReadinessDecisionValue,
)


class ProductionReadinessEvaluator:
    def evaluate(self, evidence: ProductionReadinessEvidence) -> ProductionReadinessDecision:
        failed = [gate.gate_id for gate in evidence.gates if gate.hard_blocker and gate.status != GateStatus.PASS]
        reasons: list[str] = []
        if not evidence.stage8d_resolved:
            failed.append("BLOCKER-STAGE-8D")
            reasons.append("Stage 8D deployment metrics, regression baselines and eligibility gates remain unresolved")
        if not evidence.stage9d_resolved:
            failed.append("BLOCKER-STAGE-9D")
            reasons.append("Stage 9D enterprise control-plane implementation remains unresolved")
        if not evidence.production_route_enabled:
            failed.append("BLOCKER-PRODUCTION-ROUTE-DISABLED")
            reasons.append("production route activation remains disabled")
        failed = list(dict.fromkeys(failed))
        if failed:
            return ProductionReadinessDecision(
                decision=ReadinessDecisionValue.DENIED,
                reasons=tuple(reasons or ["one or more hard readiness gates failed"]),
                failed_hard_gates=tuple(failed),
                production_route_enabled=False,
            )
        return ProductionReadinessDecision(
            decision=ReadinessDecisionValue.EVIDENCE_COMPLETE_BUT_BLOCKED,
            reasons=("Stage 10C never activates production; a separately governed release decision is required",),
            failed_hard_gates=(),
            production_route_enabled=False,
        )
