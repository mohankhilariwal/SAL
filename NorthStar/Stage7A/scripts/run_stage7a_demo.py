#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
from dataclasses import asdict
from pathlib import Path
import tempfile

from northstar_compliance.concurrency.execution import AsyncExecutionCoordinator
from northstar_compliance.concurrency.fixtures import reference_handlers
from northstar_compliance.concurrency.models import BranchSpec, ConcurrencyPolicy


async def main() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        checkpoint = str(Path(temp_dir) / "stage7a-checkpoint.json")
        policy = ConcurrencyPolicy(global_limit=4, per_case_limit=2, queue_capacity=8)
        specs = [
            BranchSpec("jurisdiction-ca", 1, "analyze_jurisdiction", {"jurisdiction": "CA", "delay_s": 0.04}),
            BranchSpec("jurisdiction-us", 2, "analyze_jurisdiction", {"jurisdiction": "US", "delay_s": 0.02}),
            BranchSpec("evidence-policies", 3, "retrieve_evidence", {"source": "policy-library", "documents": ["POL-14", "POL-29"], "delay_s": 0.03}),
            BranchSpec("mapping-lending", 4, "map_policy", {"business_unit": "Lending", "policy_ids": ["POL-14"], "delay_s": 0.01}),
        ]
        async with AsyncExecutionCoordinator(policy, reference_handlers(), checkpoint) as coordinator:
            records, aggregation = await coordinator.run_fanout(
                case_id="CASE-2026-0801-001",
                run_id="RUN-S07A-DEMO",
                task_id="TASK-INDEPENDENT-ANALYSIS",
                specs=specs,
            )
            print(json.dumps({
                "records": [record.to_dict() for record in records],
                "aggregation": aggregation.to_dict(),
                "queue_health": asdict(coordinator.pool.health()),
                "invariants": {
                    "active_agents": ["AGT-001"],
                    "orchestration_owner": "CMP-003",
                    "authority_issuer": "CMP-007",
                    "concurrent_protected_writes": False
                }
            }, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    asyncio.run(main())
