import pytest

from northstar_compliance.reliability.bulkhead import Bulkhead, BulkheadRejected
from northstar_compliance.reliability.circuit_breaker import CircuitBreaker, CircuitBreakerPolicy, CircuitOpen, CircuitState


def test_circuit_opens_at_threshold():
    clock = [0.0]
    cb = CircuitBreaker(CircuitBreakerPolicy(2, 10, 1), monotonic=lambda: clock[0])
    cb.record_failure(); cb.record_failure()
    assert cb.state is CircuitState.OPEN
    with pytest.raises(CircuitOpen): cb.allow()


def test_circuit_half_open_then_closes():
    clock = [0.0]
    cb = CircuitBreaker(CircuitBreakerPolicy(1, 10, 1), monotonic=lambda: clock[0])
    cb.record_failure(); clock[0] = 11
    cb.allow()
    assert cb.state is CircuitState.HALF_OPEN
    cb.record_success()
    assert cb.state is CircuitState.CLOSED


def test_half_open_limits_probe():
    clock = [0.0]
    cb = CircuitBreaker(CircuitBreakerPolicy(1, 1, 1), monotonic=lambda: clock[0])
    cb.record_failure(); clock[0] = 2; cb.allow()
    with pytest.raises(CircuitOpen): cb.allow()


def test_half_open_failure_reopens():
    clock = [0.0]
    cb = CircuitBreaker(CircuitBreakerPolicy(1, 1, 1), monotonic=lambda: clock[0])
    cb.record_failure(); clock[0] = 2; cb.allow(); cb.record_failure()
    assert cb.state is CircuitState.OPEN


def test_bulkhead_rejects_when_full():
    b = Bulkhead(1)
    with b.permit():
        with pytest.raises(BulkheadRejected):
            with b.permit(0): pass


def test_bulkhead_releases_permit():
    b = Bulkhead(1)
    with b.permit(): pass
    with b.permit(): pass


def test_bulkhead_requires_positive_capacity():
    with pytest.raises(ValueError): Bulkhead(0)
