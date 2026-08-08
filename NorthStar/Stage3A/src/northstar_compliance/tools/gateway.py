from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import replace
from typing import Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from .adapters import ToolAdapter
from .controls import CircuitBreaker, CircuitOpen, RateLimitExceeded, SlidingWindowRateLimiter
from .errors import PermanentToolError, TransientToolError
from .events import JsonlToolEventWriter
from .idempotency import IdempotencyRecord, InMemoryIdempotencyStore
from .models import (
    ImpactClass,
    ToolDescriptor,
    ToolError,
    ToolExecutionEvent,
    ToolInvocationRequest,
    ToolResultEnvelope,
    ToolStatus,
)
from .policy import LocalToolPolicyEngine
from .registry import ToolRegistry, ToolRegistryError
from .utils import canonical_json, redact, sha256_json, stable_id, utc_now_iso


class ToolGateway:
    def __init__(
        self,
        registry: ToolRegistry,
        adapters: Mapping[str, ToolAdapter],
        *,
        policy_engine: LocalToolPolicyEngine | None = None,
        idempotency_store: InMemoryIdempotencyStore | None = None,
        rate_limiter: SlidingWindowRateLimiter | None = None,
        circuit_breaker: CircuitBreaker | None = None,
        event_writer: JsonlToolEventWriter | None = None,
    ) -> None:
        self.registry = registry
        self.adapters = dict(adapters)
        self.policy_engine = policy_engine or LocalToolPolicyEngine()
        self.idempotency_store = idempotency_store or InMemoryIdempotencyStore()
        self.rate_limiter = rate_limiter or SlidingWindowRateLimiter()
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.event_writer = event_writer or JsonlToolEventWriter()

    def invoke(self, request: ToolInvocationRequest) -> ToolResultEnvelope:
        started_wall = utc_now_iso()
        started = time.perf_counter()
        descriptor: ToolDescriptor | None = None
        decision_id: str | None = None
        attempts = 0

        try:
            descriptor = self.registry.resolve(request.tool_id, request.tool_version)
        except ToolRegistryError as exc:
            status = ToolStatus.VERSION_MISMATCH if "version mismatch" in str(exc) else ToolStatus.NOT_FOUND
            return self._finish(
                request,
                None,
                status,
                started_wall,
                started,
                None,
                attempts,
                error=ToolError(code=status.value, message=str(exc)),
            )

        try:
            Draft202012Validator.check_schema(dict(descriptor.input_schema))
            Draft202012Validator(descriptor.input_schema).validate(dict(request.arguments))
            arguments_hash = sha256_json(request.arguments)
        except (ValidationError, TypeError, ValueError) as exc:
            return self._finish(
                request,
                descriptor,
                ToolStatus.VALIDATION_ERROR,
                started_wall,
                started,
                None,
                attempts,
                error=ToolError(code="invalid_arguments", message=self._safe_message(exc)),
            )

        if descriptor.idempotency_required and not request.idempotency_key:
            return self._finish(
                request,
                descriptor,
                ToolStatus.VALIDATION_ERROR,
                started_wall,
                started,
                None,
                attempts,
                error=ToolError(code="idempotency_key_required", message="write tool requires idempotency_key"),
            )

        if descriptor.idempotency_required and request.idempotency_key:
            existing = self.idempotency_store.get(
                request.principal.principal_id,
                descriptor.tool_id,
                descriptor.version,
                request.idempotency_key,
            )
            if existing is not None:
                if existing.arguments_sha256 != arguments_hash:
                    return self._finish(
                        request,
                        descriptor,
                        ToolStatus.IDEMPOTENCY_CONFLICT,
                        started_wall,
                        started,
                        existing.result.authorization_decision_id,
                        0,
                        error=ToolError(
                            code="idempotency_conflict",
                            message="idempotency key was previously used with different arguments",
                        ),
                    )
                replay = replace(
                    existing.result,
                    invocation_id=request.invocation_id,
                    status=ToolStatus.REPLAYED,
                    started_at=started_wall,
                    finished_at=utc_now_iso(),
                    duration_ms=(time.perf_counter() - started) * 1000,
                    replayed=True,
                )
                self._write_event(request, descriptor, replay, arguments_hash)
                return replay

        decision = self.policy_engine.decide(request, descriptor)
        decision_id = decision.decision_id
        if not decision.allowed:
            status = (
                ToolStatus.APPROVAL_REQUIRED
                if "approval_required" in decision.reason_codes
                else ToolStatus.DENIED
            )
            return self._finish(
                request,
                descriptor,
                status,
                started_wall,
                started,
                decision_id,
                attempts,
                error=ToolError(
                    code=status.value,
                    message="tool invocation denied",
                    details={"reason_codes": list(decision.reason_codes)},
                ),
                arguments_hash=arguments_hash,
            )

        try:
            self.rate_limiter.check(request.principal.principal_id, descriptor.tool_id)
        except RateLimitExceeded as exc:
            return self._finish(
                request,
                descriptor,
                ToolStatus.RATE_LIMITED,
                started_wall,
                started,
                decision_id,
                attempts,
                error=ToolError(code="rate_limited", message=str(exc), retryable=True),
                arguments_hash=arguments_hash,
            )

        try:
            self.circuit_breaker.before_call(descriptor.tool_id)
        except CircuitOpen as exc:
            return self._finish(
                request,
                descriptor,
                ToolStatus.CIRCUIT_OPEN,
                started_wall,
                started,
                decision_id,
                attempts,
                error=ToolError(code="circuit_open", message=str(exc), retryable=True),
                arguments_hash=arguments_hash,
            )

        if request.dry_run and descriptor.impact_class == ImpactClass.REVERSIBLE_WRITE:
            result = self._finish(
                request,
                descriptor,
                ToolStatus.DRY_RUN,
                started_wall,
                started,
                decision_id,
                attempts,
                data={
                    "would_execute": descriptor.tool_id,
                    "impact_class": descriptor.impact_class.value,
                    "arguments_sha256": arguments_hash,
                    "side_effect_performed": False,
                },
                arguments_hash=arguments_hash,
            )
            return result

        adapter = self.adapters.get(descriptor.tool_id)
        if adapter is None:
            return self._finish(
                request,
                descriptor,
                ToolStatus.NOT_FOUND,
                started_wall,
                started,
                decision_id,
                attempts,
                error=ToolError(code="adapter_not_found", message="tool adapter is not installed"),
                arguments_hash=arguments_hash,
            )

        max_attempts = descriptor.retry_policy.max_attempts
        if descriptor.impact_class != ImpactClass.READ_ONLY:
            max_attempts = 1

        last_error: Exception | None = None
        for attempts in range(1, max_attempts + 1):
            try:
                data = self._execute_with_timeout(adapter, request, descriptor.timeout_ms)
                Draft202012Validator.check_schema(dict(descriptor.output_schema))
                Draft202012Validator(descriptor.output_schema).validate(dict(data))
                encoded = canonical_json(data).encode("utf-8")
                if len(encoded) > descriptor.max_result_bytes:
                    self.circuit_breaker.record_failure(descriptor.tool_id)
                    return self._finish(
                        request,
                        descriptor,
                        ToolStatus.RESULT_TOO_LARGE,
                        started_wall,
                        started,
                        decision_id,
                        attempts,
                        error=ToolError(
                            code="result_too_large",
                            message=f"result exceeds {descriptor.max_result_bytes} bytes",
                        ),
                        arguments_hash=arguments_hash,
                    )
                self.circuit_breaker.record_success(descriptor.tool_id)
                result = self._finish(
                    request,
                    descriptor,
                    ToolStatus.SUCCESS,
                    started_wall,
                    started,
                    decision_id,
                    attempts,
                    data=dict(data),
                    arguments_hash=arguments_hash,
                )
                if descriptor.idempotency_required and request.idempotency_key:
                    self.idempotency_store.put(
                        request.principal.principal_id,
                        descriptor.tool_id,
                        descriptor.version,
                        request.idempotency_key,
                        IdempotencyRecord(arguments_hash, result),
                    )
                return result
            except FutureTimeoutError as exc:
                last_error = exc
                break
            except ValidationError as exc:
                self.circuit_breaker.record_failure(descriptor.tool_id)
                return self._finish(
                    request,
                    descriptor,
                    ToolStatus.OUTPUT_VALIDATION_ERROR,
                    started_wall,
                    started,
                    decision_id,
                    attempts,
                    error=ToolError(code="invalid_tool_output", message=self._safe_message(exc)),
                    arguments_hash=arguments_hash,
                )
            except TransientToolError as exc:
                last_error = exc
                if (
                    "TransientToolError" in descriptor.retry_policy.retryable_errors
                    and attempts < max_attempts
                ):
                    continue
                break
            except (PermanentToolError, ValueError, TypeError, OSError) as exc:
                last_error = exc
                break
            except Exception as exc:  # defensive boundary; message is sanitized below
                last_error = exc
                break

        self.circuit_breaker.record_failure(descriptor.tool_id)
        if isinstance(last_error, FutureTimeoutError):
            status = ToolStatus.TIMEOUT
            error = ToolError(code="timeout", message="tool execution exceeded timeout", retryable=True)
        else:
            status = ToolStatus.EXECUTION_ERROR
            retryable = isinstance(last_error, TransientToolError)
            error = ToolError(
                code="tool_execution_error",
                message=self._safe_message(last_error or RuntimeError("unknown tool failure")),
                retryable=retryable,
            )
        return self._finish(
            request,
            descriptor,
            status,
            started_wall,
            started,
            decision_id,
            attempts,
            error=error,
            arguments_hash=arguments_hash,
        )

    @staticmethod
    def _execute_with_timeout(
        adapter: ToolAdapter, request: ToolInvocationRequest, timeout_ms: int
    ) -> Mapping[str, object]:
        executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="northstar-tool")
        future = executor.submit(adapter.execute, request.arguments, request.principal)
        try:
            return future.result(timeout=timeout_ms / 1000)
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    def _finish(
        self,
        request: ToolInvocationRequest,
        descriptor: ToolDescriptor | None,
        status: ToolStatus,
        started_wall: str,
        started: float,
        decision_id: str | None,
        attempts: int,
        *,
        data: Mapping[str, object] | None = None,
        error: ToolError | None = None,
        arguments_hash: str | None = None,
    ) -> ToolResultEnvelope:
        result = ToolResultEnvelope(
            schema_version="1.0.0",
            invocation_id=request.invocation_id,
            tool_id=request.tool_id,
            tool_version=request.tool_version,
            status=status,
            started_at=started_wall,
            finished_at=utc_now_iso(),
            duration_ms=(time.perf_counter() - started) * 1000,
            authorization_decision_id=decision_id,
            attempts=attempts,
            data=dict(data) if data is not None else None,
            error=error,
            replayed=False,
            descriptor_hash=descriptor.descriptor_hash if descriptor else None,
        )
        if descriptor is not None:
            self._write_event(
                request,
                descriptor,
                result,
                arguments_hash or self._hash_best_effort(request.arguments),
            )
        return result

    def _write_event(
        self,
        request: ToolInvocationRequest,
        descriptor: ToolDescriptor,
        result: ToolResultEnvelope,
        arguments_hash: str,
    ) -> None:
        event = ToolExecutionEvent(
            schema_version="1.0.0",
            event_id=stable_id(
                "TEVT",
                {
                    "invocation_id": result.invocation_id,
                    "tool_id": descriptor.tool_id,
                    "status": result.status.value,
                    "finished_at": result.finished_at,
                },
            ),
            invocation_id=result.invocation_id,
            tool_id=descriptor.tool_id,
            tool_version=descriptor.version,
            principal_id=request.principal.principal_id,
            correlation_id=request.principal.correlation_id,
            status=result.status.value,
            arguments_sha256=arguments_hash,
            redacted_arguments=redact(request.arguments, descriptor.sensitive_input_fields),
            authorization_decision_id=result.authorization_decision_id,
            attempts=result.attempts,
            duration_ms=result.duration_ms,
            timestamp=result.finished_at,
            descriptor_hash=descriptor.descriptor_hash,
        )
        self.event_writer.write(event)

    @staticmethod
    def _safe_message(exc: Exception) -> str:
        message = str(exc).replace("\n", " ").strip()
        return (message or exc.__class__.__name__)[:300]

    @staticmethod
    def _hash_best_effort(arguments: Mapping[str, object]) -> str:
        try:
            return sha256_json(arguments)
        except Exception:
            return sha256_json({"unserializable": True, "keys": sorted(arguments.keys())})
