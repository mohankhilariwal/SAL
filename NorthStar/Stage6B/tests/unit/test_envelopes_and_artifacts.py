from dataclasses import replace
from datetime import timedelta

import pytest

from northstar_compliance.handoff.artifacts import ArtifactError, InMemoryArtifactStore
from northstar_compliance.handoff.envelopes import EnvelopeError
from northstar_compliance.handoff.fixtures import build_signed_fixture


def test_281_signed_envelope_verifies():
    f = build_signed_fixture()
    f["envelopes"].verify_envelope(
        f["envelope"], sender=f["sender"], recipient=f["recipient"], grant=f["child"], now=f["now"]
    )


def test_282_envelope_digest_tamper_is_rejected():
    f = build_signed_fixture()
    bad = replace(f["envelope"], goal="tampered")
    with pytest.raises(EnvelopeError, match="envelope_digest_mismatch"):
        f["envelopes"].verify_envelope(
            bad, sender=f["sender"], recipient=f["recipient"], grant=f["child"], now=f["now"]
        )


def test_283_envelope_signature_tamper_is_rejected():
    f = build_signed_fixture()
    bad = replace(f["envelope"], signature="f" * 64)
    with pytest.raises(EnvelopeError, match="envelope_signature_invalid"):
        f["envelopes"].verify_envelope(
            bad, sender=f["sender"], recipient=f["recipient"], grant=f["child"], now=f["now"]
        )


def test_284_unknown_recipient_binding_is_rejected():
    f = build_signed_fixture()
    other = replace(f["recipient"], endpoint_id="CAND-OTHER")
    with pytest.raises(EnvelopeError, match="endpoint_binding_mismatch"):
        f["envelopes"].verify_envelope(
            f["envelope"], sender=f["sender"], recipient=other, grant=f["child"], now=f["now"]
        )


def test_285_expired_envelope_is_rejected():
    f = build_signed_fixture()
    with pytest.raises(EnvelopeError, match="envelope_expired"):
        f["envelopes"].verify_envelope(
            f["envelope"],
            sender=f["sender"],
            recipient=f["recipient"],
            grant=f["child"],
            now=f["envelope"].expires_at + timedelta(seconds=1),
        )


def test_286_artifact_case_mismatch_is_rejected():
    f = build_signed_fixture()
    bad_artifact = replace(f["artifact"], case_id="CASE-OTHER")
    bad = f["envelopes"].sign_envelope(replace(f["envelope"].unsigned(), input_artifacts=(bad_artifact,)))
    with pytest.raises(EnvelopeError, match="artifact_case_mismatch"):
        f["envelopes"].verify_envelope(
            bad, sender=f["sender"], recipient=f["recipient"], grant=f["child"], now=f["now"]
        )


def test_287_artifact_recipient_authorization_is_required():
    f = build_signed_fixture()
    bad_artifact = replace(f["artifact"], authorized_subjects=("AGT-001",))
    bad = f["envelopes"].sign_envelope(replace(f["envelope"].unsigned(), input_artifacts=(bad_artifact,)))
    with pytest.raises(EnvelopeError, match="artifact_recipient_not_authorized"):
        f["envelopes"].verify_envelope(
            bad, sender=f["sender"], recipient=f["recipient"], grant=f["child"], now=f["now"]
        )


def test_288_artifact_content_hash_is_verified():
    f = build_signed_fixture()
    store = InMemoryArtifactStore()
    with pytest.raises(ArtifactError, match="artifact_content_digest_mismatch"):
        store.put(f["artifact"], b"tampered")


def test_289_immutable_artifact_conflict_is_rejected():
    f = build_signed_fixture()
    store = InMemoryArtifactStore()
    store.put(f["artifact"], f["content"])
    conflicting = replace(f["artifact"], content_sha256="0" * 64)
    with pytest.raises(ArtifactError):
        store.put(conflicting, b"different")


def test_290_receipt_signature_verifies():
    from datetime import timezone
    from northstar_compliance.handoff.models import HandoffReceipt

    f = build_signed_fixture()
    receipt = HandoffReceipt(
        receipt_id="RCP-001",
        envelope_id=f["envelope"].envelope_id,
        envelope_digest=f["envelope"].digest_sha256,
        grant_digest=f["child"].digest_sha256,
        recipient_id=f["recipient"].endpoint_id,
        received_at=f["now"].astimezone(timezone.utc),
        accepted=True,
        reason_code="accepted",
        verified_artifact_digests=(f["artifact"].digest(),),
    )
    signed = f["envelopes"].sign_receipt(receipt)
    f["envelopes"].verify_receipt(signed)
