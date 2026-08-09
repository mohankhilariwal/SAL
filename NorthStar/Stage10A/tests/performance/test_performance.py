import time

from northstar_compliance.audit import AuditActor, HashChainedAuditLedger
from northstar_compliance.observability import CorrelationContext, InMemoryTracer, SamplingPolicy


def test_959_ten_thousand_in_memory_events_under_local_guard():
    tracer = InMemoryTracer(sampling=SamplingPolicy(ratio=1.0))
    context = CorrelationContext.new_root(session_id="S", run_id="R", task_id="T", case_id="C", tenant_id="N")
    start = time.perf_counter()
    for i in range(10_000):
        tracer.record_event("runtime.heartbeat", context, component_id="CMP-010", attributes={"index": i})
    elapsed = time.perf_counter() - start
    assert len(tracer.events) == 10_000
    assert elapsed < 5.0


def test_960_one_thousand_audit_appends_and_verify_under_local_guard(tmp_path):
    ledger = HashChainedAuditLedger(tmp_path / "audit.jsonl", key=b"perf-key")
    context = CorrelationContext.new_root(session_id="S", run_id="R", task_id="T", case_id="C", tenant_id="N")
    actor = AuditActor(actor_type="workload", actor_id="runtime")
    start = time.perf_counter()
    for i in range(1_000):
        ledger.append(
            event_type="state.transitioned", actor=actor, context=context, component_id="CMP-003",
            payload={"sequence": i}, idempotency_key=f"id-{i}"
        )
    report = ledger.verify()
    elapsed = time.perf_counter() - start
    assert report.valid and report.event_count == 1_000
    assert elapsed < 10.0
