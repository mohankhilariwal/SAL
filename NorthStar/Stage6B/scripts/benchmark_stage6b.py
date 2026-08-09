from __future__ import annotations

import json
import statistics
import time
from pathlib import Path

from northstar_compliance.handoff.fixtures import build_signed_fixture


def main() -> int:
    durations = []
    loops = 2000
    f = build_signed_fixture()
    for _ in range(loops):
        start = time.perf_counter_ns()
        f["authority"].verify(f["child"], now=f["now"], audience=f["recipient"].endpoint_id)
        f["envelopes"].verify_envelope(
            f["envelope"], sender=f["sender"], recipient=f["recipient"], grant=f["child"], now=f["now"]
        )
        durations.append((time.perf_counter_ns() - start) / 1_000_000)
    ordered = sorted(durations)
    report = {
        "loops": loops,
        "mean_ms": statistics.mean(durations),
        "p50_ms": ordered[int(0.50 * (loops - 1))],
        "p95_ms": ordered[int(0.95 * (loops - 1))],
        "p99_ms": ordered[int(0.99 * (loops - 1))],
        "environment": "local Python 3.13.5, HMAC/SHA-256, no network/model/database",
        "warning": "This microbenchmark measures only local serialization and validation overhead, not multi-agent latency or production capacity.",
    }
    target = Path("reports/Stage-6B-Benchmark-Report.json")
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
