from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass
from threading import Lock


class RateLimitExceeded(RuntimeError):
    pass


class CircuitOpen(RuntimeError):
    pass


class SlidingWindowRateLimiter:
    def __init__(self, limit: int = 20, window_seconds: float = 60.0) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._hits: dict[tuple[str, str], deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, principal_id: str, tool_id: str) -> None:
        now = time.monotonic()
        key = (principal_id, tool_id)
        with self._lock:
            hits = self._hits[key]
            while hits and now - hits[0] > self.window_seconds:
                hits.popleft()
            if len(hits) >= self.limit:
                raise RateLimitExceeded(f"rate limit exceeded for {principal_id}/{tool_id}")
            hits.append(now)


@dataclass
class CircuitState:
    failures: int = 0
    opened_at: float | None = None


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_seconds: float = 30.0) -> None:
        self.failure_threshold = failure_threshold
        self.reset_seconds = reset_seconds
        self._states: dict[str, CircuitState] = defaultdict(CircuitState)
        self._lock = Lock()

    def before_call(self, tool_id: str) -> None:
        now = time.monotonic()
        with self._lock:
            state = self._states[tool_id]
            if state.opened_at is None:
                return
            if now - state.opened_at >= self.reset_seconds:
                state.failures = 0
                state.opened_at = None
                return
            raise CircuitOpen(f"circuit open for {tool_id}")

    def record_success(self, tool_id: str) -> None:
        with self._lock:
            self._states[tool_id] = CircuitState()

    def record_failure(self, tool_id: str) -> None:
        now = time.monotonic()
        with self._lock:
            state = self._states[tool_id]
            state.failures += 1
            if state.failures >= self.failure_threshold:
                state.opened_at = now
