from __future__ import annotations

from dataclasses import asdict
from typing import Callable

from .budgets import BudgetExceeded, BudgetManager
from .cancellation import CancellationToken
from .models import AgentRunState, RecoveryRecord
from northstar_compliance.tools.gateway import ToolGateway, ToolInvocationRequest, ToolResult

class RecoveryManager:
    def __init__(
        self,
        gateway: ToolGateway,
        budget: BudgetManager,
        state: AgentRunState,
        *,
        reconciler: Callable[[str, str], dict | None],
        sleeper: Callable[[float], None] = lambda _s: None,
    ) -> None:
        self.gateway = gateway
        self.budget = budget
        self.state = state
        self.reconciler = reconciler
        self.sleeper = sleeper

    def execute(self, request: ToolInvocationRequest, token: CancellationToken) -> ToolResult:
        impact = self.gateway.impact(request.tool_id)
        attempt = 0
        used_fallback = False
        while True:
            token.raise_if_cancelled()
            self.budget.before_tool_call()
            result = self.gateway.invoke(request, token, use_fallback=used_fallback)
            if result.status == "success":
                if used_fallback:
                    return ToolResult(status="success", payload=result.payload, adapter=result.adapter)
                return result

            failure = result.failure
            if failure is None:
                return result
            self.budget.record_failure()

            if failure.kind == "ambiguous_write":
                return self._reconcile_ambiguous_write(request, failure)

            if failure.kind in {"authorization", "validation", "permanent"}:
                return result

            # Write retries are allowed only when the gateway states the call did not dispatch/commit.
            safe_write_retry = impact == "reversible_write" and failure.committed is False and failure.stage == "before_dispatch"
            safe_read_retry = impact == "read_only" and failure.retryable

            if not (safe_read_retry or safe_write_retry):
                return result

            attempt += 1
            self.budget.record_retry()

            self.state.recovery_records.append(asdict(RecoveryRecord(
                action="retry",
                reason=failure.code,
                attempt=attempt,
                tool_id=request.tool_id,
                outcome="scheduled",
            )))

            # One bounded fallback is permitted for read-only tools after the first primary failure.
            if impact == "read_only" and request.tool_id in self.gateway.fallback_adapters and not used_fallback:
                used_fallback = True
                self.state.recovery_records.append(asdict(RecoveryRecord(
                    action="tool_fallback",
                    reason=failure.code,
                    attempt=attempt,
                    tool_id=request.tool_id,
                    outcome="selected",
                )))
            else:
                self.sleeper(min(0.05 * (2 ** (attempt - 1)), 0.5))

    def _reconcile_ambiguous_write(self, request: ToolInvocationRequest, failure) -> ToolResult:
        key = request.idempotency_key
        self.state.recovery_records.append(asdict(RecoveryRecord(
            action="reconcile_write",
            reason=failure.code,
            attempt=1,
            tool_id=request.tool_id,
            outcome="query_by_idempotency_key",
        )))
        if not key:
            return ToolResult(status="error", failure=failure)
        found = self.reconciler(request.tool_id, key)
        if found is None:
            # Unknown remains unknown. Do not guess and do not blindly retry.
            self.state.recovery_records.append(asdict(RecoveryRecord(
                action="reconcile_write",
                reason="no_authoritative_status",
                attempt=1,
                tool_id=request.tool_id,
                outcome="unresolved",
            )))
            return ToolResult(status="error", failure=failure)
        self.state.recovery_records.append(asdict(RecoveryRecord(
            action="reconcile_write",
            reason="artifact_found",
            attempt=1,
            tool_id=request.tool_id,
            outcome="committed",
        )))
        payload = dict(found)
        payload["_reconciled"] = True
        return ToolResult(status="success", payload=payload, adapter="reconciler")
