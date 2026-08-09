from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from northstar_compliance.audit.port import AuditPort


class InvalidGrant(PermissionError):
    pass


@dataclass
class EnterpriseIntegrationGateway:
    """CMP-005 local reference. It is the only protected-effect gateway."""

    audit: AuditPort
    applied: dict[str, dict[str, Any]] = field(default_factory=dict)

    def protected_write(
        self,
        *,
        operation: str,
        payload: dict[str, Any],
        idempotency_key: str,
        grant: dict[str, Any],
    ) -> dict[str, Any]:
        if grant.get("issuer") != "CMP-007" or grant.get("operation") != operation or not grant.get("valid"):
            raise InvalidGrant("valid scoped CMP-007 grant required")
        if idempotency_key in self.applied:
            return {**self.applied[idempotency_key], "deduplicated": True}

        self.audit.append(
            "protected_effect_intent",
            {"operation": operation, "idempotency_key": idempotency_key, "grant_id": grant.get("grant_id")},
        )
        outcome = {"operation": operation, "status": "applied", "idempotency_key": idempotency_key}
        self.applied[idempotency_key] = outcome
        self.audit.append("protected_effect_outcome", outcome)
        return {**outcome, "deduplicated": False}

    def reconcile(self, idempotency_key: str) -> dict[str, Any]:
        result = self.applied.get(idempotency_key)
        return {"found": result is not None, "outcome": result, "authority_effect": "none"}
