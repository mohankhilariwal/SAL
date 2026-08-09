from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from northstar_compliance.common.canonical import sha256_digest, utc_now_iso


class AuditUnavailable(RuntimeError):
    pass


class AuditPort(Protocol):
    def append(self, event_type: str, payload: dict[str, Any]) -> str: ...


@dataclass
class InMemoryAuditPort:
    fail: bool = False
    events: list[dict[str, Any]] = field(default_factory=list)

    def append(self, event_type: str, payload: dict[str, Any]) -> str:
        if self.fail:
            raise AuditUnavailable("mandatory audit append unavailable")
        event = {
            "event_type": event_type,
            "payload": payload,
            "created_at": utc_now_iso(),
            "authority_effect": "none",
        }
        event_id = sha256_digest(event)
        event["event_id"] = event_id
        self.events.append(event)
        return event_id
