from __future__ import annotations

import hashlib

from .models import ToolAuthorizationDecision, ToolInvocationRequest
from .registry import ToolDescriptor


class LocalToolPolicyEngine:
    """Tutorial-only deterministic PDP over unauthenticated local claims."""

    def decide(self, request: ToolInvocationRequest, descriptor: ToolDescriptor) -> ToolAuthorizationDecision:
        material = f"{request.principal.correlation_id}|{request.tool_id}|{request.tool_version}|{request.principal.principal_id}"
        decision_id = "TPD-" + hashlib.sha256(material.encode()).hexdigest()[:16].upper()
        p = request.principal
        reasons: list[str] = []
        if not p.principal_id or not p.correlation_id:
            reasons.append("missing_principal_or_correlation")
        if not set(p.groups).intersection(descriptor.raw["allowed_groups"]):
            reasons.append("group_not_allowed")
        if p.purpose not in descriptor.raw["allowed_purposes"]:
            reasons.append("purpose_not_allowed")
        if p.residency not in descriptor.raw["allowed_residencies"]:
            reasons.append("residency_not_allowed")
        if descriptor.impact_class == "reversible_write":
            if request.tool_id not in p.write_scopes:
                reasons.append("write_scope_missing")
            if descriptor.raw["idempotency_required"] and not request.idempotency_key:
                reasons.append("idempotency_key_required")
        allowed = not reasons
        obligations = ("claims_unauthenticated_local_only", "emit_execution_evidence")
        return ToolAuthorizationDecision(
            decision_id=decision_id,
            allowed=allowed,
            reason="allowed" if allowed else ",".join(reasons),
            obligations=obligations,
            authenticated_claims=False,
        )
