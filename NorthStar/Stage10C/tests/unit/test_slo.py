from decimal import Decimal
from northstar_compliance.capacity.slo import SLIKind, SLIObservation, SLOProposal, evaluate_error_budget


def proposal(): return SLOProposal("S1","known disposition",SLIKind.KNOWN_DISPOSITION,Decimal("0.99"),30)

def test_1037_error_budget_calculated():
    r=evaluate_error_budget(proposal(),SLIObservation(1000,995)); assert r.allowed_bad_events==Decimal("10.00") and not r.exhausted

def test_1038_error_budget_exhausted(): assert evaluate_error_budget(proposal(),SLIObservation(1000,980)).exhausted

def test_1039_control_violation_has_zero_tolerance(): assert not evaluate_error_budget(proposal(),SLIObservation(1000,1000,1)).control_gate_passed

def test_1040_slo_is_proposed_not_approved(): assert proposal().approved is False
