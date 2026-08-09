from __future__ import annotations
from dataclasses import asdict
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from .crypto import SignedEnvelope, Ed25519KeyPair
from .models import AuthorizationGrant, BlastRadiusBudget, PolicyDecision, ProofOfPossession, ToolInvocationContext
from .proof import ProofService
from .ledgers import RevocationLedger, UseLedger, ProofNonceLedger
from .policy import AuthorizationPolicy
from .blast_radius import BlastRadiusController


class ToolAuthorizationGateway:
    """Receiver-side PEP for CMP-005. It authorizes; it does not execute tools or mutate DATA-106."""
    def __init__(self, issuer_public_key: Ed25519PublicKey, proof_public_keys: dict[str,Ed25519PublicKey], *, revocations=None, uses=None, proof_nonces=None, policy=None, blast=None):
        self.issuer_public_key=issuer_public_key
        self.proof_public_keys=proof_public_keys
        self.revocations=revocations or RevocationLedger()
        self.uses=uses or UseLedger()
        self.proof_nonces=proof_nonces or ProofNonceLedger()
        self.policy=policy or AuthorizationPolicy()
        self.blast=blast or BlastRadiusController()

    def authorize(self, grant: AuthorizationGrant, envelope: SignedEnvelope, proof: ProofOfPossession, context: ToolInvocationContext, budget: BlastRadiusBudget, *, now: datetime | None=None) -> PolicyDecision:
        now=now or datetime.now(timezone.utc)
        reasons=[]
        if envelope.payload != asdict(grant): reasons.append("grant_payload_mismatch")
        if not Ed25519KeyPair.verify(envelope, self.issuer_public_key): reasons.append("invalid_grant_signature")
        if self.revocations.is_revoked(grant.grant_id): reasons.append("grant_revoked")
        reasons.extend(self.policy.evaluate(grant, context, now=now))
        if proof.grant_id != grant.grant_id: reasons.append("proof_grant_mismatch")
        if proof.key_thumbprint != grant.proof_key_thumbprint: reasons.append("proof_thumbprint_mismatch")
        proof_bindings={
            "proof_method_mismatch": (proof.method.upper(), context.method.upper()),
            "proof_audience_mismatch": (proof.audience, context.audience),
            "proof_operation_mismatch": (proof.operation, context.operation),
            "proof_resource_mismatch": (proof.resource, context.resource),
            "proof_body_digest_mismatch": (proof.body_digest, context.body_digest),
        }
        for code,(a,b) in proof_bindings.items():
            if a != b: reasons.append(code)
        if abs((now-proof.issued_at).total_seconds()) > 30: reasons.append("proof_outside_time_window")
        key=self.proof_public_keys.get(proof.key_thumbprint)
        if key is None or not ProofService.verify(proof,key): reasons.append("invalid_proof_signature")
        # Stateful checks occur only after all stateless checks pass to avoid consuming valid rights on malformed requests.
        if not reasons:
            if not self.proof_nonces.consume(grant.grant_id, proof.request_nonce): reasons.append("proof_replay")
        if not reasons:
            if not self.uses.consume(grant.grant_id, grant.max_uses): reasons.append("grant_use_limit_exceeded")
        if not reasons:
            reasons.extend(self.blast.evaluate_and_reserve(budget,context))
        return PolicyDecision(
            decision_id=f"AUTHZ-{uuid4().hex.upper()}", allowed=not reasons,
            reason_codes=tuple(sorted(set(reasons))), grant_id=grant.grant_id,
            budget_id=budget.budget_id, evaluated_at=now,
        )
