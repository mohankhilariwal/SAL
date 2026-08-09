import datetime as dt
from dataclasses import replace

import pytest

from northstar_compliance.interoperability.fixtures import SIGNING_SECRET, build_fixture
from northstar_compliance.interoperability.validation import ContractError, verify_artifact, verify_envelope, verify_grant


def test_313_valid_grant_passes():
    f = build_fixture()
    verify_grant(f["grant"], secret=SIGNING_SECRET, recipient=f["recipient"], now=f["now"])


def test_314_invalid_grant_signature_fails():
    f = build_fixture()
    with pytest.raises(ContractError, match="grant_signature_invalid"):
        verify_grant(replace(f["grant"], signature="bad"), secret=SIGNING_SECRET, recipient=f["recipient"], now=f["now"])


def test_315_grant_audience_mismatch_fails():
    f = build_fixture()
    bad = replace(f["grant"], audience="OTHER").signed(SIGNING_SECRET)
    with pytest.raises(ContractError, match="grant_audience_mismatch"):
        verify_grant(bad, secret=SIGNING_SECRET, recipient=f["recipient"], now=f["now"])


def test_316_expired_grant_fails():
    f = build_fixture()
    with pytest.raises(ContractError, match="grant_expired"):
        verify_grant(f["grant"], secret=SIGNING_SECRET, recipient=f["recipient"], now=f["grant"].expires_at)


def test_317_valid_envelope_passes():
    f = build_fixture()
    verify_envelope(f["envelope"], secret=SIGNING_SECRET, sender=f["sender"], recipient=f["recipient"], grant=f["grant"], now=f["now"])


def test_318_envelope_signature_tamper_fails():
    f = build_fixture()
    with pytest.raises(ContractError, match="envelope_signature_invalid"):
        verify_envelope(replace(f["envelope"], signature="bad"), secret=SIGNING_SECRET, sender=f["sender"], recipient=f["recipient"], grant=f["grant"], now=f["now"])


def test_319_envelope_version_mismatch_fails():
    f = build_fixture()
    bad = replace(f["envelope"], schema_version="2.0.0").signed(SIGNING_SECRET)
    with pytest.raises(ContractError, match="unsupported"):
        verify_envelope(bad, secret=SIGNING_SECRET, sender=f["sender"], recipient=f["recipient"], grant=f["grant"], now=f["now"])


def test_320_artifact_tamper_fails():
    f = build_fixture()
    with pytest.raises(ContractError, match="artifact_content_digest_invalid"):
        verify_artifact(f["manifest"], f["content"] + b"x", recipient=f["recipient"], envelope=f["envelope"], grant=f["grant"])


def test_321_artifact_subject_denied():
    f = build_fixture()
    bad_manifest = replace(f["manifest"], authorized_subjects=("AGT-001",))
    with pytest.raises(ContractError, match="artifact_subject_not_authorized"):
        verify_artifact(bad_manifest, f["content"], recipient=f["recipient"], envelope=f["envelope"], grant=f["grant"])
