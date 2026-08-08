import pytest
from northstar_compliance.agent.budgets import BudgetExceeded, BudgetManager
from northstar_compliance.agent.models import AgentGoal, AgentRunState, ModelUsage, RuntimeBudget


def state(budget):
    return AgentRunState("1.1.0", "RUN-X", "AGT-001", AgentGoal("G", "P", "O"), budget=budget)


def test_088_token_budget_exhaustion():
    s = state(RuntimeBudget(max_total_tokens=10))
    bm = BudgetManager(s)
    with pytest.raises(BudgetExceeded, match="total_token_budget_exhausted"):
        bm.settle_model_usage(ModelUsage(8, 8))


def test_089_cost_budget_exhaustion():
    s = state(RuntimeBudget(max_cost_micro_cad=5))
    bm = BudgetManager(s)
    with pytest.raises(BudgetExceeded, match="cost_budget_exhausted"):
        bm.settle_model_usage(ModelUsage(2, 1))


def test_090_tool_call_budget_exhaustion():
    s = state(RuntimeBudget(max_tool_calls=1))
    bm = BudgetManager(s)
    bm.before_tool_call()
    with pytest.raises(BudgetExceeded, match="tool_call_budget_exhausted"):
        bm.before_tool_call()


def test_108_time_budget_exhaustion():
    s = state(RuntimeBudget(max_wall_time_ms=0))
    bm = BudgetManager(s)
    with pytest.raises(BudgetExceeded, match="time_budget_exhausted"):
        bm.before_iteration()
