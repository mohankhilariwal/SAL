from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

MemoryStatus = Literal["active", "superseded", "expired", "deleted"]
MemoryKind = Literal["case_working"]
ContextKind = Literal[
    "case_state",
    "approval_state",
    "evidence_reference",
    "unresolved_question",
    "case_working_memory",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_z(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("datetime_must_be_timezone_aware")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("datetime_must_be_timezone_aware")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class Scope:
    tenant_id: str
    case_id: str
    user_id: str


@dataclass(frozen=True)
class SourceBinding:
    source_ref: str
    source_version: str
    source_sha256: str
    classification: str = "internal"


@dataclass(frozen=True)
class MemoryFact:
    fact_id: str
    field_name: str
    value: Any
    source: SourceBinding
    origin: Literal["authoritative_state", "human_decision_reference"]


@dataclass(frozen=True)
class ContextItem:
    item_id: str
    kind: ContextKind
    priority: int
    text: str
    source: SourceBinding
    scope: Scope
    authorized: bool
    fact_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ContextRegenerationPlan:
    plan_id: str
    schema_version: str
    strategy: Literal["authoritative_regeneration_v1"]
    scope: Scope
    state_object_id: str
    state_version: str
    include_memory: bool
    max_items: int
    max_chars: int
    generated_at: str


@dataclass(frozen=True)
class ContextSnapshot:
    snapshot_id: str
    schema_version: str
    plan_id: str
    scope: Scope
    strategy: Literal["deterministic_extractive_v1"]
    rendered_context: str
    included_item_ids: tuple[str, ...]
    omitted_item_refs: tuple[str, ...]
    facts: tuple[MemoryFact, ...]
    source_bindings: tuple[SourceBinding, ...]
    char_count: int
    item_count: int
    created_at: str
    content_sha256: str


@dataclass(frozen=True)
class MemoryConsentGrant:
    grant_id: str
    schema_version: str
    scope: Scope
    purpose: Literal["case_session_continuity"]
    allowed_operations: tuple[Literal["write", "read", "delete"], ...]
    issued_at: str
    expires_at: str
    revoked_at: str | None = None
    acknowledgement: str = "user_opt_in"

    def permits(self, operation: str, *, now: datetime | None = None) -> bool:
        current = now or utc_now()
        if self.revoked_at is not None:
            return False
        return operation in self.allowed_operations and parse_datetime(self.expires_at) > current


@dataclass(frozen=True)
class CaseWorkingMemoryRecord:
    record_id: str
    schema_version: str
    memory_kind: MemoryKind
    scope: Scope
    authorized_user_ids: tuple[str, ...]
    purpose: Literal["case_session_continuity"]
    consent_grant_id: str
    source_snapshot_id: str
    source_bindings: tuple[SourceBinding, ...]
    facts: tuple[MemoryFact, ...]
    unresolved_questions: tuple[str, ...]
    created_at: str
    expires_at: str
    status: MemoryStatus
    write_request_id: str
    supersedes_record_id: str | None
    content_sha256: str


@dataclass(frozen=True)
class MemoryQuery:
    query_id: str
    schema_version: str
    scope: Scope
    memory_kind: MemoryKind = "case_working"
    include_stale: bool = False


@dataclass(frozen=True)
class MemoryReadResult:
    query_id: str
    schema_version: str
    returned_record_ids: tuple[str, ...]
    stale_record_ids: tuple[str, ...]
    denied_record_ids: tuple[str, ...]
    records: tuple[CaseWorkingMemoryRecord, ...]
    generated_at: str


@dataclass(frozen=True)
class MemoryDeletionRequest:
    request_id: str
    schema_version: str
    scope: Scope
    record_id: str
    reason: str
    requested_at: str


@dataclass(frozen=True)
class MemoryLifecycleResult:
    request_id: str
    schema_version: str
    record_id: str
    previous_status: MemoryStatus
    new_status: MemoryStatus
    content_removed: bool
    tombstone_path: str
    completed_at: str


def dataclass_to_dict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        result = asdict(value)
        return result
    if isinstance(value, tuple):
        return [dataclass_to_dict(item) for item in value]
    if isinstance(value, list):
        return [dataclass_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: dataclass_to_dict(item) for key, item in value.items()}
    return value
