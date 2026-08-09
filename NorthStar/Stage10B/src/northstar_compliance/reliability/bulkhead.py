from __future__ import annotations

from contextlib import contextmanager
from threading import BoundedSemaphore
from typing import Iterator


class BulkheadRejected(RuntimeError):
    pass


class Bulkhead:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._semaphore = BoundedSemaphore(capacity)

    @contextmanager
    def permit(self, timeout_seconds: float = 0.0) -> Iterator[None]:
        acquired = self._semaphore.acquire(timeout=timeout_seconds)
        if not acquired:
            raise BulkheadRejected("bulkhead capacity exhausted")
        try:
            yield
        finally:
            self._semaphore.release()
