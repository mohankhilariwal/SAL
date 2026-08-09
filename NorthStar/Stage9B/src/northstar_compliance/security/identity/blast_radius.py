from __future__ import annotations
from threading import Lock
from .models import BlastRadiusBudget, BudgetConsumption, ToolInvocationContext


class BlastRadiusController:
    def __init__(self):
        self._consumption: dict[str,BudgetConsumption] = {}
        self._lock = Lock()

    def evaluate_and_reserve(self, budget: BlastRadiusBudget, context: ToolInvocationContext) -> list[str]:
        with self._lock:
            c=self._consumption.setdefault(budget.budget_id, BudgetConsumption())
            reasons=[]
            if budget.emergency_stop: reasons.append("emergency_stop_active")
            if context.tool_id not in budget.allowed_tools: reasons.append("tool_not_in_budget")
            if int(context.authority_tier) > int(budget.authority_tier_ceiling): reasons.append("budget_tier_exceeded")
            if context.region not in budget.region_allowlist: reasons.append("budget_region_not_allowed")
            if context.data_scope not in budget.data_scope_allowlist: reasons.append("budget_data_scope_not_allowed")
            if budget.reversible_only and int(context.authority_tier) >= 4: reasons.append("budget_reversible_only")
            if c.total_calls + 1 > budget.max_total_calls: reasons.append("budget_total_calls_exceeded")
            tool_limit=budget.per_tool_call_limits.get(context.tool_id,0)
            if c.per_tool_calls.get(context.tool_id,0)+1 > tool_limit: reasons.append("budget_tool_calls_exceeded")
            if c.records + context.record_count > budget.max_records: reasons.append("budget_records_exceeded")
            if c.bytes + context.byte_count > budget.max_bytes: reasons.append("budget_bytes_exceeded")
            if c.external_messages + context.external_messages > budget.max_external_messages: reasons.append("budget_external_messages_exceeded")
            if c.cost_cad + context.estimated_cost_cad > budget.max_cost_cad: reasons.append("budget_cost_exceeded")
            is_write=int(context.authority_tier)>=2
            if is_write and c.active_writes + 1 > budget.max_concurrent_writes: reasons.append("concurrent_write_limit_exceeded")
            if reasons: return reasons
            c.total_calls += 1
            c.per_tool_calls[context.tool_id]=c.per_tool_calls.get(context.tool_id,0)+1
            c.records += context.record_count
            c.bytes += context.byte_count
            c.external_messages += context.external_messages
            c.cost_cad += context.estimated_cost_cad
            if is_write: c.active_writes += 1
            return []

    def complete_write(self, budget_id: str) -> None:
        with self._lock:
            c=self._consumption.get(budget_id)
            if c and c.active_writes>0: c.active_writes -= 1

    def consumption(self, budget_id: str) -> BudgetConsumption:
        with self._lock:
            c=self._consumption.get(budget_id, BudgetConsumption())
            return BudgetConsumption(total_calls=c.total_calls, per_tool_calls=dict(c.per_tool_calls), records=c.records, bytes=c.bytes, external_messages=c.external_messages, cost_cad=c.cost_cad, active_writes=c.active_writes)
