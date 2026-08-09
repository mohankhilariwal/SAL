import pytest

from northstar_compliance.reliability.models import EffectClass, FailureClass, FailureEnvelope, RetryPolicy
from northstar_compliance.reliability.retry import RetryExecutor, RetryExhausted, UnsafeRetry


def policy(max_attempts=3):
    return RetryPolicy("RP-1", max_attempts, 0.1, 1.0, 10.0, frozenset({FailureClass.TRANSIENT}))


def classify(fc=FailureClass.TRANSIENT, retryable=True, ambiguous=False):
    return lambda exc: FailureEnvelope("F", "CMP-004", "read", fc, EffectClass.READ_ONLY, retryable, ambiguous)


def test_success_first_attempt():
    result = RetryExecutor(sleep=lambda _: None).execute(lambda: 7, policy=policy(), effect_class=EffectClass.READ_ONLY, idempotency_key=None, classify=classify())
    assert result.value == 7 and result.attempts == 1


def test_transient_retry_then_success():
    calls = {"n": 0}
    def op():
        calls["n"] += 1
        if calls["n"] < 3:
            raise TimeoutError()
        return "ok"
    result = RetryExecutor(sleep=lambda _: None, random_value=lambda: 0).execute(op, policy=policy(), effect_class=EffectClass.READ_ONLY, idempotency_key=None, classify=classify())
    assert result.value == "ok" and result.attempts == 3


def test_exhaustion():
    with pytest.raises(RetryExhausted):
        RetryExecutor(sleep=lambda _: None, random_value=lambda: 0).execute(lambda: (_ for _ in ()).throw(TimeoutError()), policy=policy(2), effect_class=EffectClass.READ_ONLY, idempotency_key=None, classify=classify())

@pytest.mark.parametrize("failure_class", [
    FailureClass.AUTHENTICATION, FailureClass.AUTHORIZATION, FailureClass.POLICY,
    FailureClass.SECURITY, FailureClass.DATA_INTEGRITY, FailureClass.AUDIT,
    FailureClass.CONFIGURATION, FailureClass.PERMANENT,
])
def test_prohibited_classes_are_not_retried(failure_class):
    calls = {"n": 0}
    def op():
        calls["n"] += 1
        raise RuntimeError("x")
    with pytest.raises(RuntimeError):
        RetryExecutor(sleep=lambda _: None).execute(op, policy=policy(), effect_class=EffectClass.READ_ONLY, idempotency_key=None, classify=classify(failure_class))
    assert calls["n"] == 1


def test_write_requires_idempotency_key():
    with pytest.raises(UnsafeRetry):
        RetryExecutor().execute(lambda: 1, policy=policy(), effect_class=EffectClass.REVERSIBLE_WRITE, idempotency_key=None, classify=classify())


def test_ambiguous_protected_write_is_not_retried():
    with pytest.raises(UnsafeRetry):
        RetryExecutor(sleep=lambda _: None).execute(lambda: (_ for _ in ()).throw(TimeoutError()), policy=policy(), effect_class=EffectClass.PROTECTED_WRITE, idempotency_key="K", classify=classify(FailureClass.AMBIGUOUS_OUTCOME, retryable=True, ambiguous=True))
