from __future__ import annotations

import asyncio
from pathlib import Path

from northstar_compliance.concurrency.execution import AsyncExecutionCoordinator
from northstar_compliance.concurrency.fixtures import reference_handlers
from northstar_compliance.concurrency.models import BranchSpec, BranchStatus, ConcurrencyPolicy, WorkKind


def run(coro):
    return asyncio.run(coro)


def test_393_irreversible_write_is_rejected(tmp_path: Path) -> None:
    async def scenario() -> None:
        spec = BranchSpec("w", 1, "counted_read", {"key": "x"}, work_kind=WorkKind.IRREVERSIBLE_WRITE)
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[spec])
        assert records[0].status is BranchStatus.REJECTED
    run(scenario())


def test_394_reversible_write_is_rejected_by_default(tmp_path: Path) -> None:
    async def scenario() -> None:
        spec = BranchSpec("w", 1, "counted_read", {"key": "x"}, work_kind=WorkKind.REVERSIBLE_WRITE)
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[spec])
        assert records[0].error_code == "AUTHORITY_INVARIANT"
    run(scenario())


def test_395_approval_claim_is_rejected(tmp_path: Path) -> None:
    async def scenario() -> None:
        spec = BranchSpec("a", 1, "counted_read", {"key": "x"}, authority_claims=("approve",))
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[spec])
        assert records[0].status is BranchStatus.REJECTED
    run(scenario())


def test_396_protected_state_claim_is_rejected(tmp_path: Path) -> None:
    async def scenario() -> None:
        spec = BranchSpec("a", 1, "counted_read", {"key": "x"}, authority_claims=("mutate_protected_state",))
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[spec])
        assert records[0].error_code == "AUTHORITY_INVARIANT"
    run(scenario())


def test_397_agent_creation_claim_is_rejected(tmp_path: Path) -> None:
    async def scenario() -> None:
        spec = BranchSpec("a", 1, "counted_read", {"key": "x"}, authority_claims=("create_agent",))
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[spec])
        assert records[0].status is BranchStatus.REJECTED
    run(scenario())


def test_398_shared_memory_claim_is_rejected(tmp_path: Path) -> None:
    async def scenario() -> None:
        spec = BranchSpec("a", 1, "counted_read", {"key": "x"}, authority_claims=("write_shared_memory",))
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[spec])
        assert records[0].status is BranchStatus.REJECTED
    run(scenario())


def test_399_termination_claim_is_rejected(tmp_path: Path) -> None:
    async def scenario() -> None:
        spec = BranchSpec("a", 1, "counted_read", {"key": "x"}, authority_claims=("terminate_system",))
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[spec])
        assert records[0].status is BranchStatus.REJECTED
    run(scenario())


def test_400_normal_read_only_branch_succeeds(tmp_path: Path) -> None:
    async def scenario() -> None:
        spec = BranchSpec("r", 1, "counted_read", {"key": "x"})
        async with AsyncExecutionCoordinator(ConcurrencyPolicy(global_limit=1, per_case_limit=1, queue_capacity=2), reference_handlers(), str(tmp_path / "c.json")) as c:
            records, _ = await c.run_fanout(case_id="C", run_id="R", task_id="T", specs=[spec])
        assert records[0].status is BranchStatus.SUCCEEDED
    run(scenario())
