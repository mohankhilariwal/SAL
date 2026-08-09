from __future__ import annotations
from threading import Lock
from datetime import datetime, timezone


class RevocationLedger:
    def __init__(self):
        self._revoked: dict[str, tuple[datetime,str]] = {}
        self._lock = Lock()
    def revoke(self, grant_id: str, reason: str, now: datetime | None = None) -> None:
        with self._lock:
            self._revoked[grant_id] = (now or datetime.now(timezone.utc), reason)
    def is_revoked(self, grant_id: str) -> bool:
        with self._lock:
            return grant_id in self._revoked


class UseLedger:
    def __init__(self):
        self._uses: dict[str,int] = {}
        self._lock = Lock()
    def consume(self, grant_id: str, max_uses: int) -> bool:
        with self._lock:
            current = self._uses.get(grant_id, 0)
            if current >= max_uses:
                return False
            self._uses[grant_id] = current + 1
            return True
    def used(self, grant_id: str) -> int:
        with self._lock:
            return self._uses.get(grant_id, 0)


class ProofNonceLedger:
    def __init__(self):
        self._seen: set[tuple[str,str]] = set()
        self._lock = Lock()
    def consume(self, grant_id: str, nonce: str) -> bool:
        key=(grant_id,nonce)
        with self._lock:
            if key in self._seen:
                return False
            self._seen.add(key)
            return True
