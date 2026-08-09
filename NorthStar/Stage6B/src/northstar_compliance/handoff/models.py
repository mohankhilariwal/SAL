from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Any

from .canonical import sha256_digest


class HandoffStatus(str, Enum):
    OFFERED = "offered"
    ACCEPTED = "accepted"
    RUNNING = "running"
    COMPLETED = "completed"
    REJECTED = "rejected"
    FAILED = "failed"
    CANCEL_REQUESTED = "cancel_requested"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


TERMINAL_STATUSES = {
    HandoffStatus.COMPLETED,
    HandoffStatus.REJECTED,
    HandoffStatus.FAILED,
    HandoffStatus.CANCELLED,
    HandoffStatus.EXPIRED,
}


@dataclass(frozen=True, slots=True)
class AgentEndpointDescriptor:
    endpoint_id: str
    display_name: str
    subject_kind: str
    runtime_status: str
    version: str
    allowed_purposes: tuple[str, ...]
    allowed_input_schemas: tuple[str, ...]
    allowed_output_schemas: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    allowed_data_scopes: tuple[str, ...]
    may_delegate: bool = False
    may_write_memory: bool = False
    may_route: bool = False
    may_approve: bool = False
    may_finalize: bool = False
    may_run_concurrently: bool = False

    def digest(self) -> str:
        return sha256_digest(self)


@dataclass(frozen=True, slots=True)
class ArtifactDescriptor:
    artifact_id: str
    schema_id: str
    schema_version: str
    media_type: str
    content_sha256: str
    classification: str
    provenance_source_ids: tuple[str, ...]
    authorized_subjects: tuple[str, ...]
    case_id: str
    created_by: str
    immutable: bool = True

    def digest(self) -> str:
        return sha256_digest(self)


@dataclass(frozen=True, slots=True)
class AuthorityGrant:
    grant_id: str
    issuer: str
    subject_id: str
    parent_subject_id: str | None
    case_id: str
    run_id: str
    task_id: str
    audience: str
    purpose: str
    allowed_tools: tuple[str, ...]
    allowed_operations: tuple[str, ...]
    allowed_resources: tuple[str, ...]
    allowed_data_scopes: tuple[str, ...]
    risk_tier: int
    max_uses: int
    delegation_depth_remaining: int
    not_before: datetime
    expires_at: datetime
    nonce: str
    proof_key_id: str
    approval_refs: tuple[str, ...] = ()
    parent_grant_digest: str | None = None
    digest_sha256: str = ""
    signature: str = ""

    def unsigned(self) -> "AuthorityGrant":
        return replace(self, digest_sha256="", signature="")


@dataclass(frozen=True, slots=True)
class HandoffEnvelope:
    envelope_id: str
    schema_version: str
    message_type: str
    trace_id: str
    correlation_id: str
    causation_id: str | None
    sender_id: str
    recipient_id: str
    case_id: str
    run_id: str
    task_id: str
    attempt: int
    sent_at: datetime
    expires_at: datetime
    deadline_at: datetime
    priority: int
    purpose: str
    goal: str
    non_goals: tuple[str, ...]
    input_artifacts: tuple[ArtifactDescriptor, ...]
    expected_output_schema: str
    context_policy_id: str
    authority_grant_id: str
    authority_grant_digest: str
    max_hops: int
    hop_count: int
    status: HandoffStatus = HandoffStatus.OFFERED
    digest_sha256: str = ""
    signature: str = ""

    def unsigned(self) -> "HandoffEnvelope":
        return replace(self, digest_sha256="", signature="")


@dataclass(frozen=True, slots=True)
class HandoffReceipt:
    receipt_id: str
    envelope_id: str
    envelope_digest: str
    grant_digest: str
    recipient_id: str
    received_at: datetime
    accepted: bool
    reason_code: str
    verified_artifact_digests: tuple[str, ...]
    digest_sha256: str = ""
    signature: str = ""

    def unsigned(self) -> "HandoffReceipt":
        return replace(self, digest_sha256="", signature="")


@dataclass(frozen=True, slots=True)
class StatusEvent:
    event_id: str
    envelope_id: str
    task_id: str
    actor_id: str
    previous_status: HandoffStatus | None
    status: HandoffStatus
    occurred_at: datetime
    reason_code: str
    details: dict[str, Any] = field(default_factory=dict)
    digest_sha256: str = ""
