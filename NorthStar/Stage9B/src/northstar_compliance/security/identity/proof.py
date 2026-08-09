from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from .canonical import canonical_bytes, b64u, b64u_decode
from .crypto import Ed25519KeyPair
from .models import AuthorizationGrant, ProofOfPossession, ToolInvocationContext
from cryptography.exceptions import InvalidSignature


class ProofService:
    @staticmethod
    def _payload(*, proof_id: str, grant_id: str, key_thumbprint: str, method: str, audience: str, operation: str, resource: str, request_nonce: str, body_digest: str, issued_at: datetime) -> dict:
        return {
            "proof_id": proof_id, "grant_id": grant_id, "key_thumbprint": key_thumbprint,
            "method": method.upper(), "audience": audience, "operation": operation,
            "resource": resource, "request_nonce": request_nonce,
            "body_digest": body_digest,
            "issued_at": issued_at.astimezone(timezone.utc).isoformat().replace("+00:00","Z"),
        }

    @classmethod
    def create(cls, grant: AuthorizationGrant, context: ToolInvocationContext, key: Ed25519KeyPair, *, request_nonce: str | None = None, now: datetime | None = None) -> ProofOfPossession:
        now = now or datetime.now(timezone.utc)
        if key.thumbprint != grant.proof_key_thumbprint:
            raise ValueError("proof_key_not_bound_to_grant")
        proof_id = f"POP-{uuid4().hex.upper()}"
        nonce = request_nonce or uuid4().hex
        payload = cls._payload(proof_id=proof_id, grant_id=grant.grant_id, key_thumbprint=key.thumbprint,
            method=context.method, audience=context.audience, operation=context.operation,
            resource=context.resource, request_nonce=nonce, body_digest=context.body_digest, issued_at=now)
        signature = b64u(key._private.sign(canonical_bytes(payload)))
        return ProofOfPossession(
            proof_id=proof_id,
            grant_id=grant.grant_id,
            key_thumbprint=key.thumbprint,
            method=context.method.upper(),
            audience=context.audience,
            operation=context.operation,
            resource=context.resource,
            request_nonce=nonce,
            body_digest=context.body_digest,
            issued_at=now,
            signature=signature,
        )

    @classmethod
    def verify(cls, proof: ProofOfPossession, public_key: Ed25519PublicKey) -> bool:
        payload = cls._payload(proof_id=proof.proof_id, grant_id=proof.grant_id,
            key_thumbprint=proof.key_thumbprint, method=proof.method, audience=proof.audience,
            operation=proof.operation, resource=proof.resource, request_nonce=proof.request_nonce,
            body_digest=proof.body_digest, issued_at=proof.issued_at)
        try:
            public_key.verify(b64u_decode(proof.signature), canonical_bytes(payload))
            return True
        except (InvalidSignature, ValueError):
            return False
