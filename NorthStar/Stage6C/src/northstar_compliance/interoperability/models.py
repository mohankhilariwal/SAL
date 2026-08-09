from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field, replace
from typing import Any, Mapping

from .canonical import hmac_sha256, sha256_hex


@dataclass(frozen=True)
class EndpointDescriptor:
    endpoint_id: str
    name: str
    endpoint_kind: str
    runtime_status: str
    version: str
    allowed_purposes: tuple[str, ...]
    accepted_input_schemas: tuple[str, ...]
    accepted_output_schemas: tuple[str, ...]
    allowed_tools: tuple[str, ...] = ()
    allowed_data_scopes: tuple[str, ...] = ()
    can_delegate: bool = False
    can_write_memory: bool = False
    can_route: bool = False
    can_approve: bool = False
    can_finalize: bool = False
    can_run_concurrently: bool = False

    @property
    def digest(self) -> str:
        return sha256_hex(self)


@dataclass(frozen=True)
class ArtifactManifest:
    artifact_id: str
    schema_id: str
    schema_version: str
    content_sha256: str
    media_type: str
    classification: str
    case_id: str
    created_by: str
    authorized_subjects: tuple[str, ...]
    provenance_refs: tuple[str, ...]

    @classmethod
    def for_content(
        cls,
        *,
        artifact_id: str,
        schema_id: str,
        schema_version: str,
        content: bytes,
        media_type: str,
        classification: str,
        case_id: str,
        created_by: str,
        authorized_subjects: tuple[str, ...],
        provenance_refs: tuple[str, ...],
    ) -> "ArtifactManifest":
        return cls(
            artifact_id=artifact_id,
            schema_id=schema_id,
            schema_version=schema_version,
            content_sha256=sha256_hex(content),
            media_type=media_type,
            classification=classification,
            case_id=case_id,
            created_by=created_by,
            authorized_subjects=authorized_subjects,
            provenance_refs=provenance_refs,
        )

    @property
    def digest(self) -> str:
        return sha256_hex(self)


@dataclass(frozen=True)
class AuthorityGrant:
    grant_id: str
    issuer: str
    subject: str
    audience: str
    case_id: str
    run_id: str
    task_id: str
    purpose: str
    allowed_operations: tuple[str, ...]
    allowed_resources: tuple[str, ...]
    allowed_data_scopes: tuple[str, ...]
    issued_at: dt.datetime
    expires_at: dt.datetime
    max_uses: int
    delegation_depth_remaining: int
    nonce: str
    proof_key_id: str
    parent_grant_digest: str
    signature: str = ""

    def unsigned(self) -> "AuthorityGrant":
        return replace(self, signature="")

    @property
    def digest(self) -> str:
        return sha256_hex(self.unsigned())

    def signed(self, secret: bytes) -> "AuthorityGrant":
        return replace(self, signature=hmac_sha256(self.unsigned(), secret))


@dataclass(frozen=True)
class TaskEnvelope:
    envelope_id: str
    schema_version: str
    trace_id: str
    correlation_id: str
    causation_id: str
    sender_id: str
    recipient_id: str
    tenant_id: str
    case_id: str
    run_id: str
    task_id: str
    purpose: str
    goal: str
    non_goals: tuple[str, ...]
    expected_output_schema: str
    input_artifacts: tuple[ArtifactManifest, ...]
    authority_grant_id: str
    authority_grant_digest: str
    sent_at: dt.datetime
    expires_at: dt.datetime
    deadline_at: dt.datetime
    attempt: int = 1
    hop_count: int = 1
    signature: str = ""

    def unsigned(self) -> "TaskEnvelope":
        return replace(self, signature="")

    @property
    def digest(self) -> str:
        return sha256_hex(self.unsigned())

    def signed(self, secret: bytes) -> "TaskEnvelope":
        return replace(self, signature=hmac_sha256(self.unsigned(), secret))


@dataclass(frozen=True)
class ProtocolProfile:
    profile_id: str
    protocol_name: str
    protocol_version: str
    binding: str
    semantic_domain: str
    implementation_status: str
    canonical_contract_version: str
    supported_features: tuple[str, ...]
    prohibited_features: tuple[str, ...]
    security_target: tuple[str, ...]
    notes: str

    @property
    def digest(self) -> str:
        return sha256_hex(self)


@dataclass(frozen=True)
class CapabilityAdvertisement:
    advertisement_id: str
    endpoint_id: str
    endpoint_version: str
    endpoint_digest: str
    protocol_profiles: tuple[str, ...]
    skills: tuple[str, ...]
    tools: tuple[str, ...]
    resources: tuple[str, ...]
    security_schemes: tuple[str, ...]
    expires_at: dt.datetime
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def digest(self) -> str:
        return sha256_hex(self)


@dataclass(frozen=True)
class VersionNegotiationRecord:
    negotiation_id: str
    protocol_name: str
    local_supported: tuple[str, ...]
    remote_supported: tuple[str, ...]
    selected_version: str | None
    selected_binding: str | None
    result: str
    reason: str

    @property
    def digest(self) -> str:
        return sha256_hex(self)


@dataclass(frozen=True)
class TransportDeliveryReceipt:
    receipt_id: str
    protocol_profile_id: str
    binding: str
    envelope_digest: str
    grant_digest: str
    request_content_digest: str
    response_content_digest: str
    correlation_id: str
    task_id: str
    terminal_status: str
    delivered_at: dt.datetime
    remote_endpoint_id: str
    semantic_loss: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def digest(self) -> str:
        return sha256_hex(self)


@dataclass(frozen=True)
class AdapterConformanceRecord:
    conformance_id: str
    protocol_profile_id: str
    canonical_fields: tuple[str, ...]
    native_mappings: Mapping[str, str]
    extension_mappings: Mapping[str, str]
    lost_fields: tuple[str, ...]
    prohibited_semantics_observed: tuple[str, ...]
    result: str
    notes: str

    @property
    def digest(self) -> str:
        return sha256_hex(self)
