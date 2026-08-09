from __future__ import annotations

import asyncio
from pathlib import Path
import time

from northstar_compliance.concurrency.execution import AsyncExecutionCoordinator
from northstar_compliance.concurrency.fixtures import (
    reference_handlers,
    reset_fixture_state,
    side_effect_count,
)
from northstar_compliance.concurrency.models import (
    AggregationPolicy,
    BranchSpec,
    BranchStatus,
    ConcurrencyPolicy,
    WorkKind,
)


def run(coro):
    return asyncio.run(coro)


def test_378_parallel_fanout_is_faster_than_sequential_wait(tmp_path: Path) -> None:
    async def scenario() -> None:
        policy = ConcurrencyPolicy(global_limit=3, per_case_limit=3, queue_capacity=6)
        specs = [BranchSpec(f"b{i}", i, "analyze_jurisdiction", {"jurisdiction": "CA", "delay_s": 0.05}) for i in range(3)]
        start = time.perf_counter()
        async with AsyncExecutionCoordinator(policy, reference_handlers(), str(tmp_path / "c.json")) as c:
            records, agg = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=specs)
        elapsed = time.perf_counter() - start
        assert elapsed < 0.14
        assert agg.complete
        assert all(r.status is BranchStatus.SUCCEEDED for r in records)
    run(scenario())


def test_379_fan_in_order_is_ordinal_not_completion_order(tmp_path: Path) -> None:
    async def scenario() -> None:
        specs = [
            BranchSpec("slow", 1, "analyze_jurisdiction", {"jurisdiction": "CA", "delay_s": 0.04}),
            BranchSpec("fast", 2, "analyze_jurisdiction", {"jurisdiction": "US", "delay_s": 0.001}),
        ]
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=2, per_case_limit=2, queue_capacity=4), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, agg = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=specs)
        assert [r.branch_id for r in records] == ["slow", "fast"]
        assert agg.ordered_branch_ids == ("slow", "fast")
    run(scenario())


def test_380_transient_retry_recovers(tmp_path: Path) -> None:
    async def scenario() -> None:
        reset_fixture_state()
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[BranchSpec("retry", 1, "transient_then_success", {"key": "r", "transient_failures": 2})])
        assert records[0].status is BranchStatus.SUCCEEDED
        assert records[0].attempts == 3
    run(scenario())


def test_381_transient_retry_exhaustion_fails(tmp_path: Path) -> None:
    async def scenario() -> None:
        reset_fixture_state()
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2, max_attempts=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, agg = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[BranchSpec("retry", 1, "transient_then_success", {"key": "r", "transient_failures": 5})])
        assert records[0].status is BranchStatus.FAILED
        assert records[0].error_code == "TRANSIENT_RETRIES_EXHAUSTED"
        assert not agg.complete
    run(scenario())


def test_382_permanent_failure_is_not_retried(tmp_path: Path) -> None:
    async def scenario() -> None:
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[BranchSpec("fail", 1, "permanent_failure", {})])
        assert records[0].status is BranchStatus.FAILED
        assert records[0].attempts == 0
    run(scenario())


def test_383_branch_timeout_is_recorded(tmp_path: Path) -> None:
    async def scenario() -> None:
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2, branch_timeout_s=0.02), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[BranchSpec("slow", 1, "analyze_jurisdiction", {"jurisdiction": "CA", "delay_s": 0.2})])
        assert records[0].status is BranchStatus.TIMED_OUT
    run(scenario())


def test_384_duplicate_execution_runs_handler_once(tmp_path: Path) -> None:
    async def scenario() -> None:
        reset_fixture_state()
        policy = ConcurrencyPolicy(global_limit=2, per_case_limit=2, queue_capacity=4)
        spec = BranchSpec("dup", 1, "counted_read", {"key": "x", "delay_s": 0.03})
        async with AsyncExecutionCoordinator(policy, reference_handlers(), str(tmp_path / "c.json")) as c:
            one, two = await asyncio.gather(
                c.run_fanout(case_id="C", run_id="R", task_id="T1", specs=[spec]),
                c.run_fanout(case_id="C", run_id="R", task_id="T2", specs=[spec]),
            )
        statuses = {one[0][0].status, two[0][0].status}
        assert statuses == {BranchStatus.SUCCEEDED, BranchStatus.DUPLICATE}
        assert side_effect_count("x") == 1
    run(scenario())


def test_385_minimum_successes_allows_partial_completion(tmp_path: Path) -> None:
    async def scenario() -> None:
        specs = [
            BranchSpec("ok", 1, "analyze_jurisdiction", {"jurisdiction": "CA"}),
            BranchSpec("bad", 2, "permanent_failure", {}),
        ]
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=2, per_case_limit=2, queue_capacity=4), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, agg = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=specs, aggregation_policy=AggregationPolicy.MINIMUM_SUCCESSES, minimum_successes=1)
        assert agg.complete and agg.partial
        assert len(records) == 2
    run(scenario())


