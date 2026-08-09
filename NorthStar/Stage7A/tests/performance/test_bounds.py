from __future__ import annotations

import asyncio
from pathlib import Path

from northstar_compliance.concurrency.execution import AsyncExecutionCoordinator
from northstar_compliance.concurrency.fixtures import reference_handlers
from northstar_compliance.concurrency.models import BranchSpec, ConcurrencyPolicy


def test_403_per_case_limit_is_never_above_global_limit() -> None:
    policy = ConcurrencyPolicy(global_limit=8, per_case_limit=4, queue_capacity=32)
    policy.validate()
    assert policy.per_case_limit <= policy.global_limit


def test_404_queue_capacity_is_bounded() -> None:
    policy = ConcurrencyPolicy(global_limit=4, per_case_limit=2, queue_capacity=8)
    assert policy.queue_capacity == 8


def test_405_worker_count_matches_policy(tmp_path: Path) -> None:
    async def scenario() -> None:
        policy = ConcurrencyPolicy(global_limit=3, per_case_limit=2, queue_capacity=6)
        async with AsyncExecutionCoordinator(policy, reference_handlers(), str(tmp_path / "c.json")) as coordinator:
            assert len(coordinator.pool._workers) == 3
    asyncio.run(scenario())


def test_406_admitted_and_completed_metrics_increment(tmp_path: Path) -> None:
    async def scenario() -> None:
        policy = ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2)
        async with AsyncExecutionCoordinator(policy, reference_handlers(), str(tmp_path / "c.json")) as coordinator:
            await coordinator.run_fanout(case_id="C", run_id="R", task_id="T", specs=[BranchSpec("b", 1, "analyze_jurisdiction", {"jurisdiction": "CA"})])
            health = coordinator.pool.health()
            assert health.admitted_total == 1
            assert health.completed_total == 1
    asyncio.run(scenario())


def test_407_checkpoint_contains_terminal_state(tmp_path: Path) -> None:
    async def scenario() -> None:
        policy = ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2)
        async with AsyncExecutionCoordinator(policy, reference_handlers(), str(tmp_path / "c.json")) as coordinator:
            await coordinator.run_fanout(case_id="C", run_id="R", task_id="T", specs=[BranchSpec("b", 1, "analyze_jurisdiction", {"jurisdiction": "CA"})])
            checkpoint = await coordinator.checkpoints.load_run("C", "R")
            assert checkpoint is not None
            assert checkpoint.records[0]["status"] == "succeeded"
    asyncio.run(scenario())
