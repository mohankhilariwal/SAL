from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from threading import Lock

from .canonical import sha256_digest, sign_hmac, verify_hmac
from .models import AuthorityGrant
from .policy import HandoffPolicy


class AuthorityError(ValueError):
    pass


class GrantUseLedger:
    def __init__(self) -> None:
        self._lock = Lock()
        self._uses: dict[str, int] = {}
        self._nonces: set[str] = set()
        self._revoked: set[str] = set()

    def revoke(self, grant_id: str) -> None:
        with self._lock:
            self._revoked.add(grant_id)

    def consume(self, grant: AuthorityGrant, nonce: str) -> None:
        with self._lock:
            if grant.grant_id in self._revoked:
                raise AuthorityError("grant_revoked")
            if nonce in self._nonces:
                raise AuthorityError("nonce_replay")
            count = self._uses.get(grant.grant_id, 0)
            if count >= grant.max_uses:
                raise AuthorityError("grant_use_exhausted")
            self._uses[grant.grant_id] = count + 1
            self._nonces.add(nonce)


class AuthorityService:
    """Local HMAC reference model; not an OAuth, JWT, macaroon or DPoP implementation."""

    def __init__(self, issuer_secret: bytes, policy: HandoffPolicy, ledger: GrantUseLedger | None = None) -> None:
        if len(issuer_secret) < 32:
            raise ValueError("issuer_secret_too_short")
        self._secret = issuer_secret
        self.policy = policy
        self.ledger = ledger or GrantUseLedger()

    def mint(self, grant: AuthorityGrant) -> AuthorityGrant:
        self._validate_common(grant)
        unsigned = grant.unsigned()
        digest = sha256_digest(unsigned)
        signature = sign_hmac(replace(unsigned, digest_sha256=digest), self._secret)
        return replace(unsigned, digest_sha256=digest, signature=signature)

    def verify(self, grant: AuthorityGrant, *, now: datetime | None = None, audience: str | None = None) -> None:
        now = now or datetime.now(timezone.utc)
        self._validate_common(grant)
        expected_digest = sha256_digest(grant.unsigned())
        if grant.digest_sha256 != expected_digest:
            raise AuthorityError("grant_digest_mismatch")
        if not verify_hmac(replace(grant, signature=""), grant.signature, self._secret):
            raise AuthorityError("grant_signature_invalid")
        if now < grant.not_before:
            raise AuthorityError("grant_not_yet_valid")
        if now >= grant.expires_at:
            raise AuthorityError("grant_expired")
        if audience is not None and grant.audience != audience:
            raise AuthorityError("grant_audience_mismatch")

    def attenuate(self, parent: AuthorityGrant, child: AuthorityGrant) -> AuthorityGrant:
        self.verify(parent, now=child.not_before, audience=child.parent_subject_id or parent.subject_id)
        if child.parent_grant_digest != parent.digest_sha256:
            raise AuthorityError("parent_grant_digest_mismatch")
        if child.parent_subject_id != parent.subject_id:
            raise AuthorityError("parent_subject_mismatch")
        if child.case_id != parent.case_id or child.run_id != parent.run_id:
            raise AuthorityError("grant_scope_mismatch")
        if child.task_id != parent.task_id:
            raise AuthorityError("task_scope_mismatch")
        if child.purpose != parent.purpose:
            raise AuthorityError("purpose_escalation")
        self._assert_subset(child.allowed_tools, parent.allowed_tools, "tool_scope_escalation")
        self._assert_subset(child.allowed_operations, parent.allowed_operations, "operation_scope_escalation")
        self._assert_subset(child.allowed_resources, parent.allowed_resources, "resource_scope_escalation")
        self._assert_subset(child.allowed_data_scopes, parent.allowed_data_scopes, "data_scope_escalation")
        if child.risk_tier > parent.risk_tier:
            raise AuthorityError("risk_tier_escalation")
        if child.max_uses > parent.max_uses or child.max_uses > self.policy.max_grant_uses:
            raise AuthorityError("use_limit_escalation")
        if child.expires_at > parent.expires_at:
            raise AuthorityError("expiry_escalation")
        if child.not_before < parent.not_before:
            raise AuthorityError("not_before_escalation")
        expected_depth = parent.delegation_depth_remaining - 1
        if expected_depth < 0 or child.delegation_depth_remaining != expected_depth:
            raise AuthorityError("delegation_depth_invalid")
        return self.mint(child)

    def authorize_use(
        self,
        grant: AuthorityGrant,
        *,
        audience: str,
        nonce: str,
        tool_id: str | None = None,
        operation: str | None = None,
        resource: str | None = None,
        data_scope: str | None = None,
        now: datetime | None = None,
    ) -> None:
        self.verify(grant, now=now, audience=audience)
        if tool_id is not None and tool_id not in grant.allowed_tools:
            raise AuthorityError("tool_not_authorized")
        if operation is not None and operation not in grant.allowed_operations:
            raise AuthorityError("operation_not_authorized")
        if resource is not None and resource not in grant.allowed_resources:
            raise AuthorityError("resource_not_authorized")
        if data_scope is not None and data_scope not in grant.allowed_data_scopes:
            raise AuthorityError("data_scope_not_authorized")
        self.ledger.consume(grant, nonce)

    def revoke(self, grant_id: str) -> None:
        self.ledger.revoke(grant_id)

    def _validate_common(self, grant: AuthorityGrant) -> None:
        if grant.issuer != "CMP-007":
            raise AuthorityError("issuer_not_authoritative")
        if grant.max_uses < 1 or grant.max_uses > self.policy.max_grant_uses:
            raise AuthorityError("invalid_max_uses")
        if grant.delegation_depth_remaining < 0 or grant.delegation_depth_remaining > self.policy.max_delegation_depth:
            raise AuthorityError("invalid_delegation_depth")
        if grant.expires_at <= grant.not_before:
            raise AuthorityError("invalid_grant_window")
        if grant.purpose not in self.policy.allowed_purposes:
            raise AuthorityError("purpose_not_allowed")
        if len(set(grant.allowed_tools)) != len(grant.allowed_tools):
            raise AuthorityError("duplicate_tool_scope")

    @staticmethod
    def _assert_subset(child: tuple[str, ...], parent: tuple[str, ...], code: str) -> None:
        if not set(child).issubset(set(parent)):
            raise AuthorityError(code)
