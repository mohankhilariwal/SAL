from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .model_assist import advisory_classifier
from .models import GuardrailRequest, Outcome

ValidationResult = tuple[bool, str, str, Outcome]
Validator = Callable[[GuardrailRequest, dict[str, Any]], ValidationResult]


def _pass(code: str, summary: str = "control passed") -> ValidationResult:
    return True, code, summary, Outcome.ALLOW


def _fail(code: str, summary: str, outcome: Outcome = Outcome.DENY) -> ValidationResult:
    return False, code, summary, outcome


def input_size(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    size = len(str(req.payload.get("text", "")).encode("utf-8"))
    return _pass("INPUT_SIZE_OK") if size <= int(p.get("max_bytes", 1_000_000)) else _fail("INPUT_TOO_LARGE", "Input exceeds byte limit")


def allowed_content_type(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    allowed = set(p.get("allowed", ["text/plain", "text/markdown", "application/pdf"]))
    return _pass("CONTENT_TYPE_OK") if req.metadata.get("content_type", "text/plain") in allowed else _fail("CONTENT_TYPE_DENIED", "Content type is not allowed")


def no_secrets(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    text = str(req.payload.get("text", "")).lower()
    markers = tuple(p.get("markers", ["api_key=", "private key", "client_secret", "password="]))
    return _fail("SECRET_PATTERN", "Potential secret in input") if any(m.lower() in text for m in markers) else _pass("NO_SECRET_PATTERN")


def no_direct_injection(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    text = str(req.payload.get("text", "")).lower()
    patterns = tuple(p.get("patterns", ["ignore previous instructions", "reveal system prompt", "bypass authorization"]))
    return _fail("DIRECT_INJECTION", "Direct instruction-manipulation pattern", Outcome.QUARANTINE) if any(x in text for x in patterns) else _pass("NO_DIRECT_INJECTION")


def model_injection(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return advisory_classifier(req, mode="injection")


def tenant_case_bound(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    ok = bool(req.tenant_id and req.case_id and req.run_id and req.task_id)
    return _pass("EXECUTION_BINDING_OK") if ok else _fail("EXECUTION_BINDING_MISSING", "Tenant/case/run/task binding is incomplete")


def malware_clean(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    status = req.metadata.get("malware_status", "clean")
    return _pass("MALWARE_CLEAR") if status == "clean" else _fail("MALWARE_NOT_CLEARED", "Malware scan did not clear input", Outcome.QUARANTINE)


def provenance_complete(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    sources = req.payload.get("sources", [])
    ok = bool(sources) and all(s.get("source_id") and s.get("digest") for s in sources)
    return _pass("PROVENANCE_COMPLETE") if ok else _fail("PROVENANCE_MISSING", "Context source provenance is incomplete")


def untrusted_delimited(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("UNTRUSTED_CONTEXT_DELIMITED") if req.metadata.get("untrusted_content_delimited") is True else _fail("UNTRUSTED_CONTEXT_NOT_DELIMITED", "Untrusted context is not structurally isolated")


def no_instruction_elevation(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("NO_INSTRUCTION_ELEVATION") if req.metadata.get("context_instruction_elevation") is not True else _fail("CONTEXT_INSTRUCTION_ELEVATION", "Retrieved/source text attempted to become instructions", Outcome.QUARANTINE)


def context_budget(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    tokens = int(req.metadata.get("context_tokens", 0))
    return _pass("CONTEXT_BUDGET_OK") if tokens <= int(p.get("max_tokens", 12000)) else _fail("CONTEXT_BUDGET_EXCEEDED", "Context token budget exceeded")


def case_scope_match(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    scoped = req.metadata.get("context_case_id", req.case_id)
    return _pass("CASE_SCOPE_MATCH") if scoped == req.case_id else _fail("CROSS_CASE_CONTEXT", "Context belongs to another case")


def authorization_allowed(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("AUTHORIZATION_ALLOWED") if req.metadata.get("authorization_allowed") is True else _fail("AUTHORIZATION_DENIED", "AUTH-001 did not allow this request")


def tenant_scope_match(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("TENANT_SCOPE_MATCH") if req.metadata.get("resource_tenant_id", req.tenant_id) == req.tenant_id else _fail("CROSS_TENANT_SCOPE", "Resource tenant does not match execution tenant")


def result_limits(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    records = int(req.metadata.get("records", 0)); size = int(req.metadata.get("bytes", 0))
    ok = records <= int(p.get("max_records", 50)) and size <= int(p.get("max_bytes", 250000))
    return _pass("RETRIEVAL_LIMITS_OK") if ok else _fail("RETRIEVAL_LIMIT_EXCEEDED", "Retrieval result exceeds record/byte limits")


def citations_present(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("CITATIONS_PRESENT") if req.metadata.get("citation_count", 0) >= int(p.get("minimum", 1)) else _fail("CITATIONS_MISSING", "Retrieval result lacks required citations", Outcome.REQUIRE_HUMAN_REVIEW)


def index_freshness(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    age = int(req.metadata.get("index_age_hours", 0))
    return _pass("INDEX_FRESH") if age <= int(p.get("max_age_hours", 24)) else _fail("INDEX_STALE", "Index freshness SLO exceeded", Outcome.REQUIRE_HUMAN_REVIEW)


def allowed_plan_actions(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    allowed = set(p.get("allowed", [])); actions = set(req.payload.get("actions", []))
    return _pass("PLAN_ACTIONS_ALLOWED") if actions.issubset(allowed) else _fail("PLAN_ACTION_NOT_ALLOWED", "Plan contains an action outside the allowlist")


def no_policy_mutation(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _fail("POLICY_MUTATION_PROPOSED", "Agent plan attempted policy mutation") if "mutate_policy" in req.payload.get("actions", []) else _pass("NO_POLICY_MUTATION")


def no_agent_creation(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _fail("AGENT_CREATION_PROPOSED", "Plan attempted to create another agent") if "create_agent" in req.payload.get("actions", []) else _pass("NO_AGENT_CREATION")


def no_route_mutation(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _fail("ROUTE_MUTATION_PROPOSED", "Plan attempted route activation/change") if "activate_route" in req.payload.get("actions", []) else _pass("NO_ROUTE_MUTATION")


def plan_steps(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("PLAN_LENGTH_OK") if len(req.payload.get("steps", [])) <= int(p.get("max_steps", 12)) else _fail("PLAN_TOO_LONG", "Plan exceeds bounded step count")


def tier_within(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("PLAN_TIER_OK") if int(req.metadata.get("proposed_tier", 0)) <= int(req.metadata.get("authorized_tier", 0)) else _fail("PLAN_TIER_ESCALATION", "Plan exceeds authorized authority tier")


def blast_radius_allowed(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("BLAST_RADIUS_ALLOWED") if req.metadata.get("blast_radius_allowed") is True else _fail("BLAST_RADIUS_DENIED", "BR-001 budget did not allow this action")


def through_gateway(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("GATEWAY_PATH_OK") if req.metadata.get("gateway_id") == "CMP-005" else _fail("GATEWAY_BYPASS", "Tool request did not pass through CMP-005")


def tool_allowlisted(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("TOOL_ALLOWLIST_OK") if req.payload.get("tool_id") in set(p.get("allowed", [])) else _fail("TOOL_NOT_ALLOWLISTED", "Tool is outside the Stage 9C allowlist")


def tool_schema_valid(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("TOOL_SCHEMA_VALID") if req.metadata.get("tool_schema_valid") is True else _fail("TOOL_SCHEMA_INVALID", "Tool arguments/results failed typed validation")


def approval_satisfied(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    needed = bool(req.metadata.get("approval_required", False))
    ok = req.metadata.get("approval_verified") is True
    return _pass("APPROVAL_SATISFIED") if (not needed or ok) else _fail("APPROVAL_MISSING_OR_INVALID", "Required human approval is missing or invalid")


def protected_write_limit(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("PROTECTED_WRITE_LIMIT_OK") if int(req.metadata.get("concurrent_protected_writes", 0)) <= 1 else _fail("PROTECTED_WRITE_CONCURRENCY", "More than one protected write was requested")


def tool_result_untrusted(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("TOOL_RESULT_MARKED_UNTRUSTED") if req.metadata.get("tool_result_trusted_as_instruction") is not True else _fail("TOOL_RESULT_INSTRUCTION_ELEVATION", "Tool result was treated as trusted instructions", Outcome.QUARANTINE)


def output_schema_valid(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("OUTPUT_SCHEMA_VALID") if req.metadata.get("output_schema_valid") is True else _fail("OUTPUT_SCHEMA_INVALID", "Output failed the required schema")


def no_approval_claim(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    text = str(req.payload.get("text", "")).lower()
    markers = tuple(p.get("markers", ["case is approved", "final approval", "no human review required"]))
    return _fail("UNAUTHORIZED_APPROVAL_CLAIM", "Output falsely claims approval/finalization", Outcome.REQUIRE_HUMAN_REVIEW) if any(m in text for m in markers) else _pass("NO_APPROVAL_CLAIM")


def model_approval_claim(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return advisory_classifier(req, mode="approval")


def material_claim_citations(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("MATERIAL_CLAIMS_CITED") if req.metadata.get("material_claims_cited") is True else _fail("MATERIAL_CLAIMS_UNCITED", "Material claims are not linked to evidence", Outcome.REQUIRE_HUMAN_REVIEW)


def uncertainty_present(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("UNCERTAINTY_RECORDED") if req.metadata.get("uncertainty_recorded") is True else _fail("UNCERTAINTY_MISSING", "Required uncertainty statement is absent", Outcome.REQUIRE_HUMAN_REVIEW)


def no_cross_tenant_output(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("OUTPUT_TENANT_SCOPE_OK") if req.metadata.get("output_tenant_id", req.tenant_id) == req.tenant_id else _fail("CROSS_TENANT_OUTPUT", "Output contains another tenant's content")


def no_secret_output(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return no_secrets(req, p)


def state_owner(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("STATE_OWNER_OK") if req.metadata.get("state_owner") == "CMP-003" else _fail("STATE_OWNER_VIOLATION", "Protected state mutation owner is not CMP-003")


def no_data106_direct(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _fail("DATA106_DIRECT_MUTATION", "Guardrail/agent attempted direct DATA-106 mutation") if req.metadata.get("target_data_id") == "DATA-106" and req.metadata.get("via_cmp003") is not True else _pass("NO_DATA106_DIRECT_MUTATION")


def expected_version(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("EXPECTED_VERSION_MATCH") if req.metadata.get("expected_version") == req.metadata.get("current_version") else _fail("STALE_STATE_VERSION", "Optimistic concurrency version mismatch")


def idempotency_key(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("IDEMPOTENCY_KEY_PRESENT") if bool(req.metadata.get("idempotency_key")) else _fail("IDEMPOTENCY_KEY_MISSING", "Write lacks idempotency key")


def transition_allowed(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("STATE_TRANSITION_ALLOWED") if req.metadata.get("transition_allowed") is True else _fail("STATE_TRANSITION_DENIED", "State transition is not allowed by the case graph")


def memory_case_scope(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("MEMORY_CASE_SCOPE_OK") if req.payload.get("case_id") == req.case_id else _fail("CROSS_CASE_MEMORY_WRITE", "Memory write targets another case")


def memory_tenant_scope(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("MEMORY_TENANT_SCOPE_OK") if req.payload.get("tenant_id") == req.tenant_id else _fail("CROSS_TENANT_MEMORY_WRITE", "Memory write targets another tenant")


def memory_provenance(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("MEMORY_PROVENANCE_OK") if bool(req.payload.get("source_refs")) else _fail("MEMORY_PROVENANCE_MISSING", "Memory write lacks source references")


def no_memory_instructions(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("MEMORY_NOT_INSTRUCTION") if req.payload.get("record_type") != "instruction" else _fail("INSTRUCTION_MEMORY_PROHIBITED", "Untrusted/model-generated instructions cannot become long-term memory", Outcome.QUARANTINE)


def retention_set(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("MEMORY_RETENTION_SET") if req.payload.get("expires_at") else _fail("MEMORY_RETENTION_MISSING", "Memory record lacks expiry/retention")


def memory_consent(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    needed = bool(req.metadata.get("consent_required", False))
    return _pass("MEMORY_CONSENT_OK") if (not needed or req.metadata.get("consent_verified") is True) else _fail("MEMORY_CONSENT_MISSING", "Required memory consent is absent")


def reviewer_authenticated(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("REVIEWER_AUTHENTICATED") if bool(req.metadata.get("reviewer_id")) else _fail("REVIEWER_NOT_AUTHENTICATED", "Reviewer identity is missing")


def reviewer_role(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("REVIEWER_ROLE_OK") if req.metadata.get("reviewer_role") in set(p.get("allowed", [])) else _fail("REVIEWER_ROLE_DENIED", "Reviewer role is not eligible")


def separation_of_duties(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("SEPARATION_OF_DUTIES_OK") if req.metadata.get("reviewer_id") != req.metadata.get("requester_id") else _fail("SEPARATION_OF_DUTIES_VIOLATION", "Requester cannot approve their own action")


def review_digest(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("REVIEW_DIGEST_MATCH") if req.metadata.get("reviewed_digest") == req.metadata.get("current_digest") else _fail("REVIEW_DIGEST_MISMATCH", "Human reviewed a different payload/version")


def review_not_expired(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("REVIEW_NOT_EXPIRED") if req.metadata.get("review_expired") is not True else _fail("REVIEW_EXPIRED", "Human review has expired")


def timeout_never_approves(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _fail("TIMEOUT_APPROVAL_PROHIBITED", "Timeout cannot be interpreted as approval") if req.metadata.get("timed_out") is True and req.metadata.get("decision") == "approved" else _pass("TIMEOUT_NOT_APPROVAL")


def emergency_stop_clear(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    return _pass("EMERGENCY_STOP_CLEAR") if req.metadata.get("emergency_stop") is not True else _fail("EMERGENCY_STOP_ACTIVE", "Emergency stop is active")


def bundle_pinned(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    ok = bool(req.policy_bundle_id and req.policy_bundle_version and req.metadata.get("bundle_digest"))
    return _pass("POLICY_BUNDLE_PINNED") if ok else _fail("POLICY_BUNDLE_NOT_PINNED", "Run lacks an immutable policy bundle digest")


def high_impact_bundle_fresh(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    if int(req.metadata.get("authority_tier", 0)) < 3:
        return _pass("BUNDLE_FRESHNESS_NOT_HIGH_IMPACT")
    return _pass("HIGH_IMPACT_BUNDLE_FRESH") if req.metadata.get("bundle_stale") is not True else _fail("HIGH_IMPACT_STALE_POLICY", "High-impact action cannot use a stale policy bundle")


def stage8d_gate(req: GuardrailRequest, p: dict[str, Any]) -> ValidationResult:
    if req.metadata.get("operation") != "promote_to_production":
        return _pass("STAGE8D_GATE_NOT_APPLICABLE")
    return _pass("STAGE8D_GATE_RESOLVED") if req.metadata.get("stage8d_resolved") is True else _fail("STAGE8D_UNRESOLVED", "Production promotion remains blocked by unresolved Stage 8D")


VALIDATORS: dict[str, Validator] = {
    name: value for name, value in globals().copy().items()
    if callable(value) and name not in {"_pass", "_fail", "advisory_classifier"} and not name.startswith("_")
}
