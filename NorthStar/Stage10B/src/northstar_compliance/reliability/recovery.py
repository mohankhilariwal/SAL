from __future__ import annotations

from .models import EffectClass, FailureClass, FailureEnvelope, RecoveryAction, RecoveryDecision


class RecoveryPlanner:
    """Deterministic recovery policy; it never grants authority or approves work."""

    def decide(self, failure: FailureEnvelope) -> RecoveryDecision:
        fc = failure.failure_class
        if fc in {FailureClass.AUTHORIZATION, FailureClass.POLICY, FailureClass.SECURITY, FailureClass.AUDIT}:
            return RecoveryDecision(RecoveryAction.FAIL_CLOSED, f"{fc.value} failure cannot be bypassed")
        if fc is FailureClass.AUTHENTICATION:
            return RecoveryDecision(
                RecoveryAction.STOP,
                "expired or invalid credentials require a fresh grant from CMP-007",
                requires_reauthorization=True,
            )
        if fc is FailureClass.DATA_INTEGRITY:
            return RecoveryDecision(RecoveryAction.QUARANTINE, "corrupt state must be isolated and investigated")
        if fc is FailureClass.HUMAN_TIMEOUT:
            return RecoveryDecision(
                RecoveryAction.ESCALATE_HUMAN,
                "approval timeout remains pending; timeout never approves",
                requires_human=True,
            )
        if fc is FailureClass.OVERLOAD:
            return RecoveryDecision(RecoveryAction.SHED_LOAD, "protect dependencies and preserve bounded capacity")
        if failure.ambiguous or fc is FailureClass.AMBIGUOUS_OUTCOME:
            return RecoveryDecision(
                RecoveryAction.RECONCILE,
                "determine external outcome by idempotency reference before any repeat",
                requires_reconciliation=True,
            )
        if fc is FailureClass.TRANSIENT and failure.retryable:
            return RecoveryDecision(RecoveryAction.RETRY, "transient and explicitly retryable", may_retry=True)
        if fc is FailureClass.PERMANENT:
            return RecoveryDecision(RecoveryAction.DEAD_LETTER, "permanent failure requires correction before redrive")
        if failure.effect_class is EffectClass.READ_ONLY:
            return RecoveryDecision(RecoveryAction.DEGRADE_READ_ONLY, "return bounded partial result with limitations")
        return RecoveryDecision(RecoveryAction.STOP, "no safe automatic recovery action")
