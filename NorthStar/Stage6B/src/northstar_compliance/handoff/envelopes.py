from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from .authority import AuthorityService
from .canonical import sha256_digest, sign_hmac, verify_hmac
from .models import AgentEndpointDescriptor, HandoffEnvelope, HandoffReceipt
from .policy import HandoffPolicy


class EnvelopeError(ValueError):
    pass


class EnvelopeService:
    def __init__(self, secret: bytes, policy: HandoffPolicy, authority: AuthorityService) -> None:
        if len(secret) < 32:
            raise ValueError("envelope_secret_too_short")
        self._secret = secret
        self.policy = policy
        self.authority = authority

    def sign_envelope(self, envelope: HandoffEnvelope) -> HandoffEnvelope:
        self.validate_structure(envelope)
        unsigned = envelope.unsigned()
        digest = sha256_digest(unsigned)
        signature = sign_hmac(replace(unsigned, digest_sha256=digest), self._secret)
        return replace(unsigned, digest_sha256=digest, signature=signature)

    def verify_envelope(
        self,
        envelope: HandoffEnvelope,
        *,
        sender: AgentEndpointDescriptor,
        recipient: AgentEndpointDescriptor,
        grant,
        now: datetime | None = None,
    ) -> None:
        now = now or datetime.now(timezone.utc)
        self.validate_structure(envelope)
        expected_digest = sha256_digest(envelope.unsigned())
        if envelope.digest_sha256 != expected_digest:
            raise EnvelopeError("envelope_digest_mismatch")
        if not verify_hmac(replace(envelope, signature=""), envelope.signature, self._secret):
            raise EnvelopeError("envelope_signature_invalid")
        if envelope.sender_id != sender.endpoint_id or envelope.recipient_id != recipient.endpoint_id:
            raise EnvelopeError("endpoint_binding_mismatch")
        if envelope.purpose not in sender.allowed_purposes or envelope.purpose not in recipient.allowed_purposes:
            raise EnvelopeError("endpoint_purpose_mismatch")
        if envelope.expected_output_schema not in recipient.allowed_output_schemas:
            raise EnvelopeError("recipient_output_schema_mismatch")
        if envelope.context_policy_id not in self.policy.accepted_context_policy_ids:
            raise EnvelopeError("context_policy_not_accepted")
        if now >= envelope.expires_at or now >= envelope.deadline_at:
            raise EnvelopeError("envelope_expired")
        if envelope.authority_grant_id != grant.grant_id or envelope.authority_grant_digest != grant.digest_sha256:
            raise EnvelopeError("grant_binding_mismatch")
        self.authority.verify(grant, now=now, audience=envelope.recipient_id)
        for artifact in envelope.input_artifacts:
            if artifact.case_id != envelope.case_id:
                raise EnvelopeError("artifact_case_mismatch")
            if envelope.recipient_id not in artifact.authorized_subjects:
                raise EnvelopeError("artifact_recipient_not_authorized")
            if not artifact.immutable:
                raise EnvelopeError("mutable_artifact_prohibited")

    def sign_receipt(self, receipt: HandoffReceipt) -> HandoffReceipt:
        unsigned = receipt.unsigned()
        digest = sha256_digest(unsigned)
        signature = sign_hmac(replace(unsigned, digest_sha256=digest), self._secret)
        return replace(unsigned, digest_sha256=digest, signature=signature)

    def verify_receipt(self, receipt: HandoffReceipt) -> None:
        expected = sha256_digest(receipt.unsigned())
        if receipt.digest_sha256 != expected:
            raise EnvelopeError("receipt_digest_mismatch")
        if not verify_hmac(replace(receipt, signature=""), receipt.signature, self._secret):
            raise EnvelopeError("receipt_signature_invalid")

    def validate_structure(self, envelope: HandoffEnvelope) -> None:
        if envelope.message_type not in self.policy.allowed_message_types:
            raise EnvelopeError("message_type_not_allowed")
        if envelope.purpose not in self.policy.allowed_purposes:
            raise EnvelopeError("purpose_not_allowed")
        if envelope.attempt < 1 or envelope.attempt > self.policy.max_attempts:
            raise EnvelopeError("attempt_limit_exceeded")
        if envelope.hop_count < 0 or envelope.hop_count > envelope.max_hops or envelope.max_hops > self.policy.max_hops:
            raise EnvelopeError("hop_limit_exceeded")
        if envelope.deadline_at > envelope.expires_at:
            raise EnvelopeError("deadline_after_expiry")
        if envelope.expires_at - envelope.sent_at > self.policy.max_ttl:
            raise EnvelopeError("ttl_limit_exceeded")
        if envelope.deadline_at - envelope.sent_at > self.policy.max_deadline:
            raise EnvelopeError("deadline_limit_exceeded")
        if envelope.priority < 0 or envelope.priority > 9:
            raise EnvelopeError("invalid_priority")
        if not envelope.goal.strip():
            raise EnvelopeError("empty_goal")
