from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Protocol

from northstar_compliance.harness.models import HookResult


class HookError(RuntimeError):
    pass


class LifecycleHook(Protocol):
    name: str
    required: bool

    def handle(self, lifecycle_event: str, payload: dict[str, Any]) -> HookResult: ...


@dataclass
class InvariantEvaluationHook:
    name: str = "invariant_evaluation"
    required: bool = True

    def handle(self, lifecycle_event: str, payload: dict[str, Any]) -> HookResult:
        findings: list[str] = []
        if payload.get("agent_ids") not in (None, ["AGT-001"]):
            findings.append("one_agent_invariant_failed")
        if payload.get("memory_enabled") is True:
            findings.append("memory_must_remain_disabled")
        if payload.get("multiple_agents_enabled") is True:
            findings.append("multiple_agents_must_remain_disabled")
        disposition = payload.get("disposition")
        if isinstance(disposition, str) and disposition.startswith("final_"):
            findings.append("final_disposition_prohibited")
        return HookResult(
            schema_version="1.0.0",
            hook_name=self.name,
            lifecycle_event=lifecycle_event,
            status="failed" if findings else "passed",
            findings=tuple(findings),
        )


class HookManager:
    def __init__(self, hooks: list[LifecycleHook]):
        self.hooks = tuple(hooks)

    def emit(self, lifecycle_event: str, payload: dict[str, Any]) -> tuple[HookResult, ...]:
        results: list[HookResult] = []
        for hook in self.hooks:
            try:
                result = hook.handle(lifecycle_event, copy.deepcopy(payload))
            except Exception as exc:
                if hook.required:
                    raise HookError(f"required_hook_failed:{hook.name}") from exc
                result = HookResult("1.0.0", hook.name, lifecycle_event, "error", (type(exc).__name__,))
            if hook.required and result.status != "passed":
                raise HookError(f"required_hook_rejected:{hook.name}:{','.join(result.findings)}")
            results.append(result)
        return tuple(results)
