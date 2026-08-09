import time

from northstar_compliance.reliability.recovery import RecoveryPlanner
from northstar_compliance.reliability.models import EffectClass, FailureClass, FailureEnvelope


def test_recovery_decision_local_latency_guard():
    planner = RecoveryPlanner(); f = FailureEnvelope("F", "C", "o", FailureClass.TRANSIENT, EffectClass.READ_ONLY, True)
    start = time.perf_counter()
    for _ in range(10000): planner.decide(f)
    assert time.perf_counter() - start < 1.0
