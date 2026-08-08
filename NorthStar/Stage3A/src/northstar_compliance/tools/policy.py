from __future__ import annotations

from .models import (
    ImpactClass,
    ToolAuthorizationDecision,
    ToolDescriptor,
    ToolInvocationRequest,
)
from .utils import stable_id


class LocalToolPolicyEngine:
    """Deterministic tutorial PDP. Local claims are not enterprise authentication."""

    def decide(
        self, request: ToolInvocationRequest, descriptor: ToolDescriptor
    ) -> ToolAuthorizationDecision:
        reasons: list[str] = []
        principal = request.principal

        if not principal.principal_id.strip():
            reasons.append("missing_principal_id")
        if not principal.correlation_id.strip():
            reasons.append("missing_correlation_id")
        if not principal.groups:
            reasons.append("missing_groups")
        if principal.purpose not in descriptor.allowed_purposes:
            reasons.append("purpose_not_allowed")
        if principal.residency not in descriptor.allowed_residencies:
            reasons.append("residency_not_allowed")
        if not set(principal.groups).intersection(descriptor.allowed_groups):
            reasons.append("group_not_allowed")
        if descriptor.approval_required and not request.approval_reference:
            reasons.append("approval_required")
        if descriptor.impact_class in {
            ImpactClass.IRREVERSIBLE_WRITE,
            ImpactClass.PRIVILEGED_REGULATED,
        }:
            reasons.append("impact_class_prohibited_in_stage3a")

        allowed = not reasons
        payload = {
            "invocation_id": request.invocation_id,
            "tool_id": descriptor.tool_id,
            "version": descriptor.version,
            "principal": principal.principal_id,
            "allowed": allowed,
            "reasons": reasons,
        }
        obligations = {
            "max_result_bytes": descriptor.max_result_bytes,
            "timeout_ms": descriptor.timeout_ms,
            "idempotency_required": descriptor.idempotency_required,
            "authenticated_claims_warning": not principal.authenticated,
        }
        return ToolAuthorizationDecision(
            decision_id=stable_id("AUTHZ", payload),
            allowed=allowed,
            reason_codes=tuple(reasons) if reasons else ("allow",),
            obligations=obligations,
        )
