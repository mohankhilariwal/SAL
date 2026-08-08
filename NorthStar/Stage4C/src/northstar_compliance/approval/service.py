from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any

from northstar_compliance.approval.token import ApprovalCallbackTokenClaims, ApprovalTokenService
from northstar_compliance.common.jsonutil import isoformat_utc, new_id
from northstar_compliance.durable.store import DurableStore, DurableStoreError


class ApprovalServiceError(RuntimeError):
    pass


class ApprovalService:
    """CMP-006 local durable approval contract; decisions remain external human facts."""

    def __init__(self, store: DurableStore, token_service: ApprovalTokenService):
        self.store = store
        self.tokens = token_service

    def create_wait(
        self,
        *,
        run_id: str,
        review_request_id: str,
        graph_id: str,
        graph_version: str,
        required_role: str,
        now: datetime,
        ttl_seconds: int,
    ) -> tuple[dict[str, Any], str]:
        wait_id = new_id("WAIT")
        nonce = secrets.token_urlsafe(18)
        claims = ApprovalCallbackTokenClaims(
            wait_id=wait_id,
            run_id=run_id,
            review_request_id=review_request_id,
            graph_id=graph_id,
            graph_version=graph_version,
            required_role=required_role,
            nonce=nonce,
            issued_at=isoformat_utc(now),
            expires_at=isoformat_utc(now + timedelta(seconds=ttl_seconds)),
        )
        token = self.tokens.issue(claims)
        wait = {
            "wait_id": wait_id,
            "run_id": run_id,
            "review_request_id": review_request_id,
            "required_role": required_role,
            "expires_at": claims.expires_at,
            "status": "pending",
            "token_digest": hashlib.sha256(token.encode("utf-8")).hexdigest(),
            "active_nonce": nonce,
            "updated_at": isoformat_utc(now),
        }
        self.store.create_wait(wait)
        return wait, token

    def submit(
        self,
        *,
        token: str,
        reviewer_id: str,
        reviewer_roles: list[str],
        decision: str,
        reason: str,
        initiator_id: str,
        now: datetime,
    ) -> dict[str, Any]:
        claims = self.tokens.verify(token, now)
        wait = self.store.get_wait(claims.wait_id)
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        checks = (
            (wait["run_id"] == claims.run_id, "run_mismatch"),
            (wait["review_request_id"] == claims.review_request_id, "review_request_mismatch"),
            (wait["required_role"] == claims.required_role, "role_claim_mismatch"),
            (wait["active_nonce"] == claims.nonce, "inactive_token"),
            (wait["token_digest"] == digest, "inactive_token"),
            (wait["status"] == "pending", "wait_not_pending"),
            (claims.required_role in reviewer_roles, "reviewer_role_required"),
            (reviewer_id != initiator_id, "separation_of_duties_violation"),
            (decision in {"approved", "rejected"}, "invalid_decision"),
            (decision != "rejected" or bool(reason.strip()), "rejection_reason_required"),
        )
        for ok, message in checks:
            if not ok:
                raise ApprovalServiceError(message)
        payload = {
            "schema_version": "1.0.0",
            "decision_id": new_id("DEC"),
            "wait_id": claims.wait_id,
            "run_id": claims.run_id,
            "review_request_id": claims.review_request_id,
            "reviewer_id": reviewer_id,
            "reviewer_roles": sorted(set(reviewer_roles)),
            "decision": decision,
            "reason": reason.strip(),
            "decided_at": isoformat_utc(now),
        }
        try:
            self.store.persist_decision(claims.wait_id, payload, expected_nonce=claims.nonce, now=isoformat_utc(now))
        except DurableStoreError as exc:
            raise ApprovalServiceError(str(exc)) from exc
        return payload
