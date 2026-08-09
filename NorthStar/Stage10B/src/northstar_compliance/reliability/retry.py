from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from .models import EffectClass, FailureClass, FailureEnvelope, RetryPolicy

T = TypeVar("T")


class RetryExhausted(RuntimeError):
    pass


class UnsafeRetry(RuntimeError):
    pass


@dataclass(frozen=True)
class AttemptResult(Generic[T]):
    value: T
    attempts: int


class RetryExecutor:
    """Budgeted exponential backoff with full jitter.

    The executor retries only an explicitly classified transient failure. It never
    retries authorization, policy, security, audit, data-integrity, or ambiguous
    protected-write failures. It does not change authority.
    """

    def __init__(
        self,
        *,
        sleep: Callable[[float], None] = time.sleep,
        random_value: Callable[[], float] = random.random,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self._sleep = sleep
        self._random = random_value
        self._monotonic = monotonic

    def execute(
        self,
        operation: Callable[[], T],
        *,
        policy: RetryPolicy,
        effect_class: EffectClass,
        idempotency_key: str | None,
        classify: Callable[[Exception], FailureEnvelope],
    ) -> AttemptResult[T]:
        if (
            effect_class is not EffectClass.READ_ONLY
            and policy.require_idempotency_for_writes
            and not idempotency_key
        ):
            raise UnsafeRetry("write retry requires an idempotency key")

        start = self._monotonic()
        last_error: Exception | None = None
        for attempt in range(1, policy.max_attempts + 1):
            try:
                return AttemptResult(operation(), attempt)
            except Exception as exc:  # caller supplies deterministic classification
                last_error = exc
                failure = classify(exc)
                prohibited = {
                    FailureClass.AUTHENTICATION,
                    FailureClass.AUTHORIZATION,
                    FailureClass.POLICY,
                    FailureClass.SECURITY,
                    FailureClass.DATA_INTEGRITY,
                    FailureClass.AUDIT,
                    FailureClass.CONFIGURATION,
                    FailureClass.PERMANENT,
                }
                if failure.failure_class in prohibited:
                    raise
                if failure.ambiguous and effect_class is EffectClass.PROTECTED_WRITE:
                    raise UnsafeRetry("ambiguous protected outcome requires reconciliation") from exc
                if not failure.retryable or failure.failure_class not in policy.retryable_classes:
                    raise
                if attempt >= policy.max_attempts:
                    break

                elapsed = self._monotonic() - start
                cap = min(policy.max_delay_seconds, policy.base_delay_seconds * (2 ** (attempt - 1)))
                delay = self._random() * cap
                if elapsed + delay > policy.total_budget_seconds:
                    break
                self._sleep(delay)

        raise RetryExhausted(f"retry budget exhausted after {policy.max_attempts} attempts") from last_error
