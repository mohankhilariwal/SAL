from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from northstar_compliance.common import canonical_dumps

from ..audit import AuditActor, AuditUnavailable, EvidencePackageBuilder, HashChainedAuditLedger
from .correlation import CorrelationContext
from .exporter import BufferedTelemetryPipeline, JsonlExporter
from .tracer import InMemoryTracer, SamplingPolicy


class ObservabilityAuditService:
    MATERIAL_AUDIT_EVENTS = {
        "task.started",
        "authorization.decided",
        "guardrail.decided",
        "tool.write.requested",
        "tool.write.completed",
        "human.approval.requested",
        "human.approval.decided",
        "state.transitioned",
        "exception.applied",
        "task.disposed",
    }

    def __init__(
        self,
        *,
        report_dir: str | Path,
        audit_key: bytes,
        sampling_ratio: float = 0.25,
        audit_fail_writes: bool = False,
    ) -> None:
        report_dir = Path(report_dir)
        report_dir.mkdir(parents=True, exist_ok=True)
        self.tracer = InMemoryTracer(sampling=SamplingPolicy(ratio=sampling_ratio))
        self.pipeline = BufferedTelemetryPipeline(JsonlExporter(report_dir / "telemetry.jsonl"))
        self.ledger = HashChainedAuditLedger(
            report_dir / "audit-ledger.jsonl",
            key=audit_key,
            fail_writes=audit_fail_writes,
            redactor=self.tracer.redactor,
        )
        self.evidence = EvidencePackageBuilder(self.ledger)

    def start_context(
        self,
        *,
        session_id: str,
        run_id: str,
        task_id: str,
        case_id: str,
        tenant_id: str,
    ) -> CorrelationContext:
        return CorrelationContext.new_root(
            session_id=session_id,
            run_id=run_id,
            task_id=task_id,
            case_id=case_id,
            tenant_id=tenant_id,
        )

    def record(
        self,
        *,
        event_name: str,
        context: CorrelationContext,
        component_id: str,
        actor: AuditActor,
        payload: dict[str, Any],
        outcome: str = "ok",
        severity: str = "INFO",
        idempotency_key: str,
        audit_required: bool | None = None,
    ) -> dict[str, Any]:
        event = self.tracer.record_event(
            event_name,
            context,
            component_id=component_id,
            severity=severity,
            outcome=outcome,
            attributes=payload,
            retention_class="RET-SECURITY" if outcome not in {"ok", "success", "allowed"} else "RET-OPERATIONAL",
        )
        if event is not None:
            self.pipeline.submit(event.to_dict())
        mandatory = event_name in self.MATERIAL_AUDIT_EVENTS if audit_required is None else audit_required
        audit_record: dict[str, Any] | None = None
        if mandatory:
            audit_record = self.ledger.append(
                event_type=event_name,
                actor=actor,
                context=context,
                component_id=component_id,
                payload=payload,
                idempotency_key=idempotency_key,
            )
        return {
            "telemetry_recorded": event is not None,
            "audit_recorded": audit_record is not None,
            "audit_event_id": audit_record.get("audit_event_id") if audit_record else None,
            "authority_effect": "none",
        }

    def record_protected_action(
        self,
        *,
        context: CorrelationContext,
        actor: AuditActor,
        component_id: str,
        action: str,
        payload: dict[str, Any],
        outcome_payload: dict[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        digest = hashlib.sha256(canonical_dumps(payload).encode("utf-8")).hexdigest()
        intent = self.record(
            event_name="tool.write.requested",
            context=context,
            component_id=component_id,
            actor=actor,
            payload={"action": action, "request_digest": digest, **payload},
            idempotency_key=f"{context.run_id}:{action}:intent:{digest}",
            audit_required=True,
        )
        outcome_digest = hashlib.sha256(canonical_dumps(outcome_payload).encode("utf-8")).hexdigest()
        outcome = self.record(
            event_name="tool.write.completed",
            context=context,
            component_id=component_id,
            actor=actor,
            payload={"action": action, "request_digest": digest, "outcome_digest": outcome_digest, **outcome_payload},
            idempotency_key=f"{context.run_id}:{action}:outcome:{outcome_digest}",
            audit_required=True,
        )
        return intent, outcome

    def flush_telemetry(self) -> int:
        return self.pipeline.flush()

    def status(self) -> dict[str, Any]:
        verification = self.ledger.verify()
        return {
            "schema_id": "DATA-236",
            "telemetry_spans": len(self.tracer.spans),
            "telemetry_events": len(self.tracer.events),
            "telemetry_buffer_depth": len(self.pipeline.buffer),
            "telemetry_dropped": self.pipeline.dropped,
            "telemetry_export_error": self.pipeline.last_error,
            "audit_events": self.ledger.event_count,
            "audit_valid": verification.valid,
            "audit_last_hash": verification.last_hash,
            "production_ready": False,
            "worm_storage_implemented": False,
            "kms_hsm_signing_implemented": False,
            "full_control_plane_implemented": False,
            "stage8d_resolved": False,
            "stage9d_resolved": False,
            "authority_effect": "none",
        }

    def build_evidence_package(self, run_id: str, **kwargs: Any) -> dict[str, Any]:
        return self.evidence.build(run_id=run_id, **kwargs)


__all__ = ["AuditUnavailable", "ObservabilityAuditService"]
