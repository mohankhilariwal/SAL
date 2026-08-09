from __future__ import annotations

import time
from dataclasses import dataclass
from enum import StrEnum
from threading import Lock
from typing import Callable


class CircuitState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpen(RuntimeError):
    pass


@dataclass(frozen=True)
class CircuitBreakerPolicy:
    failure_threshold: int = 5
    recovery_timeout_seconds: float = 30.0
    half_open_max_calls: int = 1


class CircuitBreaker:
    def __init__(self, policy: CircuitBreakerPolicy, monotonic: Callable[[], float] = time.monotonic) -> None:
        self.policy = policy
        self._monotonic = monotonic
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._opened_at = 0.0
        self._half_open_inflight = 0
        self._lock = Lock()

    @property
    def state(self) -> CircuitState:
        return self._state

    def allow(self) -> None:
        with self._lock:
            now = self._monotonic()
            if self._state is CircuitState.OPEN:
                if now - self._opened_at < self.policy.recovery_timeout_seconds:
                    raise CircuitOpen("dependency circuit is open")
                self._state = CircuitState.HALF_OPEN
                self._half_open_inflight = 0
            if self._state is CircuitState.HALF_OPEN:
                if self._half_open_inflight >= self.policy.half_open_max_calls:
                    raise CircuitOpen("half-open probe already in flight")
                self._half_open_inflight += 1

    def record_success(self) -> None:
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failures = 0
            self._half_open_inflight = 0

    def record_failure(self) -> None:
        with self._lock:
            if self._state is CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN
                self._opened_at = self._monotonic()
                self._half_open_inflight = 0
                return
            self._failures += 1
            if self._failures >= self.policy.failure_threshold:
                self._state = CircuitState.OPEN
                self._opened_at = self._monotonic()
