import pytest

from northstar_compliance.reliability.models import EffectClass, FailureClass, FailureEnvelope, RecoveryAction
from northstar_compliance.reliability.recovery import RecoveryPlanner


def failure(fc, *, retryable=False, ambiguous=False, effect=EffectClass.READ_ONLY):
    return FailureEnvelope("F", "CMP-X", "op", fc, effect, retryable, ambiguous)

@pytest.mark.parametrize("fc", [FailureClass.AUTHORIZATION, FailureClass.POLICY, FailureClass.SECURITY, FailureClass.AUDIT])
def test_fail_closed_classes(fc):
    assert RecoveryPlanner().decide(failure(fc)).action is RecoveryAction.FAIL_CLOSED


def test_authentication_requires_fresh_grant():
    d = RecoveryPlanner().decide(failure(FailureClass.AUTHENTICATION))
    assert d.action is RecoveryAction.STOP and d.requires_reauthorization


def test_data_integrity_quarantines():
    assert RecoveryPlanner().decide(failure(FailureClass.DATA_INTEGRITY)).action is RecoveryAction.QUARANTINE


def test_human_timeout_escalates_not_approves():
    d = RecoveryPlanner().decide(failure(FailureClass.HUMAN_TIMEOUT))
    assert d.action is RecoveryAction.ESCALATE_HUMAN and d.requires_human


def test_overload_sheds_load():
    assert RecoveryPlanner().decide(failure(FailureClass.OVERLOAD)).action is RecoveryAction.SHED_LOAD


def test_ambiguous_reconciles():
    d = RecoveryPlanner().decide(failure(FailureClass.AMBIGUOUS_OUTCOME, ambiguous=True, effect=EffectClass.PROTECTED_WRITE))
    assert d.action is RecoveryAction.RECONCILE and d.requires_reconciliation


def test_transient_retries():
    d = RecoveryPlanner().decide(failure(FailureClass.TRANSIENT, retryable=True))
    assert d.action is RecoveryAction.RETRY and d.may_retry


def test_permanent_dead_letters():
    assert RecoveryPlanner().decide(failure(FailureClass.PERMANENT)).action is RecoveryAction.DEAD_LETTER
