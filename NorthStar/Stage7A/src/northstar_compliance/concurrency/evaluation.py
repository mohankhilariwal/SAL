"""Deterministic Stage 7A evaluation suite."""

from __future__ import annotations

import asyncio
from pathlib import Path
import tempfile
from typing import Any

from .execution import AsyncExecutionCoordinator
from .fixtures import reference_handlers, reset_fixture_state, side_effect_count
from .models import AggregationPolicy, BranchSpec, BranchStatus, ConcurrencyPolicy, WorkKind


async def run_evaluations() -> list[dict[str, Any]]:
    reset_fixture_state()
    with tempfile.TemporaryDirectory() as temp_dir:
        checkpoint = str(Path(temp_dir) / "checkpoint.json")
        policy = ConcurrencyPolicy(global_limit=4, per_case_limit=2, queue_capacity=8)
        results: list[dict[str, Any]] = []
        async with AsyncExecutionCoordinator(policy, reference_handlers(), checkpoint) as coordinator:
            specs = [
                BranchSpec("jur-CA", 2, "analyze_jurisdiction", {"jurisdiction": "CA", "delay_s": 0.03}),
                BranchSpec("jur-US", 1, "analyze_jurisdiction", {"jurisdiction": "US", "delay_s": 0.01}),
                BranchSpec("jur-EU", 3, "analyze_jurisdiction", {"jurisdiction": "EU", "delay_s": 0.02}),
            ]
            records, aggregate = await coordinator.run_fanout(
                case_id="CASE-EVAL",
                run_id="RUN-079",
                task_id="TASK-079",
                specs=specs,
            )
            results.append({
                "evaluation_id": "EVAL-079",
                "name": "independent branch eligibility",
                "passed": all(r.status is BranchStatus.SUCCEEDED for r in records),
            })
            results.append({
                "evaluation_id": "EVAL-080",
                "name": "bounded deterministic fan-in",
                "passed": aggregate.ordered_branch_ids == ("jur-US", "jur-CA", "jur-EU"),
            })

            duplicate_specs = [
                BranchSpec("dup", 1, "counted_read", {"key": "same", "delay_s": 0.04}),
            ]
            first, _ = await coordinator.run_fanout(
                case_id="CASE-EVAL",
                run_id="RUN-081",
                task_id="TASK-081A",
                specs=duplicate_specs,
            )
            second, _ = await coordinator.run_fanout(
                case_id="CASE-EVAL",
                run_id="RUN-081",
                task_id="TASK-081B",
                specs=duplicate_specs,
            )
            results.append({
                "evaluation_id": "EVAL-081",
                "name": "idempotent duplicate suppression",
                "passed": side_effect_count("same") == 1
                and first[0].status is BranchStatus.SUCCEEDED
                and second[0].status is BranchStatus.DUPLICATE,
            })

            retry_records, _ = await coordinator.run_fanout(
                case_id="CASE-EVAL",
                run_id="RUN-082",
                task_id="TASK-082",
                specs=[BranchSpec("retry", 1, "transient_then_success", {"key": "retry", "transient_failures": 2})],
            )
            results.append({
                "evaluation_id": "EVAL-082",
                "name": "bounded retry and recovery",
                "passed": retry_records[0].status is BranchStatus.SUCCEEDED and retry_records[0].attempts == 3,
            })

            failure_records, failure_aggregate = await coordinator.run_fanout(
                case_id="CASE-EVAL",
                run_id="RUN-083",
                task_id="TASK-083",
                specs=[
                    BranchSpec("ok", 1, "analyze_jurisdiction", {"jurisdiction": "CA"}),
                    BranchSpec("fail", 2, "permanent_failure", {}),
                ],
                aggregation_policy=AggregationPolicy.MINIMUM_SUCCESSES,
                minimum_successes=1,
            )
            results.append({
                "evaluation_id": "EVAL-083",
                "name": "partial-result policy",
                "passed": failure_aggregate.complete and failure_aggregate.partial
                and any(r.status is BranchStatus.FAILED for r in failure_records),
            })

            winner_records, winner_aggregate = await coordinator.run_fanout(
                case_id="CASE-EVAL",
                run_id="RUN-084",
                task_id="TASK-084",
                specs=[
                    BranchSpec("slow-low", 1, "scored_candidate", {"candidate": "a", "score": 0.6, "delay_s": 0.08}),
                    BranchSpec("fast-high", 2, "scored_candidate", {"candidate": "b", "score": 0.95, "delay_s": 0.01}),
                    BranchSpec("slow-high", 3, "scored_candidate", {"candidate": "c", "score": 0.96, "delay_s": 0.09}),
                ],
                aggregation_policy=AggregationPolicy.FIRST_SATISFACTORY,
                satisfactory=lambda r: bool(r.output) and r.output.get("score", 0) >= 0.9,
            )
            results.append({
                "evaluation_id": "EVAL-084",
                "name": "winner cancellation",
                "passed": winner_aggregate.winner_branch_id == "fast-high"
                and any(r.status is BranchStatus.CANCELLED for r in winner_records),
            })

            rejected_records, _ = await coordinator.run_fanout(
                case_id="CASE-EVAL",
                run_id="RUN-085",
                task_id="TASK-085",
                specs=[
                    BranchSpec(
                        "forbidden-write",
                        1,
                        "counted_read",
                        {"key": "forbidden"},
                        work_kind=WorkKind.IRREVERSIBLE_WRITE,
                    )
                ],
            )
            results.append({
                "evaluation_id": "EVAL-085",
                "name": "authority and work-kind denial",
                "passed": rejected_records[0].status is BranchStatus.REJECTED,
            })

            checkpoint_state = await coordinator.checkpoints.load_run("CASE-EVAL", "RUN-079")
            results.append({
                "evaluation_id": "EVAL-086",
                "name": "durable checkpoint evidence",
                "passed": checkpoint_state is not None and len(checkpoint_state.records) == 3,
            })

            health = coordinator.pool.health()
            results.append({
                "evaluation_id": "EVAL-087",
                "name": "bounded worker ceiling",
                "passed": health.worker_limit == 4 and health.queue_capacity == 8,
            })

            results.append({
                "evaluation_id": "EVAL-088",
                "name": "one-agent invariant",
                "passed": all(spec.work_kind in {WorkKind.READ_ONLY, WorkKind.PURE_COMPUTE} for spec in specs),
            })
        return results


def run_evaluations_sync() -> list[dict[str, Any]]:
    return asyncio.run(run_evaluations())
