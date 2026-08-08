from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


class TokenValidationError(ValueError):
    pass


def b64e(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64d(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def canonical(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass(frozen=True, slots=True)
class ApprovalTokenClaims:
    wait_id: str
    run_id: str
    review_request_id: str
    graph_id: str
    graph_version: str
    required_role: str
    exp: int
    nonce: str


class ApprovalTokenService:
    def __init__(self, secret: bytes):
        if len(secret) < 32:
            raise ValueError("approval_secret_must_be_at_least_32_bytes")
        self.secret = secret

    def mint(self, *, wait_id: str, run_id: str, review_request_id: str, graph_id: str,
             graph_version: str, required_role: str, expires_at: datetime) -> tuple[str, ApprovalTokenClaims]:
        claims = ApprovalTokenClaims(
            wait_id=wait_id, run_id=run_id, review_request_id=review_request_id,
            graph_id=graph_id, graph_version=graph_version, required_role=required_role,
            exp=int(expires_at.astimezone(timezone.utc).timestamp()), nonce=secrets.token_urlsafe(18),
        )
        payload = b64e(canonical(claims.__dict__ if hasattr(claims, '__dict__') else {
            'wait_id': claims.wait_id, 'run_id': claims.run_id, 'review_request_id': claims.review_request_id,
            'graph_id': claims.graph_id, 'graph_version': claims.graph_version, 'required_role': claims.required_role,
            'exp': claims.exp, 'nonce': claims.nonce,
        }))
        sig = b64e(hmac.new(self.secret, payload.encode("ascii"), hashlib.sha256).digest())
        return f"{payload}.{sig}", claims

    def verify(self, token: str, now: datetime) -> ApprovalTokenClaims:
        try:
            payload, sig = token.split(".", 1)
        except ValueError as exc:
            raise TokenValidationError("malformed_token") from exc
        expected = hmac.new(self.secret, payload.encode("ascii"), hashlib.sha256).digest()
        try:
            supplied = b64d(sig)
        except Exception as exc:
            raise TokenValidationError("malformed_signature") from exc
        if not hmac.compare_digest(expected, supplied):
            raise TokenValidationError("invalid_signature")
        try:
            raw = json.loads(b64d(payload))
            claims = ApprovalTokenClaims(**raw)
        except Exception as exc:
            raise TokenValidationError("invalid_claims") from exc
        if int(now.astimezone(timezone.utc).timestamp()) >= claims.exp:
            raise TokenValidationError("token_expired")
        return claims

    @staticmethod
    def digest(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
