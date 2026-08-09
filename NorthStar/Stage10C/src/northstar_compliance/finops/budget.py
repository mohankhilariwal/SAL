from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .models import money


class BudgetAction(StrEnum):
    ALLOW = "allow"
    WARN = "warn"
    REQUIRE_REVIEW = "require_review"
    STOP_BEFORE_START = "stop_before_start"
    CONTINUE_RECONCILIATION = "continue_reconciliation"


@dataclass(frozen=True)
class BudgetPolicy:
    soft_limit: Decimal
    hard_limit: Decimal
    currency: str = "CAD"
    protected_effect_in_progress_rule: str = "continue_reconciliation"
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if self.soft_limit < 0 or self.hard_limit < 0 or self.soft_limit > self.hard_limit:
            raise ValueError("invalid budget limits")
        if self.currency != "CAD":
            raise ValueError("Stage 10C example is denominated in CAD")


@dataclass(frozen=True)
class BudgetDecision:
    action: BudgetAction
    projected_cost: Decimal
    remaining: Decimal
    reason: str
    authority_effect: str = "none"


class BudgetEvaluator:
    def evaluate(self, policy: BudgetPolicy, spent: Decimal, projected_increment: Decimal, *, protected_effect_in_progress: bool) -> BudgetDecision:
        if spent < 0 or projected_increment < 0:
            raise ValueError("costs must be non-negative")
        projected = money(spent + projected_increment)
        remaining = money(policy.hard_limit - projected)
        if protected_effect_in_progress and projected > policy.hard_limit:
            return BudgetDecision(
                BudgetAction.CONTINUE_RECONCILIATION,
                projected,
                remaining,
                "budget cannot interrupt audit, outcome capture or reconciliation of an in-flight protected effect",
            )
        if projected > policy.hard_limit:
            return BudgetDecision(BudgetAction.STOP_BEFORE_START, projected, remaining, "hard budget exceeded before new work")
        if projected > policy.soft_limit:
            return BudgetDecision(BudgetAction.REQUIRE_REVIEW, projected, remaining, "soft budget exceeded")
        if projected >= policy.soft_limit * Decimal("0.8"):
            return BudgetDecision(BudgetAction.WARN, projected, remaining, "approaching soft limit")
        return BudgetDecision(BudgetAction.ALLOW, projected, remaining, "within budget")
