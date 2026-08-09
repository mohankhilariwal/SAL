from dataclasses import replace
from datetime import timedelta

import pytest

from northstar_compliance.handoff.authority import AuthorityError
from northstar_compliance.handoff.fixtures import build_signed_fixture


def test_271_parent_and_child_grants_verify():
    f = build_signed_fixture()
    f["authority"].verify(f["parent"], now=f["now"], audience="AGT-001")
    f["authority"].verify(f["child"], now=f["now"], audience="CAND-EVIDENCE-VERIFIER-001")


def test_272_child_grant_is_strictly_attenuated():
    f = build_signed_fixture()
    assert f["child"].delegation_depth_remaining == 0
    assert set(f["child"].allowed_tools).issubset(f["parent"].allowed_tools)
    assert f["child"].expires_at <= f["parent"].expires_at


def test_273_tool_scope_escalation_is_rejected():
    f = build_signed_fixture()
    bad = replace(f["child"].unsigned(), grant_id="BAD", allowed_tools=("TOOL-006",))
    with pytest.raises(AuthorityError, match="tool_scope_escalation"):
        f["authority"].attenuate(f["parent"], bad)


def test_274_operation_scope_escalation_is_rejected():
    f = build_signed_fixture()
    bad = replace(f["child"].unsigned(), grant_id="BAD", allowed_operations=("verify_artifact", "approve"))
    with pytest.raises(AuthorityError, match="operation_scope_escalation"):
        f["authority"].attenuate(f["parent"], bad)


def test_275_expiry_escalation_is_rejected():
    f = build_signed_fixture()
    bad = replace(f["child"].unsigned(), grant_id="BAD", expires_at=f["parent"].expires_at + timedelta(seconds=1))
    with pytest.raises(AuthorityError, match="expiry_escalation"):
        f["authority"].attenuate(f["parent"], bad)


def test_276_parent_digest_binding_is_required():
    f = build_signed_fixture()
    bad = replace(f["child"].unsigned(), grant_id="BAD", parent_grant_digest="0" * 64)
    with pytest.raises(AuthorityError, match="parent_grant_digest_mismatch"):
        f["authority"].attenuate(f["parent"], bad)


def test_277_grant_signature_tamper_fails_closed():
    f = build_signed_fixture()
    bad = replace(f["child"], signature="0" * 64)
    with pytest.raises(AuthorityError, match="grant_signature_invalid"):
        f["authority"].verify(bad, now=f["now"], audience=f["recipient"].endpoint_id)


def test_278_audience_binding_is_enforced():
    f = build_signed_fixture()
    with pytest.raises(AuthorityError, match="grant_audience_mismatch"):
        f["authority"].verify(f["child"], now=f["now"], audience="AGT-001")


def test_279_single_use_and_nonce_replay_are_enforced():
    f = build_signed_fixture()
    kwargs = dict(
        audience=f["recipient"].endpoint_id,
        nonce="USE-001",
        operation="verify_artifact",
        resource=f["artifact"].artifact_id,
        data_scope="case_evidence",
        now=f["now"],
    )
    f["authority"].authorize_use(f["child"], **kwargs)
    with pytest.raises(AuthorityError, match="nonce_replay|grant_use_exhausted"):
        f["authority"].authorize_use(f["child"], **kwargs)


def test_280_revoked_grant_cannot_be_used():
    f = build_signed_fixture()
    f["authority"].revoke(f["child"].grant_id)
    with pytest.raises(AuthorityError, match="grant_revoked"):
        f["authority"].authorize_use(
            f["child"],
            audience=f["recipient"].endpoint_id,
            nonce="USE-002",
            operation="verify_artifact",
            resource=f["artifact"].artifact_id,
            data_scope="case_evidence",
            now=f["now"],
        )
