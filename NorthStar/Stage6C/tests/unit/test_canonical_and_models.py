from dataclasses import replace

import pytest

from northstar_compliance.interoperability.canonical import canonical_json, hmac_sha256, sha256_hex
from northstar_compliance.interoperability.fixtures import SIGNING_SECRET, build_fixture


def test_307_canonical_json_is_stable():
    assert canonical_json({"b": 2, "a": 1}) == '{"a":1,"b":2}'


def test_308_hash_changes_on_content_change():
    assert sha256_hex(b"a") != sha256_hex(b"b")


def test_309_grant_digest_excludes_signature():
    fixture = build_fixture()
    grant = fixture["grant"]
    assert grant.digest == replace(grant, signature="changed").digest


def test_310_envelope_digest_excludes_signature():
    fixture = build_fixture()
    envelope = fixture["envelope"]
    assert envelope.digest == replace(envelope, signature="changed").digest


def test_311_manifest_hash_matches_content():
    fixture = build_fixture()
    assert fixture["manifest"].content_sha256 == sha256_hex(fixture["content"])


def test_312_endpoint_candidate_has_zero_authority_flags():
    endpoint = build_fixture()["recipient"]
    assert not any((endpoint.can_delegate, endpoint.can_write_memory, endpoint.can_route, endpoint.can_approve, endpoint.can_finalize, endpoint.can_run_concurrently))
