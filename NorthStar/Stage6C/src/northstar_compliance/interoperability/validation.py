from __future__ import annotations

import datetime as dt
from dataclasses import asdict
from typing import Any

from .canonical import constant_time_equal, hmac_sha256, sha256_hex
from .models import ArtifactManifest, AuthorityGrant, EndpointDescriptor, TaskEnvelope


class ContractError(ValueError):
    pass


def verify_grant(grant: AuthorityGrant, *, secret: bytes, recipient: EndpointDescriptor, now: dt.datetime) -> None:
    expected = hmac_sha256(grant.unsigned(), secret)
    if not constant_time_equal(grant.signature, expected):
        raise ContractError("grant_signature_invalid")
    if grant.issuer != "CMP-007":
        raise ContractError("grant_issuer_invalid")
    if grant.subject != recipient.endpoint_id or grant.audience != recipient.endpoint_id:
        raise ContractError("grant_audience_mismatch")
    if not (grant.issued_at <= now < grant.expires_at):
        raise ContractError("grant_expired_or_not_yet_valid")
    if grant.max_uses != 1:
        raise ContractError("grant_use_limit_invalid")
    if grant.delegation_depth_remaining != 0:
        raise ContractError("grant_delegation_depth_invalid")
    if tuple(grant.allowed_operations) != ("verify_artifact",):
        raise ContractError("grant_operation_scope_invalid")


def verify_envelope(
    envelope: TaskEnvelope,
    *,
    secret: bytes,
    sender: EndpointDescriptor,
    recipient: EndpointDescriptor,
    grant: AuthorityGrant,
    now: dt.datetime,
) -> None:
    expected = hmac_sha256(envelope.unsigned(), secret)
    if not constant_time_equal(envelope.signature, expected):
        raise ContractError("envelope_signature_invalid")
    if envelope.schema_version != "1.0.0":
        raise ContractError("envelope_schema_version_unsupported")
    if envelope.sender_id != sender.endpoint_id or envelope.recipient_id != recipient.endpoint_id:
        raise ContractError("endpoint_binding_mismatch")
    if recipient.runtime_status != "candidate_sandbox_only":
        raise ContractError("recipient_status_invalid")
    if envelope.purpose not in recipient.allowed_purposes:
        raise ContractError("purpose_not_allowed")
    if envelope.expected_output_schema not in recipient.accepted_output_schemas:
        raise ContractError("output_schema_not_allowed")
    if envelope.attempt != 1 or envelope.hop_count != 1:
        raise ContractError("attempt_or_hop_invalid")
    if not (envelope.sent_at <= now < envelope.expires_at <= envelope.deadline_at):
        raise ContractError("envelope_time_window_invalid")
    if envelope.authority_grant_id != grant.grant_id or envelope.authority_grant_digest != grant.digest:
        raise ContractError("grant_binding_mismatch")
    for left, right, code in (
        (envelope.case_id, grant.case_id, "case_binding_mismatch"),
        (envelope.run_id, grant.run_id, "run_binding_mismatch"),
        (envelope.task_id, grant.task_id, "task_binding_mismatch"),
        (envelope.purpose, grant.purpose, "purpose_binding_mismatch"),
    ):
        if left != right:
            raise ContractError(code)
    if len(envelope.input_artifacts) != 1:
        raise ContractError("artifact_count_invalid")


def verify_artifact(
    manifest: ArtifactManifest,
    content: bytes,
    *,
    recipient: EndpointDescriptor,
    envelope: TaskEnvelope,
    grant: AuthorityGrant,
) -> None:
    if manifest.case_id != envelope.case_id:
        raise ContractError("artifact_case_mismatch")
    if recipient.endpoint_id not in manifest.authorized_subjects:
        raise ContractError("artifact_subject_not_authorized")
    if manifest.artifact_id not in grant.allowed_resources:
        raise ContractError("artifact_resource_not_authorized")
    if "case_evidence" not in grant.allowed_data_scopes:
        raise ContractError("artifact_data_scope_not_authorized")
    if manifest.content_sha256 != sha256_hex(content):
        raise ContractError("artifact_content_digest_invalid")


def envelope_wire_dict(envelope: TaskEnvelope) -> dict[str, Any]:
    data = asdict(envelope)
    for key in ("sent_at", "expires_at", "deadline_at"):
        data[key] = data[key].isoformat().replace("+00:00", "Z")
    return data
