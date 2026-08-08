from __future__ import annotations

import json
import shutil
import statistics
from pathlib import Path

from northstar_compliance.tools.factory import build_local_gateway
from northstar_compliance.tools.controls import SlidingWindowRateLimiter
from northstar_compliance.tools.models import ToolInvocationRequest, ToolPrincipalContext


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "stage3a-gateway-benchmark.json"


def percentile(values, p):
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * p)))
    return ordered[index]


def main() -> None:
    store = ROOT / "examples" / "stage3a-output" / "benchmark-store"
    if store.exists():
        shutil.rmtree(store)
    gateway, _ = build_local_gateway(ROOT / "config" / "tools", store)
    gateway.rate_limiter = SlidingWindowRateLimiter(limit=1000, window_seconds=60)
    principal = ToolPrincipalContext(
        principal_id="maya.chen",
        groups=("regulatory_analysts",),
        clearance="confidential",
        purpose="regulatory_change_assessment",
        residency="CA",
        correlation_id="CORR-STAGE3A-BENCH",
    )
    durations = []
    for i in range(100):
        result = gateway.invoke(
            ToolInvocationRequest(
                invocation_id=f"TINV-BENCH-{i:03d}",
                tool_id="TOOL-002",
                tool_version="1.0.0",
                principal=principal,
                arguments={"control_id": None, "domain": "lending"},
            )
        )
        if result.status.value != "success":
            raise SystemExit(f"benchmark failed: {result.to_dict()}")
        durations.append(result.duration_ms)
    report = {
        "schema_version": "1.0.0",
        "sample_count": len(durations),
        "p50_ms": statistics.median(durations),
        "p95_ms": percentile(durations, 0.95),
        "p99_ms": percentile(durations, 0.99),
        "mean_ms": statistics.mean(durations),
        "boundary": "single-process local synthetic adapter; not a production SLO",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
