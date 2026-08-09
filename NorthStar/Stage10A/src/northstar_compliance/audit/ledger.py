from __future__ import annotations

import hashlib
import hmac
import json
import os
import threading
from pathlib import Path
from typing import Any

from northstar_compliance.common import canonical_dumps
from northstar_compliance.observability import CorrelationContext, TelemetryRedactor

from .models import AuditActor, AuditEvent, AuditVerificationReport, utc_now

GENESIS_HASH = "0" * 64


class AuditUnavailable(RuntimeError):
    pass


class AuditIntegrityError(RuntimeError):
    pass


class HashChainedAuditLedger:
    """Append-only local reference ledger.

    HMAC authenticates records in the tutorial. It is not non-repudiation and is
    intentionally not described as WORM or KMS/HSM-backed production storage.
    """

    def __init__(
        self,
        path: str | Path,
        *,
        key: bytes,
        signer_id: str = "local-hmac-stage10a",
        fail_writes: bool = False,
        redactor: TelemetryRedactor | None = None,
    ) -> None:
        if not key:
            raise ValueError("audit key is required")
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.key = key
        self.signer_id = signer_id
        self.fail_writes = fail_writes
        self.redactor = redactor or TelemetryRedactor()
        self._lock = threading.Lock()
        self._events: list[dict[str, Any]] = []
        self._idempotency: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                event = json.loads(line)
                self._events.append(event)
                self._idempotency[event["idempotency_key"]] = event

    @property
    def event_count(self) -> int:
        return len(self._events)

    @property
    def last_hash(self) -> str:
        return self._events[-1]["record_hash"] if self._events else GENESIS_HASH

    def _signature(self, record_hash: str) -> str:
        return hmac.new(self.key, record_hash.encode("ascii"), hashlib.sha256).hexdigest()

    @staticmethod
    def _record_hash(core: dict[str, Any]) -> str:
        return hashlib.sha256(canonical_dumps(core).encode("utf-8")).hexdigest()

    def append(
        self,
        *,
        event_type: str,
        actor: AuditActor,
        context: CorrelationContext,
        component_id: str,
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        if not idempotency_key:
            raise ValueError("idempotency_key is required")
        with self._lock:
            if idempotency_key in self._idempotency:
                return dict(self._idempotency[idempotency_key])
            if self.fail_writes:
                raise AuditUnavailable("mandatory audit append failed")
            redacted = self.redactor.redact(payload)
            safe_payload = dict(redacted.sanitized)
            if redacted.redacted_paths:
                safe_payload["redacted_paths"] = redacted.redacted_paths
                safe_payload["redacted_digests"] = redacted.digests
            sequence = len(self._events) + 1
            now = utc_now()
            payload_hash = hashlib.sha256(canonical_dumps(safe_payload).encode("utf-8")).hexdigest()
            core = {
                "sequence": sequence,
                "event_type": event_type,
                "timestamp": now,
                "observed_timestamp": now,
                "actor": {
                    "actor_type": actor.actor_type,
                    "actor_id": actor.actor_id,
                    "role": actor.role,
                    "workload_id": actor.workload_id,
                },
                "tenant_id": context.tenant_id,
                "case_id": context.case_id,
                "run_id": context.run_id,
                "task_id": context.task_id,
                "component_id": component_id,
                "payload": safe_payload,
                "payload_hash": payload_hash,
                "previous_hash": self.last_hash,
                "signer_id": self.signer_id,
                "trace_id": context.trace_id,
                "span_id": context.span_id,
                "idempotency_key": idempotency_key,
                "authority_effect": "none",
            }
            record_hash = self._record_hash(core)
            event = AuditEvent(
                sequence=sequence,
                event_type=event_type,
                timestamp=now,
                observed_timestamp=now,
                actor=actor,
                tenant_id=context.tenant_id,
                case_id=context.case_id,
                run_id=context.run_id,
                task_id=context.task_id,
                component_id=component_id,
                payload=safe_payload,
                payload_hash=payload_hash,
                previous_hash=self.last_hash,
                record_hash=record_hash,
                signer_id=self.signer_id,
                signature=self._signature(record_hash),
                trace_id=context.trace_id,
                span_id=context.span_id,
                idempotency_key=idempotency_key,
            ).to_dict()
            line = json.dumps(event, sort_keys=True, ensure_ascii=False)
            try:
                with self.path.open("a", encoding="utf-8") as handle:
                    handle.write(line + "\n")
                    handle.flush()
                    os.fsync(handle.fileno())
            except OSError as exc:
                raise AuditUnavailable(f"mandatory audit append failed: {exc}") from exc
            self._events.append(event)
            self._idempotency[idempotency_key] = event
            return dict(event)

    def records(self) -> list[dict[str, Any]]:
        return [dict(event) for event in self._events]

    def verify(self) -> AuditVerificationReport:
        errors: list[str] = []
        previous = GENESIS_HASH
        seen_ids: set[str] = set()
        seen_keys: set[str] = set()
        for expected_sequence, event in enumerate(self._events, start=1):
            if event.get("sequence") != expected_sequence:
                errors.append(f"sequence mismatch at {expected_sequence}")
            if event.get("previous_hash") != previous:
                errors.append(f"previous hash mismatch at {expected_sequence}")
            if event.get("audit_event_id") in seen_ids:
                errors.append(f"duplicate audit_event_id at {expected_sequence}")
            seen_ids.add(event.get("audit_event_id", ""))
            if event.get("idempotency_key") in seen_keys:
                errors.append(f"duplicate idempotency_key at {expected_sequence}")
            seen_keys.add(event.get("idempotency_key", ""))
            actual_payload_hash = hashlib.sha256(
                canonical_dumps(event.get("payload", {})).encode("utf-8")
            ).hexdigest()
            if not hmac.compare_digest(actual_payload_hash, event.get("payload_hash", "")):
                errors.append(f"payload hash mismatch at {expected_sequence}")
            core = {
                key: event[key]
                for key in (
                    "sequence",
                    "event_type",
                    "timestamp",
                    "observed_timestamp",
                    "actor",
                    "tenant_id",
                    "case_id",
                    "run_id",
                    "task_id",
                    "component_id",
                    "payload",
                    "payload_hash",
                    "previous_hash",
                    "signer_id",
                    "trace_id",
                    "span_id",
                    "idempotency_key",
                    "authority_effect",
                )
            }
            actual_record_hash = self._record_hash(core)
            if not hmac.compare_digest(actual_record_hash, event.get("record_hash", "")):
                errors.append(f"record hash mismatch at {expected_sequence}")
            expected_signature = self._signature(actual_record_hash)
            if not hmac.compare_digest(expected_signature, event.get("signature", "")):
                errors.append(f"signature mismatch at {expected_sequence}")
            previous = event.get("record_hash", previous)
        return AuditVerificationReport(
            valid=not errors,
            event_count=len(self._events),
            last_hash=previous,
            errors=errors,
        )

    def create_checkpoint(self) -> dict[str, Any]:
        payload = {
            "event_count": self.event_count,
            "last_hash": self.last_hash,
            "created_at": utc_now(),
            "signer_id": self.signer_id,
            "algorithm": "HMAC-SHA256-local-reference",
            "authority_effect": "none",
        }
        payload["signature"] = hmac.new(
            self.key,
            canonical_dumps(payload).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return payload
