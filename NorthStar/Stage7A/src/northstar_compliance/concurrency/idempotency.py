"""In-memory idempotency and duplicate-suppression reference store."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

from .errors import IdempotencyConflict


@dataclass(slots=True)
class _Entry:
    input_digest: str
    event: asyncio.Event = field(default_factory=asyncio.Event)
    state: str = "running"
    output: Any = None
    error: BaseException | None = None


class InMemoryIdempotencyStore:
    """Coordinates same-key calls inside one reference runtime.

    Production migration replaces this with a transactional, durable store.
    The store does not claim exactly-once side effects.
    """

    def __init__(self) -> None:
        self._entries: dict[str, _Entry] = {}
        self._lock = asyncio.Lock()

    async def execute_once(
        self,
        key: str,
        input_digest: str,
        producer: Callable[[], Awaitable[Any]],
    ) -> tuple[Any, bool]:
        async with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                entry = _Entry(input_digest=input_digest)
                self._entries[key] = entry
                owner = True
            else:
                if entry.input_digest != input_digest:
                    raise IdempotencyConflict(
                        "idempotency key reused for a different canonical input digest"
                    )
                owner = False

        if owner:
            try:
                output = await producer()
            except BaseException as exc:
                async with self._lock:
                    entry.state = "failed"
                    entry.error = exc
                    entry.event.set()
                raise
            else:
                async with self._lock:
                    entry.state = "succeeded"
                    entry.output = output
                    entry.event.set()
                return output, False

        await entry.event.wait()
        if entry.state == "succeeded":
            return entry.output, True
        assert entry.error is not None
        raise entry.error

    async def snapshot(self) -> dict[str, dict[str, Any]]:
        async with self._lock:
            return {
                key: {
                    "input_digest": entry.input_digest,
                    "state": entry.state,
                    "has_output": entry.output is not None,
                    "error_type": type(entry.error).__name__ if entry.error else None,
                }
                for key, entry in self._entries.items()
            }
