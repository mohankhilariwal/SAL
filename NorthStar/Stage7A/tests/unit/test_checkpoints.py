from __future__ import annotations

import asyncio
from pathlib import Path

from northstar_compliance.concurrency.checkpoints import JsonCheckpointStore
from northstar_compliance.concurrency.models import BranchExecutionRecord, BranchStatus


def test_375_checkpoint_round_trip(tmp_path: Path) -> None:
    async def scenario() -> None:
        store = JsonCheckpointStore(tmp_path / "checkpoint.json")
        record = BranchExecutionRecord("C", "R", "T", "B", 1, BranchStatus.SUCCEEDED, 1, output={"x": 1})
        await store.save_record(record, "GRAPH-001/1.2.0")
        loaded = await store.load_run("C", "R")
        assert loaded is not None
        assert loaded.graph_version == "GRAPH-001/1.2.0"
        assert loaded.records[0]["branch_id"] == "B"
    asyncio.run(scenario())


def test_376_checkpoint_missing_run_returns_none(tmp_path: Path) -> None:
    async def scenario() -> None:
        store = JsonCheckpointStore(tmp_path / "checkpoint.json")
        assert await store.load_run("C", "R") is None
    asyncio.run(scenario())


def test_377_checkpoint_orders_records_by_ordinal(tmp_path: Path) -> None:
    async def scenario() -> None:
        store = JsonCheckpointStore(tmp_path / "checkpoint.json")
        await store.save_record(BranchExecutionRecord("C", "R", "T", "B2", 2, BranchStatus.SUCCEEDED, 1), "G")
        await store.save_record(BranchExecutionRecord("C", "R", "T", "B1", 1, BranchStatus.SUCCEEDED, 1), "G")
        loaded = await store.load_run("C", "R")
        assert loaded is not None
        assert [r["branch_id"] for r in loaded.records] == ["B1", "B2"]
    asyncio.run(scenario())
