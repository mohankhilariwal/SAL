from __future__ import annotations

from datetime import timedelta
import json
from pathlib import Path
import statistics
import tempfile
import time

from northstar_compliance.memory import (
    CaseWorkingMemoryService,
    ContextCompactor,
    ContextRegenerator,
    LocalCaseMemoryStore,
    MemoryConsentGrant,
    MemoryPolicy,
    MemoryQuery,
    Scope,
)
from northstar_compliance.memory.models import isoformat_z, utc_now
from run_stage5b_demo import sample_state


def timed(fn, iterations: int = 200):
    samples = []
    result = None
    for _ in range(iterations):
        start = time.perf_counter_ns()
        result = fn()
        samples.append((time.perf_counter_ns() - start) / 1_000_000)
    return result, samples


def percentile(samples, p):
    ordered = sorted(samples)
    index = min(len(ordered) - 1, max(0, round((p / 100) * (len(ordered) - 1))))
    return ordered[index]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    policy = MemoryPolicy.from_file(root / "config/memory/policy.json")
    scope = Scope("TENANT-NORTHSTAR", "CASE-BENCH", "maya.chen")
    state = sample_state(scope)
    regenerator = ContextRegenerator(policy)
    compactor = ContextCompactor(policy)
    regenerated, regen_samples = timed(lambda: regenerator.regenerate(scope=scope, case_state=state, state_version="1.1.0"))
    snapshot, compact_samples = timed(lambda: compactor.compact(regenerated))
    now = utc_now()
    grant = MemoryConsentGrant(
        grant_id="MCG-BENCH",
        schema_version="1.0.0",
        scope=scope,
        purpose="case_session_continuity",
        allowed_operations=("write", "read", "delete"),
        issued_at=isoformat_z(now),
        expires_at=isoformat_z(now + timedelta(days=7)),
    )
    with tempfile.TemporaryDirectory(prefix="northstar-stage5b-bench-") as tmp:
        service = CaseWorkingMemoryService(policy, LocalCaseMemoryStore(Path(tmp) / "memory"))
        _, write_samples = timed(lambda: service.write_snapshot(snapshot=snapshot, grant=grant, write_request_id="WR-BENCH"), iterations=100)
        _, read_samples = timed(
            lambda: service.read(
                query=MemoryQuery(query_id="Q-BENCH", schema_version="1.0.0", scope=scope),
                grant=grant,
                current_source_versions={},
            ),
            iterations=100,
        )
    state_chars = len(json.dumps(state, sort_keys=True, ensure_ascii=False))
    report = {
        "stage": "S05B",
        "environment": {"python": "3.13.5", "runtime_dependencies": "standard_library_only"},
        "workload": {"synthetic_case_state_chars": state_chars, "iterations": 200},
        "context": {
            "snapshot_chars": snapshot.char_count,
            "snapshot_items": snapshot.item_count,
            "raw_to_snapshot_ratio": round(snapshot.char_count / state_chars, 4),
        },
        "latency_ms": {
            "regeneration_p50": percentile(regen_samples, 50),
            "regeneration_p95": percentile(regen_samples, 95),
            "compaction_p50": percentile(compact_samples, 50),
            "compaction_p95": percentile(compact_samples, 95),
            "idempotent_write_p50": percentile(write_samples, 50),
            "idempotent_write_p95": percentile(write_samples, 95),
            "read_p50": percentile(read_samples, 50),
            "read_p95": percentile(read_samples, 95),
        },
        "warning": "Local microbenchmark only; not a production SLO, cost, concurrency or database benchmark."
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
