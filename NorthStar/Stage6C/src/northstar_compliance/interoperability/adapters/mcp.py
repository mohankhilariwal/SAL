from __future__ import annotations

from typing import Any, Iterable

from ..models import AdapterConformanceRecord, ArtifactManifest


class McpMappingAdapter:
    profile_id = "PRF-MCP-2026-07-28"

    def build_server_document(
        self,
        *,
        tool_ids: Iterable[str],
        artifacts: Iterable[ArtifactManifest],
    ) -> dict[str, Any]:
        tools = []
        for tool_id in tool_ids:
            tools.append(
                {
                    "name": tool_id.lower().replace("-", "_"),
                    "title": tool_id,
                    "description": "NorthStar gateway capability; authorization remains at CMP-005/CMP-007.",
                    "inputSchema": {"type": "object", "additionalProperties": False},
                    "annotations": {"readOnlyHint": tool_id in {"TOOL-001", "TOOL-002", "TOOL-003"}},
                }
            )
        resources = [
            {
                "uri": f"northstar://cases/{artifact.case_id}/artifacts/{artifact.artifact_id}",
                "name": artifact.artifact_id,
                "mimeType": artifact.media_type,
                "metadata": {
                    "contentSha256": artifact.content_sha256,
                    "classification": artifact.classification,
                    "schemaId": artifact.schema_id,
                },
            }
            for artifact in artifacts
        ]
        return {
            "protocolVersion": "2026-07-28",
            "serverInfo": {"name": "northstar-cmp005-reference", "version": "1.5.0"},
            "capabilities": {
                "tools": {"listChanged": False},
                "resources": {"subscribe": False, "listChanged": False},
                "logging": {},
            },
            "tools": tools,
            "resources": resources,
            "northstar": {
                "semanticDomain": "tool-resource-interoperability",
                "authorityIssuer": "CMP-007",
                "toolGateway": "CMP-005",
                "notAgentTaskLifecycle": True,
            },
        }

    def attempt_agent_handoff_mapping(self) -> AdapterConformanceRecord:
        lost = (
            "orchestrator-owned task acceptance lifecycle",
            "case/run/task-bound attenuated authority semantics",
            "system termination ownership",
            "human approval non-transfer invariant",
        )
        return AdapterConformanceRecord(
            conformance_id="CONF-MCP-HANDOFF-NEGATIVE-001",
            protocol_profile_id=self.profile_id,
            canonical_fields=("authority", "deadline", "cancellation", "artifact_integrity", "correlation", "termination"),
            native_mappings={
                "cancellation": "MCP cancellation utility",
                "artifact_integrity": "resource metadata plus NorthStar digest",
                "correlation": "JSON-RPC request ID/progress token plus NorthStar trace metadata",
            },
            extension_mappings={"authority": "NorthStar authorization outside MCP base semantics"},
            lost_fields=lost,
            prohibited_semantics_observed=(),
            result="fail_for_agent_handoff",
            notes="MCP is retained for tool/resource interoperability; it is not used as NorthStar's agent task protocol.",
        )

    def conformance(self) -> AdapterConformanceRecord:
        return AdapterConformanceRecord(
            conformance_id="CONF-MCP-001",
            protocol_profile_id=self.profile_id,
            canonical_fields=("tool_identity", "resource_identity", "schema", "capability_negotiation", "authorization_boundary"),
            native_mappings={
                "tool_identity": "tools/list name",
                "resource_identity": "resources/list URI",
                "schema": "tool inputSchema",
                "capability_negotiation": "initialize capabilities",
            },
            extension_mappings={"authorization_boundary": "CMP-007 grant + CMP-005 receiver PEP"},
            lost_fields=(),
            prohibited_semantics_observed=(),
            result="pass_for_tool_resource_domain",
            notes="No MCP server is activated in S06C; this is a deterministic mapping and policy check.",
        )
