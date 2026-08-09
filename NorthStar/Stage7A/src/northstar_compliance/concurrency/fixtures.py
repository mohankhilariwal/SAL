"""Deterministic local handlers for Stage 7A demonstrations and tests."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, Mapping

from .errors import PermanentBranchError, TransientBranchError
from .execution import BranchExecutionContext, Handler

_ATTEMPTS: dict[str, int] = defaultdict(int)
_SIDE_EFFECT_COUNTER: dict[str, int] = defaultdict(int)


def reset_fixture_state() -> None:
    _ATTEMPTS.clear()
    _SIDE_EFFECT_COUNTER.clear()


def side_effect_count(key: str) -> int:
    return _SIDE_EFFECT_COUNTER[key]


async def _cooperative_delay(seconds: float, context: BranchExecutionContext) -> None:
    remaining = max(0.0, seconds)
    while remaining > 0:
        context.ensure_active()
        step = min(0.01, remaining)
        await asyncio.sleep(step)
        remaining -= step
    context.ensure_active()


async def analyze_jurisdiction(
    payload: Mapping[str, Any],
    context: BranchExecutionContext,
) -> dict[str, Any]:
    await _cooperative_delay(float(payload.get("delay_s", 0.01)), context)
    jurisdiction = str(payload["jurisdiction"])
    return {
        "jurisdiction": jurisdiction,
        "applicable": jurisdiction in {"CA", "US", "EU"},
        "evidence_ids": list(payload.get("evidence_ids", [])),
        "worker_id": context.worker_id,
    }


async def retrieve_evidence(
    payload: Mapping[str, Any],
    context: BranchExecutionContext,
) -> dict[str, Any]:
    await _cooperative_delay(float(payload.get("delay_s", 0.01)), context)
    source = str(payload["source"])
    return {
        "source": source,
        "artefacts": [f"{source}:{item}" for item in payload.get("documents", [])],
        "immutable_snapshot": True,
        "worker_id": context.worker_id,
    }


async def map_policy(
    payload: Mapping[str, Any],
    context: BranchExecutionContext,
) -> dict[str, Any]:
    await _cooperative_delay(float(payload.get("delay_s", 0.01)), context)
    business_unit = str(payload["business_unit"])
    return {
        "business_unit": business_unit,
        "candidate_policies": list(payload.get("policy_ids", [])),
        "proposal_only": True,
        "worker_id": context.worker_id,
    }


async def transient_then_success(
    payload: Mapping[str, Any],
    context: BranchExecutionContext,
) -> dict[str, Any]:
    key = str(payload.get("key", "default"))
    _ATTEMPTS[key] += 1
    await _cooperative_delay(float(payload.get("delay_s", 0.0)), context)
    if _ATTEMPTS[key] <= int(payload.get("transient_failures", 1)):
        raise TransientBranchError(f"simulated transient failure for {key}")
    return {"key": key, "attempt": _ATTEMPTS[key], "recovered": True}


async def permanent_failure(
    payload: Mapping[str, Any],
    context: BranchExecutionContext,
) -> dict[str, Any]:
    await _cooperative_delay(float(payload.get("delay_s", 0.0)), context)
    raise PermanentBranchError(str(payload.get("message", "simulated permanent failure")))


async def counted_read(
    payload: Mapping[str, Any],
    context: BranchExecutionContext,
) -> dict[str, Any]:
    key = str(payload.get("key", "counted"))
    await _cooperative_delay(float(payload.get("delay_s", 0.02)), context)
    _SIDE_EFFECT_COUNTER[key] += 1
    return {"key": key, "count": _SIDE_EFFECT_COUNTER[key], "read_only_simulation": True}


async def scored_candidate(
    payload: Mapping[str, Any],
    context: BranchExecutionContext,
) -> dict[str, Any]:
    await _cooperative_delay(float(payload.get("delay_s", 0.01)), context)
    return {
        "candidate": str(payload["candidate"]),
        "score": float(payload["score"]),
        "worker_id": context.worker_id,
    }


def reference_handlers() -> dict[str, Handler]:
    return {
        "analyze_jurisdiction": analyze_jurisdiction,
        "retrieve_evidence": retrieve_evidence,
        "map_policy": map_policy,
        "transient_then_success": transient_then_success,
        "permanent_failure": permanent_failure,
        "counted_read": counted_read,
        "scored_candidate": scored_candidate,
    }
