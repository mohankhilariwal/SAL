from __future__ import annotations

import copy
import re
from datetime import datetime
from typing import Any

from northstar_compliance.common.jsonutil import isoformat_utc, new_id
from northstar_compliance.harness.models import TraceEvent
from northstar_compliance.harness.workspace import SessionWorkspace


_SENSITIVE = re.compile(r"token|secret|password|authorization|cookie|prompt_content|raw_content|chain_of_thought|hidden_reasoning", re.I)


def _sanitize(value: Any, *, key: str = "") -> Any:
    if _SENSITIVE.search(key):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(k): _sanitize(v, key=str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_sanitize(v, key=key) for v in value]
    if isinstance(value, str) and len(value) > 256:
        return value[:256] + "...[truncated]"
    return copy.deepcopy(value)


class JsonlTracer:
    """Local privacy-preserving trace evidence. It is not an audit ledger."""

    def __init__(self, workspace: SessionWorkspace, *, session_id: str, trace_id: str | None = None):
        self.workspace = workspace
        self.session_id = session_id
        self.trace_id = trace_id or new_id("TRACE")

    def emit(
        self,
        *,
        event_type: str,
        now: datetime,
        run_id: str | None = None,
        parent_span_id: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> TraceEvent:
        event = TraceEvent(
            schema_version="1.0.0",
            trace_id=self.trace_id,
            span_id=new_id("SPAN"),
            parent_span_id=parent_span_id,
            session_id=self.session_id,
            run_id=run_id,
            event_type=event_type,
            timestamp=isoformat_utc(now),
            attributes=_sanitize(attributes or {}),
        )
        self.workspace.append_jsonl("trace.jsonl", event.to_dict())
        return event
