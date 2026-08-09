from northstar_compliance.interoperability.adapters.mcp import McpMappingAdapter
from northstar_compliance.interoperability.fixtures import build_fixture


def test_330_mcp_maps_all_gateway_tools():
    f = build_fixture()
    doc = McpMappingAdapter().build_server_document(
        tool_ids=("TOOL-001", "TOOL-002", "TOOL-003", "TOOL-004", "TOOL-005", "TOOL-006"),
        artifacts=(f["manifest"],),
    )
    assert len(doc["tools"]) == 6


def test_331_mcp_marks_read_only_tools():
    f = build_fixture()
    doc = McpMappingAdapter().build_server_document(tool_ids=("TOOL-001", "TOOL-004"), artifacts=(f["manifest"],))
    flags = {item["title"]: item["annotations"]["readOnlyHint"] for item in doc["tools"]}
    assert flags == {"TOOL-001": True, "TOOL-004": False}


def test_332_mcp_resource_contains_integrity_metadata():
    f = build_fixture()
    resource = McpMappingAdapter().build_server_document(tool_ids=(), artifacts=(f["manifest"],))["resources"][0]
    assert resource["metadata"]["contentSha256"] == f["manifest"].content_sha256


def test_333_mcp_does_not_claim_agent_task_lifecycle():
    f = build_fixture()
    doc = McpMappingAdapter().build_server_document(tool_ids=(), artifacts=(f["manifest"],))
    assert doc["northstar"]["notAgentTaskLifecycle"] is True


def test_334_mcp_agent_handoff_mapping_fails():
    result = McpMappingAdapter().attempt_agent_handoff_mapping()
    assert result.result == "fail_for_agent_handoff" and result.lost_fields


def test_335_mcp_tool_resource_conformance_passes():
    assert McpMappingAdapter().conformance().result == "pass_for_tool_resource_domain"
