from __future__ import annotations

import hashlib
import json
import time
import uuid
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import asdict
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

from .adapters import ToolAdapter, TransientToolError
from .models import ToolInvocationRequest, ToolResultEnvelope
from .policy import LocalToolPolicyEngine
from .registry import ToolRegistry
from .storage import LocalJsonStore


class ToolGateway:
    def __init__(
        self,
        registry: ToolRegistry,
        policy: LocalToolPolicyEngine,
        adapters: dict[str, ToolAdapter],
        store: LocalJsonStore,
    ):
        self.registry = registry
        self.policy = policy
        self.adapters = adapters
        self.store = store
        self._idempotency: dict[str, tuple[str, dict[str, Any]]] = {}
        self._rate_history: dict[tuple[str, str], deque[float]] = defaultdict(deque)
        self._circuit_failures: dict[str, int] = defaultdict(int)
        self._circuit_open_until: dict[str, float] = defaultdict(float)


    def _rate_allowed(self, request: ToolInvocationRequest, descriptor) -> bool:
        now = time.monotonic()
        key = (request.principal.principal_id, request.tool_id)
        history = self._rate_history[key]
        while history and now - history[0] >= 60.0:
            history.popleft()
        if len(history) >= int(descriptor.raw["rate_limit_per_minute"]):
            return False
        history.append(now)
        return True

    def _circuit_allowed(self, descriptor) -> bool:
        return time.monotonic() >= self._circuit_open_until[descriptor.tool_id]

    def _record_success(self, descriptor) -> None:
        self._circuit_failures[descriptor.tool_id] = 0
        self._circuit_open_until[descriptor.tool_id] = 0.0

    def _record_failure(self, descriptor) -> None:
        tool_id = descriptor.tool_id
        self._circuit_failures[tool_id] += 1
        if self._circuit_failures[tool_id] >= int(descriptor.raw["circuit_failure_threshold"]):
            self._circuit_open_until[tool_id] = time.monotonic() + int(descriptor.raw["circuit_reset_seconds"])

    @staticmethod
    def _argument_hash(arguments: dict[str, Any]) -> str:
        canonical = json.dumps(arguments, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(canonical).hexdigest()

    def invoke(self, request: ToolInvocationRequest) -> ToolResultEnvelope:
        invocation_id = "TINV-" + uuid.uuid4().hex[:16].upper()
        started = time.monotonic()
        try:
            descriptor = self.registry.resolve(request.tool_id, request.tool_version)
        except KeyError as exc:
            return ToolResultEnvelope("not_found", invocation_id, request.tool_id, request.tool_version, error_code="tool_not_found", error_message=str(exc))
        except LookupError as exc:
            return ToolResultEnvelope("version_mismatch", invocation_id, request.tool_id, request.tool_version, error_code="version_mismatch", error_message=str(exc))

        try:
            Draft202012Validator(descriptor.input_schema).validate(request.arguments)
        except ValidationError as exc:
            return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                "validation_error", invocation_id, request.tool_id, request.tool_version,
                error_code="invalid_arguments", error_message=exc.message,
            ))

        argument_hash = self._argument_hash(request.arguments)
        if descriptor.impact_class == "reversible_write" and request.idempotency_key:
            existing = self._idempotency.get(request.idempotency_key)
            if existing:
                prior_hash, prior_data = existing
                if prior_hash != argument_hash:
                    return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                        "idempotency_conflict", invocation_id, request.tool_id, request.tool_version,
                        error_code="idempotency_conflict", error_message="Key was already bound to different arguments.",
                    ))
                return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                    "replayed", invocation_id, request.tool_id, request.tool_version,
                    data=prior_data, replayed=True,
                ))

        decision = self.policy.decide(request, descriptor)
        if not decision.allowed:
            return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                "denied", invocation_id, request.tool_id, request.tool_version,
                error_code="policy_denied", error_message=decision.reason,
                authorization_decision_id=decision.decision_id,
            ), decision_id=decision.decision_id)

        if not self._rate_allowed(request, descriptor):
            return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                "rate_limited", invocation_id, request.tool_id, request.tool_version,
                error_code="rate_limited", error_message="Process-local rate limit exceeded.",
                authorization_decision_id=decision.decision_id,
            ), decision_id=decision.decision_id)
        if not self._circuit_allowed(descriptor):
            return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                "circuit_open", invocation_id, request.tool_id, request.tool_version,
                error_code="circuit_open", error_message="Process-local circuit breaker is open.",
                authorization_decision_id=decision.decision_id,
            ), decision_id=decision.decision_id)

        adapter = self.adapters.get(request.tool_id)
        if adapter is None:
            return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                "execution_error", invocation_id, request.tool_id, request.tool_version,
                error_code="adapter_missing", error_message="No adapter is registered.",
                authorization_decision_id=decision.decision_id,
            ), decision_id=decision.decision_id)

        max_attempts = int(descriptor.raw["retry_policy"]["max_attempts"])
        if descriptor.impact_class == "reversible_write":
            max_attempts = 1
        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            try:
                executor = ThreadPoolExecutor(max_workers=1)
                future = executor.submit(adapter.execute, request.arguments, request.principal, request.dry_run)
                try:
                    data = future.result(timeout=descriptor.raw["timeout_ms"] / 1000)
                finally:
                    executor.shutdown(wait=False, cancel_futures=True)
                Draft202012Validator(descriptor.output_schema).validate(data)
                encoded = json.dumps(data, sort_keys=True).encode()
                if len(encoded) > int(descriptor.raw["max_result_bytes"]):
                    raise ValueError("result_too_large")
                status = "dry_run" if request.dry_run else "success"
                self._record_success(descriptor)
                if descriptor.impact_class == "reversible_write" and request.idempotency_key and not request.dry_run:
                    self._idempotency[request.idempotency_key] = (argument_hash, data)
                return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                    status, invocation_id, request.tool_id, request.tool_version,
                    data=data, authorization_decision_id=decision.decision_id, attempts=attempts,
                ), decision_id=decision.decision_id)
            except FutureTimeout:
                self._record_failure(descriptor)
                return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                    "timeout", invocation_id, request.tool_id, request.tool_version,
                    error_code="timeout", error_message="Tool exceeded its local wait deadline.",
                    authorization_decision_id=decision.decision_id, attempts=attempts,
                ), decision_id=decision.decision_id)
            except TransientToolError as exc:
                if attempts >= max_attempts:
                    self._record_failure(descriptor)
                    return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                        "execution_error", invocation_id, request.tool_id, request.tool_version,
                        error_code="transient_exhausted", error_message=str(exc),
                        authorization_decision_id=decision.decision_id, attempts=attempts,
                    ), decision_id=decision.decision_id)
            except ValidationError as exc:
                self._record_failure(descriptor)
                return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                    "output_error", invocation_id, request.tool_id, request.tool_version,
                    error_code="invalid_output", error_message=exc.message,
                    authorization_decision_id=decision.decision_id, attempts=attempts,
                ), decision_id=decision.decision_id)
            except Exception as exc:  # normalized boundary for the tutorial runtime
                self._record_failure(descriptor)
                return self._finish(request, descriptor, invocation_id, started, ToolResultEnvelope(
                    "execution_error", invocation_id, request.tool_id, request.tool_version,
                    error_code="execution_error", error_message=str(exc),
                    authorization_decision_id=decision.decision_id, attempts=attempts,
                ), decision_id=decision.decision_id)
        raise AssertionError("unreachable")

    def _finish(self, request, descriptor, invocation_id, started, result, decision_id=None):
        event = {
            "event_type": "tool_execution",
            "invocation_id": invocation_id,
            "tool_id": request.tool_id,
            "tool_version": request.tool_version,
            "descriptor_hash": descriptor.descriptor_hash,
            "principal_id": request.principal.principal_id,
            "correlation_id": request.principal.correlation_id,
            "argument_sha256": self._argument_hash(request.arguments),
            "status": result.status,
            "authorization_decision_id": decision_id or result.authorization_decision_id,
            "attempts": result.attempts,
            "duration_ms": round((time.monotonic() - started) * 1000, 3),
        }
        self.store.append_event(event)
        return result
