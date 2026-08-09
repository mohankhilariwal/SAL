from __future__ import annotations

import datetime as dt
import json
from dataclasses import asdict, replace

import pytest

from northstar_compliance.interoperability.adapters.a2a import A2AMappingAdapter
from northstar_compliance.interoperability.adapters.mcp import McpMappingAdapter
from northstar_compliance.interoperability.fixtures import SIGNING_SECRET, build_fixture
from northstar_compliance.interoperability.registry import get_profile
from northstar_compliance.interoperability.validation import ContractError, verify_envelope, verify_grant


def test_347_protocol_profiles_do_not_claim_production_identity():
    assert "OAuth2" in " ".join(get_profile("PRF-HTTP-JSON-1").security_target)
    assert get_profile("PRF-HTTP-JSON-1").implementation_status == "selected_reference_boundary"


def test_348_candidate_cannot_delegate():
    assert build_fixture()["recipient"].can_delegate is False


def test_349_candidate_has_no_tools():
    assert build_fixture()["recipient"].allowed_tools == ()


def test_350_mcp_tool_descriptions_are_not_authority():
    f = build_fixture()
    doc = McpMappingAdapter().build_server_document(tool_ids=("TOOL-001",), artifacts=(f["manifest"],))
    assert "authorization remains" in doc["tools"][0]["description"]


def test_351_a2a_card_does_not_allocate_agent():
    f = build_fixture()
    card = A2AMappingAdapter().build_agent_card(f["recipient"], endpoint_url="https://invalid.example")
    assert card["metadata"]["northstarNoAgentAllocation"] is True


def test_352_late_envelope_fails_closed():
    f = build_fixture()
    with pytest.raises(ContractError, match="time_window"):
        verify_envelope(f["envelope"], secret=SIGNING_SECRET, sender=f["sender"], recipient=f["recipient"], grant=f["grant"], now=f["envelope"].expires_at)


def test_353_multi_use_grant_fails():
    f = build_fixture()
    bad = replace(f["grant"], max_uses=2).signed(SIGNING_SECRET)
    with pytest.raises(ContractError, match="use_limit"):
        verify_grant(bad, secret=SIGNING_SECRET, recipient=f["recipient"], now=f["now"])


def test_354_delegation_depth_fails():
    f = build_fixture()
    bad = replace(f["grant"], delegation_depth_remaining=1).signed(SIGNING_SECRET)
    with pytest.raises(ContractError, match="delegation_depth"):
        verify_grant(bad, secret=SIGNING_SECRET, recipient=f["recipient"], now=f["now"])
