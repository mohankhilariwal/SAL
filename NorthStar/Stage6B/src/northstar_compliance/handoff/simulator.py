from __future__ import annotations

import hashlib
from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

from .artifacts import InMemoryArtifactStore
from .authority import AuthorityService
from .envelopes import EnvelopeService
from .lifecycle import HandoffCoordinator
from .models import (
    AgentEndpointDescriptor,
    ArtifactDescriptor,
    AuthorityGrant,
    HandoffEnvelope,
    HandoffReceipt,
    HandoffStatus,
)


class SequentialHandoffSandbox:
    """Deterministic two-party contract lab, not an activated multi-agent runtime."""

    def __init__(
        self,
        *,
        sender: AgentEndpointDescriptor,
        recipient: AgentEndpointDescriptor,
        authority: AuthorityService,
        envelopes: EnvelopeService,
        coordinator: HandoffCoordinator,
        artifacts: InMemoryArtifactStore,
    ) -> None:
        self.sender = sender
        self.recipient = recipient
        self.authority = authority
        self.envelopes = envelopes
        self.coordinator = coordinator
        self.artifacts = artifacts

    def execute_verification(
        self,
        *,
        envelope: HandoffEnvelope,
        grant: AuthorityGrant,
        input_content: bytes,
        now: datetime | None = None,
    ) -> tuple[HandoffReceipt, ArtifactDescriptor]:
        now = now or datetime.now(timezone.utc)
        if self.recipient.runtime_status != "candidate_sandbox_only":
            raise RuntimeError("recipient_not_sandbox_candidate")
        self.envelopes.verify_envelope(
            envelope,
            sender=self.sender,
            recipient=self.recipient,
            grant=grant,
            now=now,
        )
        self.coordinator.register(envelope)
        self.coordinator.transition(
            envelope.envelope_id,
            HandoffStatus.ACCEPTED,
            actor_id=self.recipient.endpoint_id,
            reason_code="contract_accepted",
            now=now,
        )
        self.authority.authorize_use(
            grant,
            audience=self.recipient.endpoint_id,
            nonce=f"{grant.nonce}:consume",
            operation="verify_artifact",
            resource=envelope.input_artifacts[0].artifact_id,
            data_scope="case_evidence",
            now=now,
        )
        self.artifacts.put(envelope.input_artifacts[0], input_content)
        self.coordinator.transition(
            envelope.envelope_id,
            HandoffStatus.RUNNING,
            actor_id=self.recipient.endpoint_id,
            reason_code="verification_started",
            now=now,
        )

        verdict = b"verified:" + hashlib.sha256(input_content).hexdigest().encode("ascii")
        output = ArtifactDescriptor(
            artifact_id=f"ART-VERIFY-{uuid4().hex[:12].upper()}",
            schema_id=envelope.expected_output_schema,
            schema_version="1.0.0",
            media_type="application/json",
            content_sha256=hashlib.sha256(verdict).hexdigest(),
            classification="internal",
            provenance_source_ids=tuple(a.artifact_id for a in envelope.input_artifacts),
            authorized_subjects=(self.sender.endpoint_id, self.recipient.endpoint_id),
            case_id=envelope.case_id,
            created_by=self.recipient.endpoint_id,
            immutable=True,
        )
        self.artifacts.put(output, verdict)
        self.coordinator.transition(
            envelope.envelope_id,
            HandoffStatus.COMPLETED,
            actor_id=self.recipient.endpoint_id,
            reason_code="verification_completed",
            now=now,
            details={"output_artifact_id": output.artifact_id},
        )
        receipt = HandoffReceipt(
            receipt_id=f"RCP-{uuid4().hex[:16].upper()}",
            envelope_id=envelope.envelope_id,
            envelope_digest=envelope.digest_sha256,
            grant_digest=grant.digest_sha256,
            recipient_id=self.recipient.endpoint_id,
            received_at=now,
            accepted=True,
            reason_code="completed",
            verified_artifact_digests=tuple(a.digest() for a in envelope.input_artifacts),
        )
        return self.envelopes.sign_receipt(receipt), output
