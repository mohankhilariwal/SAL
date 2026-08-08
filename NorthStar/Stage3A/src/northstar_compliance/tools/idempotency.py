from __future__ import annotations

from dataclasses import dataclass
from threading import Lock

from .models import ToolResultEnvelope


@dataclass(frozen=True)
class IdempotencyRecord:
    arguments_sha256: str
    result: ToolResultEnvelope


class InMemoryIdempotencyStore:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str, str, str], IdempotencyRecord] = {}
        self._lock = Lock()

    def get(
        self, principal_id: str, tool_id: str, version: str, key: str
    ) -> IdempotencyRecord | None:
        with self._lock:
            return self._records.get((principal_id, tool_id, version, key))

    def put(
        self,
        principal_id: str,
        tool_id: str,
        version: str,
        key: str,
        record: IdempotencyRecord,
    ) -> None:
        with self._lock:
            self._records[(principal_id, tool_id, version, key)] = record
