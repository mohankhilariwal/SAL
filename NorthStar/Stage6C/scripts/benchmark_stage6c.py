from __future__ import annotations

import json
import statistics
import time
from pathlib import Path

from northstar_compliance.interoperability.adapters.a2a import A2AMappingAdapter
from northstar_compliance.interoperability.adapters.direct import DirectAdapter
from northstar_compliance.interoperability.adapters.mcp import McpMappingAdapter
from northstar_compliance.interoperability.fixtures import build_fixture


def measure(fn, iterations: int = 1000) -> dict[str, float]:
    samples = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        fn()
        samples.append((time.perf_counter_ns() - start) / 1_000_000)
    ordered = sorted(samples)
    return {
        "iterations": iterations,
        "mean_ms": statistics.fmean(samples),
        "p50_ms": ordered[int(iterations * 0.50)],
        "p95_ms": ordered[int(iterations * 0.95)],
        "max_ms": max(samples),
    }


def main() -> None:
    fixture = build_fixture()
    a2a = A2AMappingAdapter()
    mcp = McpMappingAdapter()
    report = {
        "environment": "local deterministic microbenchmark; excludes network, TLS, IAM, model and storage latency",
        "direct_contract_validation": measure(lambda: DirectAdapter().deliver(fixture), 500),
        "a2a_mapping": measure(lambda: a2a.map_task_message(fixture["envelope"]), 2000),
        "mcp_catalog_mapping": measure(
            lambda: mcp.build_server_document(
                tool_ids=("TOOL-001", "TOOL-002", "TOOL-003", "TOOL-004", "TOOL-005", "TOOL-006"),
                artifacts=(fixture["manifest"],),
            ),
            2000,
        ),
    }
    path = Path("reports/stage6c-benchmark.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
