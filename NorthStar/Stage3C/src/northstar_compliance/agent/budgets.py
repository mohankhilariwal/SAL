from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from .models import AgentRunState, ModelUsage

class BudgetExceeded(RuntimeError):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason

@dataclass(frozen=True)
class CostTariff:
    # Explicit tutorial assumption, not a vendor price.
    input_micro_cad_per_token: int = 2
    output_micro_cad_per_token: int = 6

class BudgetManager:
    def __init__(
        self,
        state: AgentRunState,
        *,
        clock: Callable[[], float] = time.monotonic,
        tariff: CostTariff = CostTariff(),
    ) -> None:
        self.state = state
        self.clock = clock
        self.tariff = tariff
        self._started = clock()
        self._prior_elapsed_ms = state.ledger.elapsed_ms

    def refresh_elapsed(self) -> None:
        self.state.ledger.elapsed_ms = self._prior_elapsed_ms + int((self.clock() - self._started) * 1000)

    def check_wall_time(self) -> None:
        self.refresh_elapsed()
        if self.state.ledger.elapsed_ms >= self.state.budget.max_wall_time_ms:
            raise BudgetExceeded("time_budget_exhausted")

    def before_iteration(self) -> None:
        self.check_wall_time()
        if self.state.ledger.iterations >= self.state.budget.max_iterations:
            raise BudgetExceeded("iteration_budget_exhausted")
        if self.state.ledger.model_calls >= self.state.budget.max_model_calls:
            raise BudgetExceeded("model_call_budget_exhausted")

    def settle_model_usage(self, usage: ModelUsage) -> None:
        self.state.ledger.model_calls += 1
        self.state.ledger.iterations += 1
        self.state.ledger.input_tokens += usage.input_tokens
        self.state.ledger.output_tokens += usage.output_tokens
        self.state.ledger.cost_micro_cad += (
            usage.input_tokens * self.tariff.input_micro_cad_per_token
            + usage.output_tokens * self.tariff.output_micro_cad_per_token
        )
        if self.state.ledger.input_tokens > self.state.budget.max_input_tokens:
            raise BudgetExceeded("input_token_budget_exhausted")
        if self.state.ledger.output_tokens > self.state.budget.max_output_tokens:
            raise BudgetExceeded("output_token_budget_exhausted")
        if self.state.ledger.input_tokens + self.state.ledger.output_tokens > self.state.budget.max_total_tokens:
            raise BudgetExceeded("total_token_budget_exhausted")
        if self.state.ledger.cost_micro_cad > self.state.budget.max_cost_micro_cad:
            raise BudgetExceeded("cost_budget_exhausted")
        self.check_wall_time()

    def before_tool_call(self) -> None:
        self.check_wall_time()
        if self.state.ledger.tool_calls >= self.state.budget.max_tool_calls:
            raise BudgetExceeded("tool_call_budget_exhausted")
        self.state.ledger.tool_calls += 1

    def record_failure(self) -> None:
        self.state.ledger.failures += 1
        if self.state.ledger.failures > self.state.budget.max_failures:
            raise BudgetExceeded("failure_budget_exhausted")

    def record_retry(self) -> None:
        self.state.ledger.retries += 1
        if self.state.ledger.retries > self.state.budget.max_retries:
            raise BudgetExceeded("retry_budget_exhausted")

    def record_replan(self) -> None:
        self.state.ledger.replans += 1
        if self.state.ledger.replans > self.state.budget.max_replans:
            raise BudgetExceeded("replan_budget_exhausted")
