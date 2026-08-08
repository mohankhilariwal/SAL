from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from .models import AgentSpecification, Finding, SpecificationValidationReport

SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_TOP_LEVEL = {
    "$schema",
    "specification_id",
    "version",
    "agent",
    "ownership",
    "purpose",
    "users",
    "goals",
    "non_goals",
    "contracts",
    "authority",
    "context_policy",
    "human_control",
    "termination",
    "errors",
    "operational_slos",
    "evaluation",
    "lifecycle",
    "traceability",
}

REQUIRED_INVARIANTS = {
    "exactly_one_agent",
    "graph_routes_are_application_owned",
    "all_tools_execute_through_cmp_005",
    "instructions_and_prompts_grant_no_authority",
    "authorization_precedes_context_loading",
    "timeout_never_approves",
    "late_decisions_fail_closed",
    "tool_006_effect_is_idempotent_and_single",
    "approved_and_rejected_dispositions_remain_preliminary",
    "memory_is_disabled",
    "concurrent_graph_branches_are_disabled",
    "multiple_agents_are_disabled",
}

ALLOWED_TOOL_IDS = {f"TOOL-{i:03d}" for i in range(1, 7)}
ALLOWED_CONTEXT_KINDS = {"publication", "evidence", "run_state", "policy_context"}
PROHIBITED_CONTEXT_KINDS = {"memory", "user_memory", "episodic_memory", "semantic_memory"}


