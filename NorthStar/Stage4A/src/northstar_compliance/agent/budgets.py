from __future__ import annotations

import time
from dataclasses import dataclass

from .models import AgentRunState


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class BudgetManager:
    state: AgentRunState
    started_monotonic: float = 0.0

    def __post_init__(self) -> None:
        if not self.started_monotonic:
            self.started_monotonic = time.monotonic()

    def check_wall(self) -> None:
        if time.monotonic() - self.started_monotonic > self.state.budget.max_wall_seconds:
            raise BudgetExceeded("wall_time_budget_exhausted")

    def before_model(self) -> None:
        self.check_wall()
        l, b = self.state.ledger, self.state.budget
        if l.iterations >= b.max_iterations:
            raise BudgetExceeded("iteration_budget_exhausted")
        if l.model_calls >= b.max_model_calls:
            raise BudgetExceeded("model_call_budget_exhausted")
        l.iterations += 1
        l.model_calls += 1

    def settle_model(self, input_tokens: int, output_tokens: int) -> None:
        l, b = self.state.ledger, self.state.budget
        l.input_tokens += input_tokens
        l.output_tokens += output_tokens
        l.cost_micro_cad += 2 * input_tokens + 6 * output_tokens
        if l.input_tokens > b.max_input_tokens:
            raise BudgetExceeded("input_token_budget_exhausted")
        if l.output_tokens > b.max_output_tokens:
            raise BudgetExceeded("output_token_budget_exhausted")
        if l.input_tokens + l.output_tokens > b.max_total_tokens:
            raise BudgetExceeded("total_token_budget_exhausted")
        if l.cost_micro_cad > b.max_cost_micro_cad:
            raise BudgetExceeded("cost_budget_exhausted")

    def before_tool(self) -> None:
        self.check_wall()
        if self.state.ledger.tool_calls >= self.state.budget.max_tool_calls:
            raise BudgetExceeded("tool_call_budget_exhausted")
        self.state.ledger.tool_calls += 1

    def failure(self) -> None:
        self.state.ledger.failures += 1
        if self.state.ledger.failures > self.state.budget.max_failures:
            raise BudgetExceeded("failure_budget_exhausted")

    def retry(self) -> None:
        self.state.ledger.retries += 1
        if self.state.ledger.retries > self.state.budget.max_retries:
            raise BudgetExceeded("retry_budget_exhausted")
