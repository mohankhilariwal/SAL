import json

from northstar_compliance.audit import AuditActor
from northstar_compliance.observability import BufferedTelemetryPipeline, CorrelationContext, JsonlExporter
from northstar_compliance.observability.service import ObservabilityAuditService


def context(service):
    return service.start_context(session_id="S", run_id="R", task_id="T", case_id="C", tenant_id="N")


def test_955_raw_prompt_and_token_do_not_leak(tmp_path):
    service = ObservabilityAuditService(report_dir=tmp_path, audit_key=b"security", sampling_ratio=1.0)
    service.record(
        event_name="task.started", context=context(service), component_id="CMP-003",
        actor=AuditActor(actor_type="human", actor_id="MAYA"),
        payload={"raw_prompt":"private prompt", "access_token":"Bearer secret.token"}, idempotency_key="one"
    )
    service.flush_telemetry()
    combined = (tmp_path / "telemetry.jsonl").read_text() + (tmp_path / "audit-ledger.jsonl").read_text()
    assert "private prompt" not in combined
    assert "secret.token" not in combined


def test_956_exporter_failure_does_not_delete_buffer(tmp_path):
    exporter = JsonlExporter(tmp_path / "out.jsonl", fail=True)
    pipeline = BufferedTelemetryPipeline(exporter, max_buffer=2)
    pipeline.submit({"event": 1})
    assert pipeline.flush() == 0
    assert len(pipeline.buffer) == 1


def test_957_buffer_overflow_is_counted(tmp_path):
    pipeline = BufferedTelemetryPipeline(JsonlExporter(tmp_path / "out.jsonl"), max_buffer=2)
    pipeline.submit({"event": 1})
    pipeline.submit({"event": 2})
    pipeline.submit({"event": 3})
    assert pipeline.dropped == 1
    assert len(pipeline.buffer) == 2


def test_958_audit_records_do_not_contain_hidden_reasoning(tmp_path):
    service = ObservabilityAuditService(report_dir=tmp_path, audit_key=b"security", sampling_ratio=1.0)
    service.record(
        event_name="task.started", context=context(service), component_id="CMP-003",
        actor=AuditActor(actor_type="human", actor_id="MAYA"),
        payload={"chain_of_thought":"never store this", "decision_summary":"bounded evidence"}, idempotency_key="two"
    )
    record = json.loads((tmp_path / "audit-ledger.jsonl").read_text())
    assert record["payload"]["chain_of_thought"] == "[REDACTED]"
    assert "never store this" not in json.dumps(record)
