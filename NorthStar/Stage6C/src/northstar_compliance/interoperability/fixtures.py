from __future__ import annotations

import datetime as dt
from dataclasses import asdict
from typing import Any

from .models import ArtifactManifest, AuthorityGrant, EndpointDescriptor, TaskEnvelope

SIGNING_SECRET = b"northstar-stage6c-reference-secret-not-production"


def utc(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def build_fixture(now: dt.datetime | None = None) -> dict[str, Any]:
    now = now or utc("2026-08-01T18:00:00Z")
    sender = EndpointDescriptor(
        endpoint_id="AGT-001",
        name="Regulatory Impact Assessment Agent",
        endpoint_kind="active_agent",
        runtime_status="active_one_agent_runtime",
        version="1.1.0",
        allowed_purposes=("regulatory_impact_assessment",),
        accepted_input_schemas=("DATA-001", "DATA-041"),
        accepted_output_schemas=("DATA-041",),
        allowed_tools=("TOOL-001", "TOOL-002", "TOOL-003", "TOOL-004", "TOOL-005", "TOOL-006"),
        allowed_data_scopes=("case_evidence", "policy", "control", "process"),
    )
    recipient = EndpointDescriptor(
        endpoint_id="CAND-EVIDENCE-VERIFIER-001",
        name="Candidate Evidence Verification Endpoint",
        endpoint_kind="candidate_endpoint",
        runtime_status="candidate_sandbox_only",
        version="0.1.0",
        allowed_purposes=("verify_supplied_evidence",),
        accepted_input_schemas=("DATA-095",),
        accepted_output_schemas=("DATA-096",),
        allowed_tools=(),
        allowed_data_scopes=("case_evidence",),
    )
    content = b'{"finding":"The cited control text is present and the source digest matches.","not_an_approval":true}'
    manifest = ArtifactManifest.for_content(
        artifact_id="ART-EVID-001",
        schema_id="DATA-095",
        schema_version="1.0.0",
        content=content,
        media_type="application/json",
        classification="northstar-confidential",
        case_id="CASE-NS-060C-001",
        created_by="AGT-001",
        authorized_subjects=("AGT-001", "CAND-EVIDENCE-VERIFIER-001"),
        provenance_refs=("PUB-NS-001", "POL-LEND-001", "CTRL-PRIV-007"),
    )
    grant = AuthorityGrant(
        grant_id="GRANT-060C-001",
        issuer="CMP-007",
        subject=recipient.endpoint_id,
        audience=recipient.endpoint_id,
        case_id=manifest.case_id,
        run_id="RUN-060C-001",
        task_id="TASK-VERIFY-001",
        purpose="verify_supplied_evidence",
        allowed_operations=("verify_artifact",),
        allowed_resources=(manifest.artifact_id,),
        allowed_data_scopes=("case_evidence",),
        issued_at=now - dt.timedelta(minutes=1),
        expires_at=now + dt.timedelta(minutes=4),
        max_uses=1,
        delegation_depth_remaining=0,
        nonce="nonce-060c-001",
        proof_key_id="reference-hmac-key-1",
        parent_grant_digest="parent-grant-digest-redacted",
    ).signed(SIGNING_SECRET)
    envelope = TaskEnvelope(
        envelope_id="ENV-060C-001",
        schema_version="1.0.0",
        trace_id="TRACE-060C-001",
        correlation_id="CORR-060C-001",
        causation_id="EVT-060C-START",
        sender_id=sender.endpoint_id,
        recipient_id=recipient.endpoint_id,
        tenant_id="NORTHSTAR",
        case_id=manifest.case_id,
        run_id=grant.run_id,
        task_id=grant.task_id,
        purpose=grant.purpose,
        goal="Verify the supplied immutable evidence artefact and return DATA-096.",
        non_goals=("Do not approve", "Do not mutate case state", "Do not call tools", "Do not write memory"),
        expected_output_schema="DATA-096",
        input_artifacts=(manifest,),
        authority_grant_id=grant.grant_id,
        authority_grant_digest=grant.digest,
        sent_at=now,
        expires_at=now + dt.timedelta(minutes=3),
        deadline_at=now + dt.timedelta(minutes=5),
    ).signed(SIGNING_SECRET)
    return {
        "now": now,
        "sender": sender,
        "recipient": recipient,
        "content": content,
        "manifest": manifest,
        "grant": grant,
        "envelope": envelope,
    }
