import pytest

from northstar_compliance.audit import AuditActor, AuditUnavailable
from northstar_compliance.observability.service import ObservabilityAuditService


def make_service(tmp_path, **kwargs):
    return ObservabilityAuditService(report_dir=tmp_path, audit_key=b"integration-key", sampling_ratio=1.0, **kwargs)


def make_context(service):
    return service.start_context(
        session_id="SES-1", run_id="RUN-10A", task_id="TASK-1", case_id="CASE-2026-0001", tenant_id="NORTHSTAR"
    )


def test_947_material_event_goes_to_telemetry_and_audit(tmp_path):
    service = make_service(tmp_path)
    result = service.record(
        event_name="task.started",
        context=make_context(service),
        component_id="CMP-003",
        actor=AuditActor(actor_type="human", actor_id="MAYA", role="analyst"),
        payload={"goal": "assess publication"},
        idempotency_key="start",
    )
    assert result["telemetry_recorded"] and result["audit_recorded"]


def test_948_nonmaterial_event_can_be_telemetry_only(tmp_path):
    service = make_service(tmp_path)
    result = service.record(
        event_name="model.token.usage",
        context=make_context(service),
        component_id="CMP-003",
        actor=AuditActor(actor_type="workload", actor_id="AGT-001"),
        payload={"input_tokens": 100},
        idempotency_key="tokens",
    )
    assert result["telemetry_recorded"] and not result["audit_recorded"]


def test_949_protected_action_records_intent_and_outcome(tmp_path):
    service = make_service(tmp_path)
    intent, outcome = service.record_protected_action(
        context=make_context(service),
        actor=AuditActor(actor_type="workload", actor_id="AGT-001"),
        component_id="CMP-005",
        action="TOOL-006.create_review_request",
        payload={"approval_id": "APR-1"},
        outcome_payload={"status": "queued"},
    )
    assert intent["audit_recorded"] and outcome["audit_recorded"]
    assert service.ledger.event_count == 2


def test_950_audit_outage_blocks_material_event(tmp_path):
    service = make_service(tmp_path, audit_fail_writes=True)
    with pytest.raises(AuditUnavailable):
        service.record(
            event_name="task.started",
            context=make_context(service),
            component_id="CMP-003",
            actor=AuditActor(actor_type="human", actor_id="MAYA"),
            payload={},
            idempotency_key="start",
        )


def test_951_telemetry_flush_writes_jsonl(tmp_path):
    service = make_service(tmp_path)
    service.record(
        event_name="task.started", context=make_context(service), component_id="CMP-003",
        actor=AuditActor(actor_type="human", actor_id="MAYA"), payload={}, idempotency_key="start"
    )
    assert service.flush_telemetry() == 1
    assert (tmp_path / "telemetry.jsonl").exists()


def test_952_status_declares_production_boundaries(tmp_path):
    status = make_service(tmp_path).status()
    assert status["production_ready"] is False
    assert status["worm_storage_implemented"] is False
    assert status["stage9d_resolved"] is False


def test_953_build_evidence_package_after_disposition(tmp_path):
    service = make_service(tmp_path)
    context = make_context(service)
    actor = AuditActor(actor_type="human", actor_id="MAYA", role="analyst")
    service.record(event_name="task.started", context=context, component_id="CMP-003", actor=actor, payload={}, idempotency_key="start")
    service.record(event_name="task.disposed", context=context, component_id="CMP-003", actor=actor, payload={"disposition":"pending_human"}, idempotency_key="end")
    package = service.build_evidence_package("RUN-10A")
    assert package["manifest"]["event_count"] == 2


def test_954_no_new_tool_or_agent_is_introduced(tmp_path):
    status = make_service(tmp_path).status()
    assert status["authority_effect"] == "none"
    assert "TOOL-007" not in str(status)
    assert "AGT-002" not in str(status)
