from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timedelta, timezone

from northstar_compliance.approval.token import ApprovalTokenService
from northstar_compliance.durable.store import DurableStore, parse_utc
from northstar_compliance.graph.models import ReviewDecision


class ApprovalService:
    def __init__(self, store: DurableStore, tokens: ApprovalTokenService):
        self.store = store
        self.tokens = tokens

    def create_wait(self, *, run_id: str, review_request_id: str, initiated_by: str,
                    required_role: str, graph_id: str, graph_version: str,
                    now: datetime, timeout_seconds: int) -> tuple[dict, str]:
        wait_id = "WAIT-" + hashlib.sha256(f"{run_id}:{review_request_id}".encode()).hexdigest()[:16].upper()
        expires_at = now.astimezone(timezone.utc) + timedelta(seconds=timeout_seconds)
        token, claims = self.tokens.mint(
            wait_id=wait_id, run_id=run_id, review_request_id=review_request_id,
            graph_id=graph_id, graph_version=graph_version, required_role=required_role,
            expires_at=expires_at,
        )
        wait = self.store.ensure_wait(
            wait_id=wait_id, run_id=run_id, review_request_id=review_request_id,
            initiated_by=initiated_by, required_role=required_role, expires_at=expires_at,
            token_nonce=claims.nonce, token_digest=self.tokens.digest(token), now=now,
        )
        if wait["token_nonce"] != claims.nonce:
            token, claims = self.tokens.mint(
                wait_id=wait_id, run_id=run_id, review_request_id=review_request_id,
                graph_id=graph_id, graph_version=graph_version, required_role=required_role,
                expires_at=parse_utc(wait["expires_at"]),
            )
            self.store.rotate_wait_token(wait_id, claims.nonce, self.tokens.digest(token), now)
            wait = self.store.load_wait(wait_id=wait_id)
        return wait, token

    def submit(self, *, token: str, reviewer_id: str, reviewer_roles: list[str],
               decision: str, reason: str | None, now: datetime) -> ReviewDecision:
        claims = self.tokens.verify(token, now)
        wait = self.store.load_wait(wait_id=claims.wait_id)
        if claims.graph_id != "GRAPH-001" or claims.graph_version != "1.1.0":
            raise ValueError("token_graph_version_mismatch")
        if wait["review_request_id"] != claims.review_request_id or wait["run_id"] != claims.run_id:
            raise ValueError("token_wait_correlation_mismatch")
        record = ReviewDecision(
            schema_version="1.0.0",
            decision_id="DEC-" + uuid.uuid4().hex[:16].upper(),
            wait_id=claims.wait_id,
            run_id=claims.run_id,
            decision=decision,
            reviewer_id=reviewer_id,
            reviewer_roles=list(reviewer_roles),
            reason=reason,
            issued_at=now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            token_nonce=claims.nonce,
        )
        return self.store.record_decision(record, expected_token_digest=self.tokens.digest(token), now=now)
