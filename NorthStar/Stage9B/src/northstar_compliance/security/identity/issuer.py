from __future__ import annotations
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from .crypto import Ed25519KeyPair, SignedEnvelope
from .models import AgentExecutionIdentity, ApprovalBinding, AuthorizationGrant


class GrantError(ValueError):
    pass


class GrantIssuer:
    ISSUER = "CMP-007"

    def __init__(self, signing_key: Ed25519KeyPair):
        self.signing_key = signing_key

    def issue(
        self,
        execution: AgentExecutionIdentity,
        *,
        human_actor_id: str,
        workload_principal_id: str,
        purpose: str,
        audience: str,
        intended_tool: str,
        operations: tuple[str, ...],
        resource_prefixes: tuple[str, ...],
        data_scopes: tuple[str, ...],
        region_allowlist: tuple[str, ...],
        max_authority_tier: int,
        max_uses: int,
        max_tool_calls: int,
        max_records: int,
        max_bytes: int,
        max_external_messages: int,
        monetary_limit_cad: float,
        reversible_only: bool,
        approval: ApprovalBinding,
        proof_key_thumbprint: str,
        ttl_seconds: int = 120,
        now: datetime | None = None,
    ) -> tuple[AuthorizationGrant, SignedEnvelope]:
        now = now or datetime.now(timezone.utc)
        if ttl_seconds <= 0 or ttl_seconds > 300:
            raise GrantError("ttl_seconds_out_of_range")
        if human_actor_id != execution.human_subject_id:
            raise GrantError("human_actor_execution_mismatch")
        if workload_principal_id != execution.workload_principal_id:
            raise GrantError("workload_execution_mismatch")
        if max_uses < 1 or max_tool_calls < 1:
            raise GrantError("use_limits_must_be_positive")
        grant = AuthorizationGrant(
            grant_id=f"GRANT-{uuid4().hex.upper()}", issuer=self.ISSUER,
            subject_execution_id=execution.execution_id,
            human_actor_id=human_actor_id, workload_principal_id=workload_principal_id,
            tenant_id=execution.tenant_id, case_id=execution.case_id,
            run_id=execution.run_id, task_id=execution.task_id, purpose=purpose,
            audience=audience, intended_tool=intended_tool,
            operations=tuple(sorted(set(operations))),
            resource_prefixes=tuple(sorted(set(resource_prefixes))),
            data_scopes=tuple(sorted(set(data_scopes))),
            region_allowlist=tuple(sorted(set(region_allowlist))),
            max_authority_tier=max_authority_tier, max_uses=max_uses,
            max_tool_calls=max_tool_calls, max_records=max_records,
            max_bytes=max_bytes, max_external_messages=max_external_messages,
            monetary_limit_cad=monetary_limit_cad, reversible_only=reversible_only,
            delegation_depth=0, max_delegation_depth=0, approval=approval,
            proof_key_thumbprint=proof_key_thumbprint, issued_at=now,
            not_before=now, expires_at=now + timedelta(seconds=ttl_seconds),
            nonce=uuid4().hex, parent_grant_id=None,
            revocation_ref=f"REV-{uuid4().hex.upper()}",
        )
        return grant, self.signing_key.sign(asdict(grant))

    def attenuate(self, parent: AuthorizationGrant, **changes) -> AuthorizationGrant:
        data = asdict(parent)
        data.update(changes)
        child = AuthorizationGrant(**data)
        if child.delegation_depth != parent.delegation_depth + 1:
            raise GrantError("invalid_delegation_depth")
        if child.delegation_depth > parent.max_delegation_depth:
            raise GrantError("delegation_depth_exceeded")
        for name in ("operations", "resource_prefixes", "data_scopes", "region_allowlist"):
            if not set(getattr(child, name)).issubset(set(getattr(parent, name))):
                raise GrantError(f"{name}_not_attenuated")
        for name in ("max_authority_tier", "max_uses", "max_tool_calls", "max_records", "max_bytes", "max_external_messages", "monetary_limit_cad"):
            if getattr(child, name) > getattr(parent, name):
                raise GrantError(f"{name}_expanded")
        if child.expires_at > parent.expires_at:
            raise GrantError("expiry_expanded")
        if parent.reversible_only and not child.reversible_only:
            raise GrantError("reversibility_expanded")
        return child
