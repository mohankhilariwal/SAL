from northstar_compliance.readiness.evaluator import ProductionReadinessEvaluator
from northstar_compliance.readiness.models import GateStatus, ProductionReadinessEvidence, ReadinessGate, ReadinessDecisionValue


def evidence(route=False, s8=False, s9=False, gate=GateStatus.PASS):
    return ProductionReadinessEvidence("1.17.0","1.17.0","GRAPH-001/1.12.0","AGT-001/1.1.0",(ReadinessGate("G1","gate",True,gate),),route,s8,s9)

def test_1043_stage8d_blocks_production(): assert "BLOCKER-STAGE-8D" in ProductionReadinessEvaluator().evaluate(evidence()).failed_hard_gates

def test_1044_stage9d_blocks_production(): assert "BLOCKER-STAGE-9D" in ProductionReadinessEvaluator().evaluate(evidence()).failed_hard_gates

def test_1045_disabled_route_blocks_production(): assert "BLOCKER-PRODUCTION-ROUTE-DISABLED" in ProductionReadinessEvaluator().evaluate(evidence()).failed_hard_gates

def test_1046_failed_gate_blocks_production(): assert "G1" in ProductionReadinessEvaluator().evaluate(evidence(route=True,s8=True,s9=True,gate=GateStatus.FAIL)).failed_hard_gates

def test_1047_evaluator_never_enables_route(): assert not ProductionReadinessEvaluator().evaluate(evidence(route=True,s8=True,s9=True)).production_route_enabled

def test_1048_readiness_decision_has_no_authority(): assert ProductionReadinessEvaluator().evaluate(evidence()).authority_effect == "none"
