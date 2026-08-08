from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from northstar_compliance.common.jsonutil import canonical_json, parse_utc


class ApprovalTokenError(RuntimeError):
    pass


def _b64e(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64d(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


@dataclass(frozen=True)
class ApprovalCallbackTokenClaims:
    wait_id: str
    run_id: str
    review_request_id: str
    graph_id: str
    graph_version: str
    required_role: str
    nonce: str
    issued_at: str
    expires_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ApprovalTokenService:
    def __init__(self, secret: bytes):
        if len(secret) < 32:
            raise ValueError("approval secret must be at least 32 bytes")
        self._secret = secret

    def issue(self, claims: ApprovalCallbackTokenClaims) -> str:
        body = _b64e(canonical_json(claims.to_dict()).encode("utf-8"))
        sig = _b64e(hmac.new(self._secret, body.encode("ascii"), hashlib.sha256).digest())
        return f"{body}.{sig}"

    def verify(self, token: str, now: datetime) -> ApprovalCallbackTokenClaims:
        try:
            body, sig = token.split(".", 1)
            expected = _b64e(hmac.new(self._secret, body.encode("ascii"), hashlib.sha256).digest())
            if not hmac.compare_digest(sig, expected):
                raise ApprovalTokenError("invalid_signature")
            data = json.loads(_b64d(body).decode("utf-8"))
            claims = ApprovalCallbackTokenClaims(**data)
        except ApprovalTokenError:
            raise
        except Exception as exc:
            raise ApprovalTokenError("malformed_token") from exc
        if parse_utc(claims.expires_at) <= now:
            raise ApprovalTokenError("token_expired")
        return claims
