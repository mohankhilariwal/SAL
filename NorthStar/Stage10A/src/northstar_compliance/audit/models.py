from __future__ import annotations

import datetime as dt
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


@dataclass(frozen=True, slots=True)
class AuditActor:
    actor_type: str
    actor_id: str
    role: str | None = None
    workload_id: str | None = None


@dataclass(slots=True)
class AuditEvent:
    sequence: int
    event_type: str
    timestamp: str
    observed_timestamp: str
    actor: AuditActor
    tenant_id: str
    case_id: str
    run_id: str
    task_id: str
    component_id: str
    payload: dict[str, Any]
    payload_hash: str
    previous_hash: str
    record_hash: str
    signer_id: str
    signature: str
    trace_id: str
    span_id: str
    idempotency_key: str
    audit_event_id: str = field(default_factory=lambda: f"AUD-{uuid.uuid4().hex.upper()}")
    authority_effect: str = "none"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AuditVerificationReport:
    valid: bool
    event_count: int
    last_hash: str
    errors: list[str]
    verified_at: str = field(default_factory=utc_now)
    authority_effect: str = "none"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
