from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

from northstar_compliance.audit import AuditActor, HashChainedAuditLedger
from northstar_compliance.observability import CorrelationContext, InMemoryTracer, SamplingPolicy

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def main() -> None:
    work = REPORTS / "stage10a-performance-work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    context = CorrelationContext.new_root(session_id="S", run_id="R", task_id="T", case_id="C", tenant_id="N")
    tracer = InMemoryTracer(sampling=SamplingPolicy(ratio=1.0))

    start = time.perf_counter()
    for i in range(10_000):
        tracer.record_event("runtime.heartbeat", context, component_id="CMP-010", attributes={"index": i})
    telemetry_seconds = time.perf_counter() - start

    ledger = HashChainedAuditLedger(work / "audit.jsonl", key=b"stage10a-performance")
    actor = AuditActor(actor_type="workload", actor_id="runtime")
    start = time.perf_counter()
    for i in range(1_000):
        ledger.append(
            event_type="state.transitioned",
            actor=actor,
            context=context,
            component_id="CMP-003",
            payload={"sequence": i},
            idempotency_key=f"perf-{i}",
        )
    append_seconds = time.perf_counter() - start
    start = time.perf_counter()
    verification = ledger.verify()
    verify_seconds = time.perf_counter() - start

    result = {
        "telemetry_events": 10_000,
        "telemetry_seconds": telemetry_seconds,
        "telemetry_events_per_second": 10_000 / telemetry_seconds,
        "audit_events": 1_000,
        "audit_append_seconds": append_seconds,
        "audit_appends_per_second": 1_000 / append_seconds,
        "audit_verify_seconds": verify_seconds,
        "audit_valid": verification.valid,
        "local_guard_passed": telemetry_seconds < 5 and append_seconds + verify_seconds < 10,
        "production_benchmark": False,
        "authority_effect": "none",
    }
    (REPORTS / "stage10a-performance.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
