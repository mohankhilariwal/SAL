from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

from .canonical import sha256_digest
from .models import HandoffEnvelope, HandoffStatus, StatusEvent, TERMINAL_STATUSES


class LifecycleError(ValueError):
    pass


_ALLOWED_TRANSITIONS: dict[HandoffStatus, set[HandoffStatus]] = {
    HandoffStatus.OFFERED: {HandoffStatus.ACCEPTED, HandoffStatus.REJECTED, HandoffStatus.EXPIRED, HandoffStatus.CANCEL_REQUESTED},
    HandoffStatus.ACCEPTED: {HandoffStatus.RUNNING, HandoffStatus.CANCEL_REQUESTED, HandoffStatus.EXPIRED},
    HandoffStatus.RUNNING: {HandoffStatus.COMPLETED, HandoffStatus.FAILED, HandoffStatus.CANCEL_REQUESTED, HandoffStatus.EXPIRED},
    HandoffStatus.CANCEL_REQUESTED: {HandoffStatus.CANCELLED, HandoffStatus.FAILED, HandoffStatus.EXPIRED},
}


class HandoffCoordinator:
    """Orchestrator-owned sequential state machine; recipients cannot route the graph."""

    def __init__(self) -> None:
        self._events: dict[str, list[StatusEvent]] = {}
        self._envelopes: dict[str, HandoffEnvelope] = {}

    def register(self, envelope: HandoffEnvelope) -> StatusEvent:
        if envelope.envelope_id in self._envelopes:
            raise LifecycleError("duplicate_envelope")
        self._envelopes[envelope.envelope_id] = envelope
        return self._record(envelope, None, envelope.status, envelope.sender_id, "registered")

    def transition(
        self,
        envelope_id: str,
        new_status: HandoffStatus,
        *,
        actor_id: str,
        reason_code: str,
        now: datetime | None = None,
        details: dict | None = None,
    ) -> StatusEvent:
        now = now or datetime.now(timezone.utc)
        envelope = self._require(envelope_id)
        current = envelope.status
        if current in TERMINAL_STATUSES:
            raise LifecycleError("terminal_transition_prohibited")
        if new_status not in _ALLOWED_TRANSITIONS.get(current, set()):
            raise LifecycleError("invalid_status_transition")
        if now >= envelope.deadline_at and new_status not in {HandoffStatus.EXPIRED, HandoffStatus.CANCELLED}:
            raise LifecycleError("deadline_passed")
        updated = replace(envelope, status=new_status)
        self._envelopes[envelope_id] = updated
        return self._record(updated, current, new_status, actor_id, reason_code, now=now, details=details)

    def current(self, envelope_id: str) -> HandoffEnvelope:
        return self._require(envelope_id)

    def events(self, envelope_id: str) -> tuple[StatusEvent, ...]:
        return tuple(self._events.get(envelope_id, ()))

    def system_termination_ready(self, envelope_ids: tuple[str, ...]) -> bool:
        if not envelope_ids:
            return False
        return all(self._require(eid).status in TERMINAL_STATUSES for eid in envelope_ids)

    def _record(
        self,
        envelope: HandoffEnvelope,
        previous: HandoffStatus | None,
        status: HandoffStatus,
        actor_id: str,
        reason_code: str,
        *,
        now: datetime | None = None,
        details: dict | None = None,
    ) -> StatusEvent:
        now = now or datetime.now(timezone.utc)
        event = StatusEvent(
            event_id=f"EVT-{uuid4().hex[:16].upper()}",
            envelope_id=envelope.envelope_id,
            task_id=envelope.task_id,
            actor_id=actor_id,
            previous_status=previous,
            status=status,
            occurred_at=now,
            reason_code=reason_code,
            details=details or {},
        )
        event = replace(event, digest_sha256=sha256_digest(event))
        self._events.setdefault(envelope.envelope_id, []).append(event)
        return event

    def _require(self, envelope_id: str) -> HandoffEnvelope:
        try:
            return self._envelopes[envelope_id]
        except KeyError as exc:
            raise LifecycleError("unknown_envelope") from exc
