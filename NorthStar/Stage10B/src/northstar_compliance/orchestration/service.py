from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from northstar_compliance.reliability.models import FailureEnvelope
from northstar_compliance.reliability.recovery import RecoveryPlanner


@dataclass
class ReliabilityService:
    planner: RecoveryPlanner

    def handle_failure(self, failure: FailureEnvelope) -> dict[str, Any]:
        decision = self.planner.decide(failure)
        return {
            "failure_id": failure.failure_id,
            "action": decision.action.value,
            "reason": decision.reason,
            "requires_reauthorization": decision.requires_reauthorization,
            "requires_reconciliation": decision.requires_reconciliation,
            "requires_human": decision.requires_human,
            "authority_effect": "none",
        }
