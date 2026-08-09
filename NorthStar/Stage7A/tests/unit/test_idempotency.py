from __future__ import annotations

import asyncio

import pytest

from northstar_compliance.concurrency.errors import IdempotencyConflict
from northstar_compliance.concurrency.idempotency import InMemoryIdempotencyStore


def test_369_first_execution_is_not_duplicate() -> None:
    async def scenario() -> None:
        store = InMemoryIdempotencyStore()
        value, duplicate = await store.execute_once("k", "d", lambda: asyncio.sleep(0, result=7))
        assert value == 7
        assert duplicate is False
    asyncio.run(scenario())


def test_370_second_execution_reuses_result() -> None:
    async def scenario() -> None:
        store = InMemoryIdempotencyStore()
        counter = 0
        async def producer() -> int:
            nonlocal counter
            counter += 1
            return counter
        assert await store.execute_once("k", "d", producer) == (1, False)
        assert await store.execute_once("k", "d", producer) == (1, True)
        assert counter == 1
    asyncio.run(scenario())


def test_371_concurrent_duplicate_waits_for_owner() -> None:
    async def scenario() -> None:
        store = InMemoryIdempotencyStore()
        counter = 0
        async def producer() -> str:
            nonlocal counter
            counter += 1
            await asyncio.sleep(0.02)
            return "done"
        first, second = await asyncio.gather(
            store.execute_once("k", "d", producer),
            store.execute_once("k", "d", producer),
        )
        assert {first[1], second[1]} == {False, True}
        assert first[0] == second[0] == "done"
        assert counter == 1
    asyncio.run(scenario())


def test_372_key_digest_conflict_fails_closed() -> None:
    async def scenario() -> None:
        store = InMemoryIdempotencyStore()
        await store.execute_once("k", "d1", lambda: asyncio.sleep(0, result=1))
        with pytest.raises(IdempotencyConflict):
            await store.execute_once("k", "d2", lambda: asyncio.sleep(0, result=2))
    asyncio.run(scenario())


def test_373_failure_is_replayed_to_duplicate() -> None:
    async def scenario() -> None:
        store = InMemoryIdempotencyStore()
        async def fail() -> int:
            raise RuntimeError("boom")
        with pytest.raises(RuntimeError, match="boom"):
            await store.execute_once("k", "d", fail)
        with pytest.raises(RuntimeError, match="boom"):
            await store.execute_once("k", "d", fail)
    asyncio.run(scenario())


def test_374_snapshot_records_state() -> None:
    async def scenario() -> None:
        store = InMemoryIdempotencyStore()
        await store.execute_once("k", "d", lambda: asyncio.sleep(0, result=1))
        snapshot = await store.snapshot()
        assert snapshot["k"]["state"] == "succeeded"
        assert snapshot["k"]["has_output"] is True
    asyncio.run(scenario())
