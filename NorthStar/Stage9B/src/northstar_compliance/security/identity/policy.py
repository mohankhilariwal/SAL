from __future__ import annotations
from datetime import datetime, timezone, timedelta
from .models import AuthorizationGrant, ToolInvocationContext, ApprovalStatus


TOOL_TIERS = {
    "TOOL-001": 1, "TOOL-002": 1, "TOOL-003": 1,
    "TOOL-004": 2, "TOOL-005": 2, "TOOL-006": 3,
}
TOOL_OPERATIONS = {
    "TOOL-001": {"search_regulatory_sources"},
    "TOOL-002": {"retrieve_internal_policies"},
    "TOOL-003": {"query_control_repository"},
    "TOOL-004": {"create_draft_impact_assessment"},
    "TOOL-005": {"save_case_draft"},
    "TOOL-006": {"send_review_request"},
}


class AuthorizationPolicy:
    def evaluate(self, grant: AuthorizationGrant, context: ToolInvocationContext, *, now: datetime | None = None) -> list[str]:
        now = now or datetime.now(timezone.utc)
        reasons=[]
        if grant.issuer != "CMP-007": reasons.append("issuer_mismatch")
        if now < grant.not_before: reasons.append("grant_not_yet_valid")
        if now >= grant.expires_at: reasons.append("grant_expired")
        if grant.expires_at - grant.issued_at > timedelta(minutes=5): reasons.append("grant_ttl_exceeds_policy")
        bindings = {
            "tenant_mismatch": (grant.tenant_id, context.tenant_id),
            "case_mismatch": (grant.case_id, context.case_id),
            "run_mismatch": (grant.run_id, context.run_id),
            "task_mismatch": (grant.task_id, context.task_id),
            "execution_mismatch": (grant.subject_execution_id, context.execution_id),
            "human_actor_mismatch": (grant.human_actor_id, context.human_actor_id),
            "workload_mismatch": (grant.workload_principal_id, context.workload_principal_id),
            "audience_mismatch": (grant.audience, context.audience),
            "tool_mismatch": (grant.intended_tool, context.tool_id),
        }
        for code,(a,b) in bindings.items():
            if a != b: reasons.append(code)
        if context.operation not in grant.operations: reasons.append("operation_not_granted")
        if context.operation not in TOOL_OPERATIONS.get(context.tool_id,set()): reasons.append("operation_not_tool_contract")
        if not any(context.resource.startswith(prefix) for prefix in grant.resource_prefixes): reasons.append("resource_out_of_scope")
        if context.data_scope not in grant.data_scopes: reasons.append("data_scope_out_of_scope")
        if context.region not in grant.region_allowlist: reasons.append("region_not_allowed")
        if int(context.authority_tier) > grant.max_authority_tier: reasons.append("authority_tier_exceeded")
        if int(context.authority_tier) != TOOL_TIERS.get(context.tool_id,99): reasons.append("tool_tier_mismatch")
        if context.record_count > grant.max_records: reasons.append("record_limit_exceeded")
        if context.byte_count > grant.max_bytes: reasons.append("byte_limit_exceeded")
        if context.external_messages > grant.max_external_messages: reasons.append("external_message_limit_exceeded")
        if context.estimated_cost_cad > grant.monetary_limit_cad: reasons.append("monetary_limit_exceeded")
        if grant.reversible_only and int(context.authority_tier) >= 4: reasons.append("irreversible_action_prohibited")
        if int(context.authority_tier) == 4:
            if grant.approval.status != ApprovalStatus.APPROVED:
                reasons.append("high_impact_requires_approval")
            if grant.approval.expires_at is not None and now >= grant.approval.expires_at:
                reasons.append("approval_expired")
            if grant.approval.required_count < 2 or len(set(grant.approval.approver_subject_ids)) < 2: reasons.append("dual_control_required")
        if int(context.authority_tier) >= 5: reasons.append("prohibited_autonomous_action")
        return reasons
