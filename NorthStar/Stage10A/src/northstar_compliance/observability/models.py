from __future__ import annotations

import datetime as dt
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from .correlation import CorrelationContext


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


@dataclass(slots=True)
class TelemetryEvent:
    event_name: str
    context: CorrelationContext
    component_id: str
    severity: str = "INFO"
    outcome: str = "ok"
    attributes: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now)
    observed_timestamp: str = field(default_factory=utc_now)
    event_id: str = field(default_factory=lambda: f"TEL-{uuid.uuid4().hex.upper()}")
    retention_class: str = "RET-OPERATIONAL"
    authority_effect: str = "none"

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value.pop("context")
        value.update(self.context.safe_attributes())
        value["parent_span_id"] = self.context.parent_span_id
        value["trace_flags"] = self.context.trace_flags
        return value


@dataclass(slots=True)
class SpanRecord:
    name: str
    context: CorrelationContext
    component_id: str
    start_time: str
    end_time: str | None = None
    duration_ms: float | None = None
    status: str = "UNSET"
    attributes: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    sampled: bool = True
    authority_effect: str = "none"

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value.pop("context")
        value.update(self.context.safe_attributes())
        value["parent_span_id"] = self.context.parent_span_id
        value["trace_flags"] = self.context.trace_flags
        return value


@dataclass(slots=True)
class MetricPoint:
    name: str
    value: float
    unit: str
    attributes: dict[str, str]
    timestamp: str = field(default_factory=utc_now)
    authority_effect: str = "none"