class AgentSpecificationValidator:
    """Strict structural and semantic validator for DATA-071.

    This local validator intentionally enforces the subset used by the tutorial and
    supplements the JSON Schema artefact with cross-contract checks.
    """

    def validate(
        self,
        specification: AgentSpecification,
        *,
        manifest: Mapping[str, Any] | None = None,
    ) -> SpecificationValidationReport:
        raw = specification.raw
        findings: list[Finding] = []

        self._require_exact_keys(raw, EXPECTED_TOP_LEVEL, findings, "$")
        self._expect(raw.get("specification_id") == "AGT-001-spec", findings, "SPEC_ID", "specification_id must be AGT-001-spec", "$.specification_id")
        self._expect(bool(SEMVER.fullmatch(str(raw.get("version", "")))), findings, "SPEC_VERSION", "version must be semantic version", "$.version")

        agent = self._mapping(raw.get("agent"), findings, "$.agent")
        self._expect(agent.get("id") == "AGT-001", findings, "AGENT_ID", "agent.id must remain AGT-001", "$.agent.id")
        self._expect(agent.get("name") == "Regulatory Impact Assessment Agent", findings, "AGENT_NAME", "accepted agent name changed", "$.agent.name")
        self._expect(agent.get("graph") == {"id": "GRAPH-001", "version": "1.1.0"}, findings, "GRAPH_BINDING", "GRAPH-001 1.1.0 must be preserved", "$.agent.graph")

        ownership = self._mapping(raw.get("ownership"), findings, "$.ownership")
        for key in ("business_owner", "technical_owner", "risk_owner", "operations_owner"):
            self._expect(bool(str(ownership.get(key, "")).strip()), findings, "OWNER_REQUIRED", f"{key} is required", f"$.ownership.{key}")

        for list_key in ("users", "goals", "non_goals"):
            self._expect(self._non_empty_string_list(raw.get(list_key)), findings, "LIST_REQUIRED", f"{list_key} must be a non-empty string array", f"$.{list_key}")

        contracts = self._mapping(raw.get("contracts"), findings, "$.contracts")
        for key in ("inputs", "outputs", "preconditions", "postconditions", "invariants"):
            self._expect(self._non_empty_string_list(contracts.get(key)), findings, "CONTRACT_REQUIRED", f"contracts.{key} must be non-empty", f"$.contracts.{key}")
        invariants = set(contracts.get("invariants", [])) if isinstance(contracts.get("invariants"), list) else set()
        missing_invariants = sorted(REQUIRED_INVARIANTS - invariants)
        self._expect(not missing_invariants, findings, "INVARIANT_MISSING", f"missing invariants: {missing_invariants}", "$.contracts.invariants")

        authority = self._mapping(raw.get("authority"), findings, "$.authority")
        self._expect(authority.get("can_grant_authority") is False, findings, "AUTHORITY_GRANT", "agent cannot grant authority", "$.authority.can_grant_authority")
        self._expect(authority.get("can_approve_or_finalize") is False, findings, "AUTHORITY_APPROVE", "agent cannot approve or finalize", "$.authority.can_approve_or_finalize")
        self._expect(authority.get("can_delegate") is False, findings, "AUTHORITY_DELEGATE", "agent cannot delegate", "$.authority.can_delegate")
        self._expect(authority.get("can_create_agents") is False, findings, "AUTHORITY_CREATE_AGENT", "agent cannot create agents", "$.authority.can_create_agents")
        self._expect(authority.get("can_register_tools") is False, findings, "AUTHORITY_REGISTER_TOOL", "agent cannot register tools", "$.authority.can_register_tools")

        tools = authority.get("allowed_tools")
        if not isinstance(tools, list):
            findings.append(Finding("TOOLS_REQUIRED", "error", "authority.allowed_tools must be an array", "$.authority.allowed_tools"))
            tools = []
        tool_ids = {item.get("id") for item in tools if isinstance(item, Mapping)}
        self._expect(tool_ids == ALLOWED_TOOL_IDS, findings, "TOOL_ALLOWLIST", f"allowed tools must be exactly {sorted(ALLOWED_TOOL_IDS)}", "$.authority.allowed_tools")
        for index, tool in enumerate(tools):
            if not isinstance(tool, Mapping):
                findings.append(Finding("TOOL_OBJECT", "error", "tool entry must be an object", f"$.authority.allowed_tools[{index}]"))
                continue
            self._expect(tool.get("version") == "1.0.0", findings, "TOOL_VERSION", "tool version must be 1.0.0", f"$.authority.allowed_tools[{index}].version")
            self._expect(tool.get("via") == "INT-017/CMP-005", findings, "TOOL_GATEWAY", "all tools must use INT-017/CMP-005", f"$.authority.allowed_tools[{index}].via")
            self._expect(tool.get("impact") in {"read_only", "reversible_unapproved_write"}, findings, "TOOL_IMPACT", "unsupported tool impact", f"$.authority.allowed_tools[{index}].impact")

        context = self._mapping(raw.get("context_policy"), findings, "$.context_policy")
        allowed_kinds = set(context.get("allowed_kinds", [])) if isinstance(context.get("allowed_kinds"), list) else set()
        prohibited_kinds = set(context.get("prohibited_kinds", [])) if isinstance(context.get("prohibited_kinds"), list) else set()
        self._expect(allowed_kinds == ALLOWED_CONTEXT_KINDS, findings, "CONTEXT_ALLOWLIST", "context kinds changed", "$.context_policy.allowed_kinds")
        self._expect(PROHIBITED_CONTEXT_KINDS <= prohibited_kinds, findings, "MEMORY_PROHIBITION", "memory kinds must be prohibited", "$.context_policy.prohibited_kinds")
        self._expect(context.get("authorization_before_load") is True, findings, "ACCESS_ORDER", "authorization must precede loader invocation", "$.context_policy.authorization_before_load")
        self._expect(context.get("memory_enabled") is False, findings, "MEMORY_DISABLED", "memory must remain disabled", "$.context_policy.memory_enabled")
        self._expect(context.get("max_items") == 8, findings, "CONTEXT_ITEM_LIMIT", "max_items must remain 8", "$.context_policy.max_items")
        self._expect(context.get("max_characters") == 12000, findings, "CONTEXT_CHAR_LIMIT", "max_characters must remain 12000", "$.context_policy.max_characters")

        human = self._mapping(raw.get("human_control"), findings, "$.human_control")
        self._expect(human.get("external_decision_service") == "CMP-006", findings, "HUMAN_SERVICE", "human decisions remain external to CMP-006", "$.human_control.external_decision_service")
        self._expect(human.get("timeout_behavior") == "escalate_unapproved", findings, "TIMEOUT_BEHAVIOR", "timeout must escalate without approval", "$.human_control.timeout_behavior")
        self._expect(human.get("final_legal_or_compliance_closure") is False, findings, "FINAL_CLOSURE", "final legal/compliance closure is prohibited", "$.human_control.final_legal_or_compliance_closure")

        lifecycle = self._mapping(raw.get("lifecycle"), findings, "$.lifecycle")
        self._expect(lifecycle.get("status") in {"active", "deprecated", "retired"}, findings, "LIFECYCLE_STATUS", "invalid lifecycle status", "$.lifecycle.status")
        retirement = self._mapping(lifecycle.get("retirement"), findings, "$.lifecycle.retirement")
        self._expect(self._non_empty_string_list(retirement.get("criteria")), findings, "RETIREMENT_CRITERIA", "retirement criteria are required", "$.lifecycle.retirement.criteria")

        evaluation = self._mapping(raw.get("evaluation"), findings, "$.evaluation")
        self._expect(self._non_empty_string_list(evaluation.get("required_evaluations")), findings, "EVALUATIONS_REQUIRED", "required evaluations must be listed", "$.evaluation.required_evaluations")
        self._expect(evaluation.get("deployment_gate") == "deny_by_default", findings, "DEPLOYMENT_GATE", "deployment gate must deny by default", "$.evaluation.deployment_gate")

        traceability = self._mapping(raw.get("traceability"), findings, "$.traceability")
        self._expect(self._non_empty_string_list(traceability.get("requirements")), findings, "TRACE_REQUIREMENTS", "requirement traceability required", "$.traceability.requirements")
        self._expect(self._non_empty_string_list(traceability.get("controls")), findings, "TRACE_CONTROLS", "control traceability required", "$.traceability.controls")
        self._expect(self._non_empty_string_list(traceability.get("tests")), findings, "TRACE_TESTS", "test traceability required", "$.traceability.tests")

        if manifest is not None:
            self._validate_manifest_binding(specification, manifest, findings)

        return SpecificationValidationReport(
            valid=not any(f.severity == "error" for f in findings),
            specification_id=str(raw.get("specification_id")) if raw.get("specification_id") else None,
            specification_version=str(raw.get("version")) if raw.get("version") else None,
            digest=specification.digest,
            findings=tuple(findings),
        )

    def _validate_manifest_binding(self, specification: AgentSpecification, manifest: Mapping[str, Any], findings: list[Finding]) -> None:
        binding = self._mapping(manifest.get("agent_specification"), findings, "$.manifest.agent_specification")
        self._expect(binding.get("id") == specification.specification_id, findings, "MANIFEST_SPEC_ID", "manifest specification id mismatch", "$.manifest.agent_specification.id")
        self._expect(binding.get("version") == specification.version, findings, "MANIFEST_SPEC_VERSION", "manifest specification version mismatch", "$.manifest.agent_specification.version")
        digest = str(binding.get("sha256", ""))
        self._expect(bool(SHA256.fullmatch(digest)), findings, "MANIFEST_SPEC_HASH_FORMAT", "manifest specification hash must be SHA-256", "$.manifest.agent_specification.sha256")
        self._expect(digest == specification.digest, findings, "MANIFEST_SPEC_HASH", "manifest specification digest mismatch", "$.manifest.agent_specification.sha256")
        self._expect(manifest.get("agent_id") == "AGT-001", findings, "MANIFEST_AGENT", "manifest agent mismatch", "$.manifest.agent_id")
        self._expect(manifest.get("graph") == {"id": "GRAPH-001", "version": "1.1.0"}, findings, "MANIFEST_GRAPH", "manifest graph mismatch", "$.manifest.graph")
        future = self._mapping(manifest.get("future_stage_flags"), findings, "$.manifest.future_stage_flags")
        self._expect(future == {"memory_enabled": False, "concurrent_graph_branches": False, "multiple_agents_enabled": False}, findings, "FUTURE_FLAGS", "future-stage flags must remain disabled", "$.manifest.future_stage_flags")

    @staticmethod
    def _mapping(value: Any, findings: list[Finding], path: str) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            findings.append(Finding("OBJECT_REQUIRED", "error", "object required", path))
            return {}
        return value

    @staticmethod
    def _non_empty_string_list(value: Any) -> bool:
        return isinstance(value, Sequence) and not isinstance(value, (str, bytes)) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)

    @staticmethod
    def _expect(condition: bool, findings: list[Finding], code: str, message: str, path: str) -> None:
        if not condition:
            findings.append(Finding(code, "error", message, path))

    @staticmethod
    def _require_exact_keys(value: Mapping[str, Any], expected: set[str], findings: list[Finding], path: str) -> None:
        actual = set(value.keys())
        for missing in sorted(expected - actual):
            findings.append(Finding("REQUIRED_PROPERTY", "error", f"missing property: {missing}", path))
        for extra in sorted(actual - expected):
            findings.append(Finding("UNKNOWN_PROPERTY", "error", f"unknown property: {extra}", path))
