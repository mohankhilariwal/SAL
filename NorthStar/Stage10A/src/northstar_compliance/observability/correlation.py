from __future__ import annotations

import re
import secrets
from dataclasses import dataclass, replace

TRACEPARENT_RE = re.compile(
    r"^(?P<version>[0-9a-f]{2})-(?P<trace_id>[0-9a-f]{32})-(?P<span_id>[0-9a-f]{16})-(?P<flags>[0-9a-f]{2})$"
)


class InvalidTraceContext(ValueError):
    pass


def _hex_id(nbytes: int) -> str:
    value = secrets.token_hex(nbytes)
    if int(value, 16) == 0:
        return _hex_id(nbytes)
    return value


@dataclass(frozen=True, slots=True)
class CorrelationContext:
    trace_id: str
    span_id: str
    parent_span_id: str | None
    trace_flags: str
    session_id: str
    run_id: str
    task_id: str
    case_id: str
    tenant_id: str
    agent_id: str = "AGT-001"
    agent_spec_version: str = "1.1.0"
    authority_effect: str = "none"

    @classmethod
    def new_root(
        cls,
        *,
        session_id: str,
        run_id: str,
        task_id: str,
        case_id: str,
        tenant_id: str,
        sampled: bool = True,
    ) -> "CorrelationContext":
        return cls(
            trace_id=_hex_id(16),
            span_id=_hex_id(8),
            parent_span_id=None,
            trace_flags="01" if sampled else "00",
            session_id=session_id,
            run_id=run_id,
            task_id=task_id,
            case_id=case_id,
            tenant_id=tenant_id,
        )

    @classmethod
    def from_traceparent(
        cls,
        traceparent: str,
        *,
        session_id: str,
        run_id: str,
        task_id: str,
        case_id: str,
        tenant_id: str,
    ) -> "CorrelationContext":
        match = TRACEPARENT_RE.match(traceparent.strip().lower())
        if not match:
            raise InvalidTraceContext("traceparent does not match W3C format")
        if match.group("version") == "ff":
            raise InvalidTraceContext("traceparent version ff is invalid")
        trace_id = match.group("trace_id")
        parent_span = match.group("span_id")
        if int(trace_id, 16) == 0 or int(parent_span, 16) == 0:
            raise InvalidTraceContext("all-zero trace or span identifiers are invalid")
        return cls(
            trace_id=trace_id,
            span_id=_hex_id(8),
            parent_span_id=parent_span,
            trace_flags=match.group("flags"),
            session_id=session_id,
            run_id=run_id,
            task_id=task_id,
            case_id=case_id,
            tenant_id=tenant_id,
        )

    def child(self) -> "CorrelationContext":
        return replace(self, parent_span_id=self.span_id, span_id=_hex_id(8))

    @property
    def traceparent(self) -> str:
        return f"00-{self.trace_id}-{self.span_id}-{self.trace_flags}"

    def safe_attributes(self) -> dict[str, str]:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "session_id": self.session_id,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "case_id": self.case_id,
            "tenant_id": self.tenant_id,
            "agent_id": self.agent_id,
            "agent_spec_version": self.agent_spec_version,
            "authority_effect": self.authority_effect,
        }
