from __future__ import annotations

from dataclasses import asdict, replace
from typing import Any

from .adapters.a2a import A2AMappingAdapter
from .adapters.direct import DirectAdapter
from .adapters.mcp import McpMappingAdapter
from .fixtures import build_fixture
from .registry import PROFILES, negotiate


def run_evaluations() -> list[dict[str, Any]]:
    fixture = build_fixture()
    direct = DirectAdapter().deliver(fixture)
    mcp = McpMappingAdapter()
    a2a = A2AMappingAdapter()
    message = a2a.map_task_message(fixture["envelope"], include_extension=True)
    bad_message = a2a.map_task_message(fixture["envelope"], include_extension=False)
    records = [
        {
            "evaluation_id": "EVAL-070",
            "name": "canonical_contract_preservation",
            "passed": direct.semantic_loss == (),
            "evidence": direct.digest,
        },
        {
            "evaluation_id": "EVAL-071",
            "name": "exact_version_negotiation",
            "passed": negotiate(
                negotiation_id="NEG-EVAL-001",
                protocol_name="A2A",
                local_supported=("1.0",),
                remote_supported=("1.0", "0.3"),
                binding_by_version={"1.0": "HTTP+JSON"},
            ).result == "accepted",
            "evidence": "A2A 1.0 exact match",
        },
        {
            "evaluation_id": "EVAL-072",
            "name": "version_mismatch_fails_closed",
            "passed": negotiate(
                negotiation_id="NEG-EVAL-002",
                protocol_name="MCP",
                local_supported=("2025-11-25",),
                remote_supported=("2026-07-28",),
                binding_by_version={"2025-11-25": "HTTP"},
            ).result == "rejected",
            "evidence": "no silent MCP downgrade/upgrade",
        },
        {
            "evaluation_id": "EVAL-073",
            "name": "mcp_domain_separation",
            "passed": mcp.attempt_agent_handoff_mapping().result == "fail_for_agent_handoff",
            "evidence": mcp.attempt_agent_handoff_mapping().lost_fields,
        },
        {
            "evaluation_id": "EVAL-074",
            "name": "a2a_extension_preserves_semantics",
            "passed": a2a.conformance_for_message(message).result == "pass",
            "evidence": a2a.conformance_for_message(message).digest,
        },
        {
            "evaluation_id": "EVAL-075",
            "name": "a2a_without_extension_fails",
            "passed": a2a.conformance_for_message(bad_message).result == "fail",
            "evidence": a2a.conformance_for_message(bad_message).lost_fields,
        },
        {
            "evaluation_id": "EVAL-076",
            "name": "one_active_agent_preserved",
            "passed": fixture["sender"].runtime_status == "active_one_agent_runtime" and fixture["recipient"].runtime_status == "candidate_sandbox_only",
            "evidence": [fixture["sender"].endpoint_id, fixture["recipient"].endpoint_id],
        },
        {
            "evaluation_id": "EVAL-077",
            "name": "no_concurrency_or_peer_delegation",
            "passed": not fixture["recipient"].can_run_concurrently and not fixture["recipient"].can_delegate,
            "evidence": fixture["recipient"].digest,
        },
        {
            "evaluation_id": "EVAL-078",
            "name": "protocol_profiles_have_explicit_status",
            "passed": all(profile.implementation_status for profile in PROFILES),
            "evidence": [profile.profile_id for profile in PROFILES],
        },
    ]
    return records
