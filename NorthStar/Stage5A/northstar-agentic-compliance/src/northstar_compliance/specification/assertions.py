from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .context_policy import ContextPolicyViolation, enforce_context_profile
from .models import AgentSpecification, RuntimeAssertionResult


class RuntimeAssertionEngine:
    """Derives lifecycle assertions from DATA-071 without moving authority into it."""

    def pre_start(
        self,
        specification: AgentSpecification,
        *,
        manifest: Mapping[str, Any],
        context_envelope: Mapping[str, Any],
    ) -> RuntimeAssertionResult:
        checks: dict[str, bool] = {
            "specification_active": specification.status == "active",
            "agent_id_matches": manifest.get("agent_id") == specification.agent_id == "AGT-001",
            "graph_version_matches": manifest.get("graph") == {"id": "GRAPH-001", "version": "1.1.0"},
            "specification_digest_matches": manifest.get("agent_specification", {}).get("sha256") == specification.digest,
            "one_agent": manifest.get("agent_count") == 1,
            "memory_disabled": manifest.get("future_stage_flags", {}).get("memory_enabled") is False,
            "concurrency_disabled": manifest.get("future_stage_flags", {}).get("concurrent_graph_branches") is False,
            "multi_agent_disabled": manifest.get("future_stage_flags", {}).get("multiple_agents_enabled") is False,
        }
        try:
            enforce_context_profile(specification.raw["context_policy"], context_envelope)
            checks["context_policy_passed"] = True
        except ContextPolicyViolation:
            checks["context_policy_passed"] = False
        failures = tuple(name for name, passed in checks.items() if not passed)
        return RuntimeAssertionResult(not failures, "pre_start", checks, failures)

    def post_result(
        self,
        specification: AgentSpecification,
        *,
        result: Mapping[str, Any],
        persisted_result: Mapping[str, Any] | None = None,
    ) -> RuntimeAssertionResult:
        allowed_dispositions = {
            "preliminary_grounded_unapproved",
            "preliminary_grounded_human_approved",
            "preliminary_grounded_human_rejected",
        }
        status = result.get("status")
        disposition = result.get("final_disposition")
        review_outcome = result.get("review_outcome")
        checks: dict[str, bool] = {
            "known_status": status in {"waiting_for_human_review", "completed", "escalated", "terminated_guard"},
            "preliminary_disposition_only": disposition in allowed_dispositions,
            "timeout_never_approves": not (review_outcome in {"expired", "expired_escalated", "timeout"} and disposition == "preliminary_grounded_human_approved"),
            "approved_requires_human_outcome": disposition != "preliminary_grounded_human_approved" or review_outcome == "approved",
            "rejected_requires_human_outcome": disposition != "preliminary_grounded_human_rejected" or review_outcome == "rejected",
            "no_final_closure": result.get("final_legal_or_compliance_closure") is not True,
            "tool006_single_effect": int(result.get("tool006_effects", 0)) <= 1,
        }
        if persisted_result is not None:
            persisted_text = str(dict(persisted_result)).lower()
            checks["no_persisted_approval_token"] = "approval_token" not in persisted_text and "callback_token" not in persisted_text
        failures = tuple(name for name, passed in checks.items() if not passed)
        return RuntimeAssertionResult(not failures, "post_result", checks, failures)
