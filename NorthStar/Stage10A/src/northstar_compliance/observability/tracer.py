from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from typing import Any

from .correlation import CorrelationContext
from .models import MetricPoint, SpanRecord, TelemetryEvent, utc_now
from .redaction import TelemetryRedactor

FORBIDDEN_METRIC_LABELS = {
    "user_id",
    "session_id",
    "run_id",
    "task_id",
    "case_id",
    "trace_id",
    "span_id",
    "prompt",
    "response",
    "tool_arguments",
}


@dataclass(frozen=True, slots=True)
class SamplingPolicy:
    ratio: float = 0.25
    always_sample_events: frozenset[str] = frozenset(
        {
            "authorization.denied",
            "guardrail.denied",
            "guardrail.quarantined",
            "tool.write.requested",
            "tool.write.completed",
            "human.approval.requested",
            "human.approval.decided",
            "exception.applied",
            "incident.raised",
            "task.disposed",
        }
    )

    def should_sample(self, trace_id: str, event_name: str, outcome: str = "ok") -> bool:
        if event_name in self.always_sample_events or outcome not in {"ok", "success", "allowed"}:
            return True
        if self.ratio <= 0:
            return False
        if self.ratio >= 1:
            return True
        bucket = int(hashlib.sha256(trace_id.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
        return bucket < self.ratio


class MetricRegistry:
    def __init__(self) -> None:
        self.points: list[MetricPoint] = []

    def record(self, name: str, value: float, unit: str, attributes: dict[str, str] | None = None) -> MetricPoint:
        attributes = attributes or {}
        forbidden = FORBIDDEN_METRIC_LABELS.intersection(attributes)
        if forbidden:
            raise ValueError(f"high-cardinality or sensitive metric labels forbidden: {sorted(forbidden)}")
        point = MetricPoint(name=name, value=float(value), unit=unit, attributes=dict(attributes))
        self.points.append(point)
        return point


class SpanHandle:
    def __init__(self, tracer: "InMemoryTracer", span: SpanRecord, start_ns: int) -> None:
        self._tracer = tracer
        self.span = span
        self._start_ns = start_ns
        self._ended = False

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        result = self._tracer.redactor.redact(attributes or {})
        self.span.events.append(
            {
                "name": name,
                "timestamp": utc_now(),
                "attributes": result.sanitized,
                "redacted_paths": result.redacted_paths,
            }
        )

    def end(self, *, status: str = "OK", attributes: dict[str, Any] | None = None) -> SpanRecord:
        if self._ended:
            return self.span
        self._ended = True
        if attributes:
            result = self._tracer.redactor.redact(attributes)
            self.span.attributes.update(result.sanitized)
            if result.redacted_paths:
                self.span.attributes["redacted_paths"] = result.redacted_paths
        self.span.end_time = utc_now()
        self.span.duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000
        self.span.status = status
        if self.span.sampled:
            self._tracer.spans.append(self.span)
        return self.span

    def __enter__(self) -> "SpanHandle":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.end(status="ERROR" if exc else "OK", attributes={"error.type": exc_type.__name__} if exc_type else None)
        return False


class InMemoryTracer:
    def __init__(self, *, sampling: SamplingPolicy | None = None, redactor: TelemetryRedactor | None = None) -> None:
        self.sampling = sampling or SamplingPolicy()
        self.redactor = redactor or TelemetryRedactor()
        self.spans: list[SpanRecord] = []
        self.events: list[TelemetryEvent] = []
        self.metrics = MetricRegistry()

    def start_span(
        self,
        name: str,
        context: CorrelationContext,
        *,
        component_id: str,
        event_name: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> SpanHandle:
        child = context.child()
        event = event_name or name
        sampled = self.sampling.should_sample(child.trace_id, event)
        result = self.redactor.redact(attributes or {})
        span = SpanRecord(
            name=name,
            context=child,
            component_id=component_id,
            start_time=utc_now(),
            attributes=result.sanitized,
            sampled=sampled,
        )
        if result.redacted_paths:
            span.attributes["redacted_paths"] = result.redacted_paths
        return SpanHandle(self, span, time.perf_counter_ns())

    def record_event(
        self,
        event_name: str,
        context: CorrelationContext,
        *,
        component_id: str,
        severity: str = "INFO",
        outcome: str = "ok",
        attributes: dict[str, Any] | None = None,
        retention_class: str = "RET-OPERATIONAL",
    ) -> TelemetryEvent | None:
        sampled = self.sampling.should_sample(context.trace_id, event_name, outcome)
        if not sampled:
            return None
        result = self.redactor.redact(attributes or {})
        safe = dict(result.sanitized)
        if result.redacted_paths:
            safe["redacted_paths"] = result.redacted_paths
            safe["redacted_digests"] = result.digests
        event = TelemetryEvent(
            event_name=event_name,
            context=context,
            component_id=component_id,
            severity=severity,
            outcome=outcome,
            attributes=safe,
            retention_class=retention_class,
        )
        self.events.append(event)
        return event
