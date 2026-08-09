from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone

from .authority import AuthorityService
from .canonical import sha256_digest
from .envelopes import EnvelopeService
from .models import AgentEndpointDescriptor, ArtifactDescriptor, AuthorityGrant, HandoffEnvelope
from .policy import HandoffPolicy


ISSUER_SECRET = b"northstar-stage6b-authority-secret-32bytes-minimum"
ENVELOPE_SECRET = b"northstar-stage6b-envelope-secret-32bytes-minimum"


def endpoints() -> tuple[AgentEndpointDescriptor, AgentEndpointDescriptor]:
    sender = AgentEndpointDescriptor(
        endpoint_id="AGT-001",
        display_name="Regulatory Impact Assessment Agent",
        subject_kind="active_agent",
        runtime_status="active_one_agent_runtime",
        version="1.1.0",
        allowed_purposes=("evidence_verification",),
        allowed_input_schemas=("DATA-007", "DATA-090", "DATA-095"),
        allowed_output_schemas=("DATA-096",),
        allowed_tools=("TOOL-001", "TOOL-002", "TOOL-003", "TOOL-004", "TOOL-005", "TOOL-006"),
        allowed_data_scopes=("case_evidence",),
    )
    recipient = AgentEndpointDescriptor(
        endpoint_id="CAND-EVIDENCE-VERIFIER-001",
        display_name="Candidate Evidence Verification Endpoint",
        subject_kind="candidate_agent_endpoint",
        runtime_status="candidate_sandbox_only",
        version="0.1.0",
        allowed_purposes=("evidence_verification",),
        allowed_input_schemas=("DATA-007", "DATA-090", "DATA-095"),
        allowed_output_schemas=("DATA-096",),
        allowed_tools=(),
        allowed_data_scopes=("case_evidence",),
    )
    return sender, recipient


def services() -> tuple[HandoffPolicy, AuthorityService, EnvelopeService]:
    policy = HandoffPolicy()
    authority = AuthorityService(ISSUER_SECRET, policy)
    envelopes = EnvelopeService(ENVELOPE_SECRET, policy, authority)
    return policy, authority, envelopes


def build_signed_fixture(now: datetime | None = None):
    now = now or datetime(2026, 8, 1, 18, 30, tzinfo=timezone.utc)
    sender, recipient = endpoints()
    policy, authority, envelope_service = services()
    content = b'{"case":"CASE-001","evidence":["SRC-001"],"claim":"candidate"}'
    artifact = ArtifactDescriptor(
        artifact_id="ART-EVIDENCE-001",
        schema_id="DATA-095",
        schema_version="1.0.0",
        media_type="application/json",
        content_sha256=hashlib.sha256(content).hexdigest(),
        classification="internal",
        provenance_source_ids=("SRC-001",),
        authorized_subjects=(sender.endpoint_id, recipient.endpoint_id),
        case_id="CASE-001",
        created_by=sender.endpoint_id,
    )
    parent = authority.mint(
        AuthorityGrant(
            grant_id="GRANT-PARENT-001",
            issuer="CMP-007",
            subject_id=sender.endpoint_id,
            parent_subject_id=None,
            case_id="CASE-001",
            run_id="RUN-001",
            task_id="TASK-VERIFY-001",
            audience=sender.endpoint_id,
            purpose="evidence_verification",
            allowed_tools=(),
            allowed_operations=("verify_artifact",),
            allowed_resources=(artifact.artifact_id,),
            allowed_data_scopes=("case_evidence",),
            risk_tier=1,
            max_uses=1,
            delegation_depth_remaining=1,
            not_before=now - timedelta(seconds=1),
            expires_at=now + timedelta(minutes=5),
            nonce="NONCE-PARENT-001",
            proof_key_id="KEY-AGT-001",
        )
    )
    child = authority.attenuate(
        parent,
        AuthorityGrant(
            grant_id="GRANT-CHILD-001",
            issuer="CMP-007",
            subject_id=recipient.endpoint_id,
            parent_subject_id=sender.endpoint_id,
            case_id="CASE-001",
            run_id="RUN-001",
            task_id="TASK-VERIFY-001",
            audience=recipient.endpoint_id,
            purpose="evidence_verification",
            allowed_tools=(),
            allowed_operations=("verify_artifact",),
            allowed_resources=(artifact.artifact_id,),
            allowed_data_scopes=("case_evidence",),
            risk_tier=1,
            max_uses=1,
            delegation_depth_remaining=0,
            not_before=now,
            expires_at=now + timedelta(minutes=4),
            nonce="NONCE-CHILD-001",
            proof_key_id="KEY-CAND-VERIFIER",
            parent_grant_digest=parent.digest_sha256,
        )
    )
    envelope = envelope_service.sign_envelope(
        HandoffEnvelope(
            envelope_id="ENV-001",
            schema_version="1.0.0",
            message_type="task_offer",
            trace_id="TRACE-001",
            correlation_id="CORR-001",
            causation_id=None,
            sender_id=sender.endpoint_id,
            recipient_id=recipient.endpoint_id,
            case_id="CASE-001",
            run_id="RUN-001",
            task_id="TASK-VERIFY-001",
            attempt=1,
            sent_at=now,
            expires_at=now + timedelta(minutes=4),
            deadline_at=now + timedelta(minutes=3),
            priority=5,
            purpose="evidence_verification",
            goal="Verify that the candidate claim is supported by the supplied immutable evidence artifact.",
            non_goals=("approve", "finalize", "route_graph", "write_memory"),
            input_artifacts=(artifact,),
            expected_output_schema="DATA-096",
            context_policy_id="DATA-077",
            authority_grant_id=child.grant_id,
            authority_grant_digest=child.digest_sha256,
            max_hops=1,
            hop_count=1,
        )
    )
    return {
        "now": now,
        "sender": sender,
        "recipient": recipient,
        "policy": policy,
        "authority": authority,
        "envelopes": envelope_service,
        "content": content,
        "artifact": artifact,
        "parent": parent,
        "child": child,
        "envelope": envelope,
        "fixture_digest": sha256_digest({"envelope": envelope, "grant": child, "artifact": artifact}),
    }
