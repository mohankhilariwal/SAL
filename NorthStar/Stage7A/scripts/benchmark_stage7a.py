#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
from pathlib import Path
import tempfile
import time

from northstar_compliance.concurrency.execution import AsyncExecutionCoordinator
from northstar_compliance.concurrency.fixtures import reference_handlers
from northstar_compliance.concurrency.models import BranchSpec, ConcurrencyPolicy


async def run_once(enabled: bool) -> float:
    with tempfile.TemporaryDirectory() as temp_dir:
        policy = ConcurrencyPolicy(
            enabled=enabled,
            global_limit=4,
            per_case_limit=4,
            queue_capacity=8,
            branch_timeout_s=2.0,
        )
        specs = [
            BranchSpec(f"b-{index}", index, "analyze_jurisdiction", {"jurisdiction": "CA", "delay_s": 0.05})
            for index in range(1, 5)
        ]
        start = time.perf_counter()
        async with AsyncExecutionCoordinator(
            policy,
            reference_handlers(),
            str(Path(temp_dir) / "checkpoint.json"),
        ) as coordinator:
            await coordinator.run_fanout(
                case_id="CASE-BENCH",
                run_id=f"RUN-{enabled}",
                task_id="TASK-BENCH",
                specs=specs,
            )
        return time.perf_counter() - start


async def main_async() -> dict[str, float]:
    sequential = await run_once(False)
    concurrent = await run_once(True)
    return {
        "sequential_seconds": round(sequential, 6),
        "concurrent_seconds": round(concurrent, 6),
        "observed_speedup": round(sequential / concurrent, 3) if concurrent else 0.0,
        "note": "Local deterministic I/O-wait simulation; not a production SLO or cost benchmark."
    }


def main() -> None:
    payload = asyncio.run(main_async())
    output = Path(__file__).resolve().parents[1] / "reports" / "benchmark-report.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