def test_386_all_required_fails_when_one_branch_fails(tmp_path: Path) -> None:
    async def scenario() -> None:
        specs = [
            BranchSpec("ok", 1, "analyze_jurisdiction", {"jurisdiction": "CA"}),
            BranchSpec("bad", 2, "permanent_failure", {}),
        ]
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=2, per_case_limit=2, queue_capacity=4), reference_handlers(), str(tmp_path / "c.json")) as c:
            _, agg = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=specs)
        assert not agg.complete
    run(scenario())


def test_387_first_satisfactory_cancels_losers(tmp_path: Path) -> None:
    async def scenario() -> None:
        specs = [
            BranchSpec("slow", 1, "scored_candidate", {"candidate": "slow", "score": 0.8, "delay_s": 0.15}),
            BranchSpec("winner", 2, "scored_candidate", {"candidate": "win", "score": 0.95, "delay_s": 0.01}),
            BranchSpec("slower", 3, "scored_candidate", {"candidate": "slower", "score": 0.99, "delay_s": 0.2}),
        ]
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=3, per_case_limit=3, queue_capacity=6), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, agg = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=specs, aggregation_policy=AggregationPolicy.FIRST_SATISFACTORY, satisfactory=lambda r: bool(r.output) and r.output["score"] >= 0.9)
        assert agg.winner_branch_id == "winner"
        assert any(r.status is BranchStatus.CANCELLED for r in records)
    run(scenario())


def test_388_external_cancellation_propagates(tmp_path: Path) -> None:
    async def scenario() -> None:
        event = asyncio.Event()
        specs = [BranchSpec("slow", 1, "analyze_jurisdiction", {"jurisdiction": "CA", "delay_s": 0.2})]
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            task = asyncio.create_task(c.run_fanout(case_id="C", run_id="R", task_id="T", specs=specs, cancellation_event=event))
            await asyncio.sleep(0.02)
            event.set()
            records, _ = await task
        assert records[0].status is BranchStatus.CANCELLED
    run(scenario())


def test_389_concurrency_disabled_runs_sequentially(tmp_path: Path) -> None:
    async def scenario() -> None:
        policy = ConcurrencyPolicy(enabled=False, global_limit=2, per_case_limit=2, queue_capacity=4)
        specs = [BranchSpec(f"b{i}", i, "analyze_jurisdiction", {"jurisdiction": "CA", "delay_s": 0.03}) for i in range(2)]
        start = time.perf_counter()
        async with AsyncExecutionCoordinator(policy, reference_handlers(), str(tmp_path / "c.json")) as c:
            records, agg = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=specs)
        elapsed = time.perf_counter() - start
        assert elapsed >= 0.055
        assert agg.complete and len(records) == 2
    run(scenario())


def test_390_resume_skips_successful_branches(tmp_path: Path) -> None:
    async def scenario() -> None:
        reset_fixture_state()
        policy = ConcurrencyPolicy(global_limit=2, per_case_limit=2, queue_capacity=4)
        specs = [
            BranchSpec("done", 1, "counted_read", {"key": "done"}),
            BranchSpec("later", 2, "counted_read", {"key": "later"}),
        ]
        async with AsyncExecutionCoordinator(policy, reference_handlers(), str(tmp_path / "c.json")) as c:
            await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[specs[0]])
            records, agg = await c.resume_incomplete(case_id="C", run_id="R", task_id="T", specs=specs)
        assert agg.complete
        assert side_effect_count("done") == 1
        assert side_effect_count("later") == 1
        assert [r.branch_id for r in records] == ["done", "later"]
    run(scenario())


def test_391_queue_health_reports_limits(tmp_path: Path) -> None:
    async def scenario() -> None:
        policy = ConcurrencyPolicy(global_limit=2, per_case_limit=1, queue_capacity=4)
        async with AsyncExecutionCoordinator(policy, reference_handlers(), str(tmp_path / "c.json")) as c:
            health = c.pool.health()
        assert health.worker_limit == 2
        assert health.queue_capacity == 4
    run(scenario())


def test_392_unique_branch_ids_are_required(tmp_path: Path) -> None:
    async def scenario() -> None:
        specs = [
            BranchSpec("same", 1, "analyze_jurisdiction", {"jurisdiction": "CA"}),
            BranchSpec("same", 2, "analyze_jurisdiction", {"jurisdiction": "US"}),
        ]
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=2, per_case_limit=2, queue_capacity=4), reference_handlers(), str(tmp_path / "c.json")) as c:
            try:
                await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=specs)
            except ValueError as exc:
                assert "unique" in str(exc)
            else:
                raise AssertionError("expected duplicate branch-id rejection")
    run(scenario())
