from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True, slots=True)
class HandoffPolicy:
    policy_id: str = "HOF-POL-001"
    schema_version: str = "1.0.0"
    accepted_architecture_version: str = "1.4.0"
    accepted_graph_version: str = "1.1.0"
    active_agent_ids: tuple[str, ...] = ("AGT-001",)
    candidate_endpoint_ids: tuple[str, ...] = ("CAND-EVIDENCE-VERIFIER-001",)
    allowed_message_types: tuple[str, ...] = (
        "task_offer",
        "task_accept",
        "task_reject",
        "status",
        "artifact_delivery",
        "cancel_request",
        "cancel_ack",
        "failure",
    )
    allowed_purposes: tuple[str, ...] = ("evidence_verification",)
    prohibited_capabilities: tuple[str, ...] = (
        "approve",
        "finalize",
        "route_graph",
        "mutate_protected_state",
        "write_memory",
        "create_agent",
        "delegate_again",
        "concurrent_execution",
        "cross_case_recall",
        "direct_tool_bypass",
    )
    max_hops: int = 1
    max_attempts: int = 1
    max_ttl: timedelta = timedelta(minutes=10)
    max_deadline: timedelta = timedelta(minutes=5)
    max_grant_uses: int = 1
    max_delegation_depth: int = 1
    accepted_context_policy_ids: tuple[str, ...] = ("DATA-077",)
    accepted_input_schemas: tuple[str, ...] = ("DATA-007", "DATA-090", "DATA-095")
    accepted_output_schemas: tuple[str, ...] = ("DATA-096",)
    current_runtime_mode: str = "contract_sandbox_only"
