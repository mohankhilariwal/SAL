from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from governed_release.domain.models import AuditEvent
from governed_release.ports.interfaces import AuditStore
from governed_release.security.redaction import redact_value


class AuditLedger:
    def __init__(self, store: AuditStore, jsonl_path: Path) -> None:
        self.store = store
        self.jsonl_path = jsonl_path
        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)

    def append(
        self, *, workflow_id: str | None, trace_id: str, event_type: str, payload: dict[str, Any]
    ) -> AuditEvent:
        redacted = redact_value(payload)
        previous_hash = self.store.last_hash()
        canonical = json.dumps(
            {
                "workflow_id": workflow_id,
                "trace_id": trace_id,
                "event_type": event_type,
                "payload": redacted,
                "previous_hash": previous_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        event_hash = hashlib.sha256(canonical.encode()).hexdigest()
        event = AuditEvent(
            workflow_id=workflow_id,
            trace_id=trace_id,
            event_type=event_type,
            payload=redacted,
            previous_hash=previous_hash,
            event_hash=event_hash,
        )
        self.store.append(event)
        with self.jsonl_path.open("a", encoding="utf-8") as handle:
            handle.write(event.model_dump_json() + "\n")
        return event

    def verify(self) -> tuple[bool, list[str]]:
        errors: list[str] = []
        previous = "0" * 64
        records = self.store.all_records()
        for record in records:
            payload = json.loads(record.payload_json)
            canonical = json.dumps(
                {
                    "workflow_id": record.workflow_id,
                    "trace_id": record.trace_id,
                    "event_type": record.event_type,
                    "payload": payload,
                    "previous_hash": previous,
                },
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            )
            expected = hashlib.sha256(canonical.encode()).hexdigest()
            if record.previous_hash != previous:
                errors.append(f"event {record.event_id}: previous hash mismatch")
            if record.event_hash != expected:
                errors.append(f"event {record.event_id}: event hash mismatch")
            previous = record.event_hash
        return not errors, errors
