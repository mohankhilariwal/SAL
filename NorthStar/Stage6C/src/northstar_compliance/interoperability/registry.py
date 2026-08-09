from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import ProtocolProfile, VersionNegotiationRecord


PROFILES: tuple[ProtocolProfile, ...] = (
    ProtocolProfile(
        profile_id="PRF-DIRECT-1",
        protocol_name="northstar-direct",
        protocol_version="1.0",
        binding="python-call",
        semantic_domain="canonical-contract-test",
        implementation_status="local_test_only",
        canonical_contract_version="1.0.0",
        supported_features=("envelope", "authority", "artifact", "receipt", "status", "cancellation"),
        prohibited_features=("remote_agent_activation", "concurrency", "peer_delegation"),
        security_target=("process-local-integrity",),
        notes="Fast local reference; not an interoperability boundary.",
    ),
    ProtocolProfile(
        profile_id="PRF-HTTP-JSON-1",
        protocol_name="northstar-http-json",
        protocol_version="1.0",
        binding="HTTP+JSON",
        semantic_domain="canonical-handoff-delivery",
        implementation_status="selected_reference_boundary",
        canonical_contract_version="1.0.0",
        supported_features=("synchronous_offer", "exact_version", "content_digest", "correlation", "deadline", "typed_error"),
        prohibited_features=("concurrent_task_execution", "automatic_retry", "peer_delegation", "agent_promotion"),
        security_target=("HTTPS", "mTLS-or-OAuth2", "sender-constrained-grant", "receiver-PEP"),
        notes="Serialized reference transport proving a real process boundary without selecting a production topology.",
    ),
    ProtocolProfile(
        profile_id="PRF-MCP-2025-11-25",
        protocol_name="MCP",
        protocol_version="2025-11-25",
        binding="Streamable HTTP or stdio",
        semantic_domain="tool-resource-interoperability",
        implementation_status="legacy_compatibility_profile",
        canonical_contract_version="1.0.0",
        supported_features=("tools", "resources", "prompts", "capability_negotiation", "progress", "cancellation"),
        prohibited_features=("agent_task_authority", "case_termination_ownership", "agent_promotion"),
        security_target=("OAuth-based-authorization-for-HTTP", "consent", "resource-server-enforcement"),
        notes="Prior stable MCP revision retained only for compatibility analysis.",
    ),
    ProtocolProfile(
        profile_id="PRF-MCP-2026-07-28",
        protocol_name="MCP",
        protocol_version="2026-07-28",
        binding="HTTP",
        semantic_domain="tool-resource-interoperability",
        implementation_status="current_conformance_profile",
        canonical_contract_version="1.0.0",
        supported_features=("stateless_core", "extensions", "versioning", "authorization_hardening", "tools", "resources"),
        prohibited_features=("agent_task_authority", "case_termination_ownership", "agent_promotion"),
        security_target=("OAuth-and-OIDC-aligned" ,),
        notes="Current MCP revision selected for conformance mapping only; no MCP server is activated.",
    ),
    ProtocolProfile(
        profile_id="PRF-A2A-1.0",
        protocol_name="A2A",
        protocol_version="1.0",
        binding="HTTP+JSON",
        semantic_domain="agent-task-lifecycle",
        implementation_status="conformance_only_candidate_profile",
        canonical_contract_version="1.0.0",
        supported_features=("agent_card", "task", "message", "artifact", "status", "cancellation", "version_negotiation"),
        prohibited_features=("activate_AGT-002", "shared_state", "shared_memory", "concurrent_execution"),
        security_target=("HTTPS", "OAuth2-or-mTLS", "signed-agent-card", "receiver-authorization"),
        notes="A2A core plus a required NorthStar extension preserves authority/deadline/trace/termination semantics.",
    ),
    ProtocolProfile(
        profile_id="PRF-GRPC-DEFERRED",
        protocol_name="gRPC",
        protocol_version="deferred",
        binding="HTTP/2+protobuf",
        semantic_domain="service-rpc",
        implementation_status="deferred",
        canonical_contract_version="1.0.0",
        supported_features=("typed_rpc", "deadlines", "cancellation", "streaming"),
        prohibited_features=("selected_without-protobuf-and-runtime-evidence",),
        security_target=("TLS", "workload-identity"),
        notes="Strong option for internal typed services; not selected for this local minimal boundary.",
    ),
    ProtocolProfile(
        profile_id="PRF-EVENT-DEFERRED",
        protocol_name="queue-event-bus",
        protocol_version="deferred",
        binding="broker",
        semantic_domain="asynchronous-distributed-delivery",
        implementation_status="deferred_to_S06D",
        canonical_contract_version="1.0.0",
        supported_features=("durability", "buffering", "fanout"),
        prohibited_features=("concurrency-before-S06D",),
        security_target=("broker-ACL", "encryption", "dedupe-ledger"),
        notes="Requires delivery, ordering, deduplication, dead-letter and backpressure architecture.",
    ),
)


def get_profile(profile_id: str) -> ProtocolProfile:
    for profile in PROFILES:
        if profile.profile_id == profile_id:
            return profile
    raise KeyError(profile_id)


def negotiate(
    *,
    negotiation_id: str,
    protocol_name: str,
    local_supported: Iterable[str],
    remote_supported: Iterable[str],
    binding_by_version: dict[str, str],
) -> VersionNegotiationRecord:
    local = tuple(local_supported)
    remote = tuple(remote_supported)
    common = [version for version in local if version in remote]
    if not common:
        return VersionNegotiationRecord(
            negotiation_id=negotiation_id,
            protocol_name=protocol_name,
            local_supported=local,
            remote_supported=remote,
            selected_version=None,
            selected_binding=None,
            result="rejected",
            reason="no_exact_compatible_version",
        )
    selected = common[0]
    binding = binding_by_version.get(selected)
    if not binding:
        return VersionNegotiationRecord(
            negotiation_id=negotiation_id,
            protocol_name=protocol_name,
            local_supported=local,
            remote_supported=remote,
            selected_version=None,
            selected_binding=None,
            result="rejected",
            reason="binding_not_approved",
        )
    return VersionNegotiationRecord(
        negotiation_id=negotiation_id,
        protocol_name=protocol_name,
        local_supported=local,
        remote_supported=remote,
        selected_version=selected,
        selected_binding=binding,
        result="accepted",
        reason="exact_version_and_binding_match",
    )
