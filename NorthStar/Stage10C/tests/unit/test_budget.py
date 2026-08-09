from decimal import Decimal
from northstar_compliance.finops.budget import BudgetAction, BudgetEvaluator, BudgetPolicy


def policy(): return BudgetPolicy(Decimal("10"), Decimal("20"))

def test_1026_budget_allows_below_threshold(): assert BudgetEvaluator().evaluate(policy(), Decimal("1"), Decimal("1"), protected_effect_in_progress=False).action == BudgetAction.ALLOW

def test_1027_budget_warns_near_soft_limit(): assert BudgetEvaluator().evaluate(policy(), Decimal("8"), Decimal("0.5"), protected_effect_in_progress=False).action == BudgetAction.WARN

def test_1028_budget_requires_review_over_soft_limit(): assert BudgetEvaluator().evaluate(policy(), Decimal("9"), Decimal("2"), protected_effect_in_progress=False).action == BudgetAction.REQUIRE_REVIEW

def test_1029_budget_stops_new_work_over_hard_limit(): assert BudgetEvaluator().evaluate(policy(), Decimal("19"), Decimal("2"), protected_effect_in_progress=False).action == BudgetAction.STOP_BEFORE_START

def test_1030_budget_cannot_interrupt_reconciliation(): assert BudgetEvaluator().evaluate(policy(), Decimal("19"), Decimal("2"), protected_effect_in_progress=True).action == BudgetAction.CONTINUE_RECONCILIATION
