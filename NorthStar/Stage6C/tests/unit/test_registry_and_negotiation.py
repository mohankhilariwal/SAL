from northstar_compliance.interoperability.registry import PROFILES, get_profile, negotiate


def test_322_profiles_include_selected_http():
    assert get_profile("PRF-HTTP-JSON-1").implementation_status == "selected_reference_boundary"


def test_323_mcp_stable_profile_is_conformance_only():
    assert get_profile("PRF-MCP-2025-11-25").implementation_status == "legacy_compatibility_profile"


def test_324_current_mcp_is_conformance_only():
    assert get_profile("PRF-MCP-2026-07-28").implementation_status == "current_conformance_profile"


def test_325_a2a_profile_is_not_active_runtime():
    assert get_profile("PRF-A2A-1.0").implementation_status == "conformance_only_candidate_profile"


def test_326_exact_version_negotiation_passes():
    record = negotiate(
        negotiation_id="NEG-1",
        protocol_name="A2A",
        local_supported=("1.0",),
        remote_supported=("1.0", "0.3"),
        binding_by_version={"1.0": "HTTP+JSON"},
    )
    assert record.result == "accepted" and record.selected_version == "1.0"


def test_327_no_common_version_fails_closed():
    record = negotiate(
        negotiation_id="NEG-2",
        protocol_name="MCP",
        local_supported=("2025-11-25",),
        remote_supported=("2026-07-28",),
        binding_by_version={"2025-11-25": "HTTP"},
    )
    assert record.result == "rejected" and record.selected_version is None


def test_328_unapproved_binding_fails_closed():
    record = negotiate(
        negotiation_id="NEG-3",
        protocol_name="A2A",
        local_supported=("1.0",),
        remote_supported=("1.0",),
        binding_by_version={},
    )
    assert record.result == "rejected" and record.reason == "binding_not_approved"


def test_329_every_profile_has_prohibited_features():
    assert all(profile.prohibited_features for profile in PROFILES)
