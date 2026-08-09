"""Bounded async execution, fan-out/fan-in, retry, cancellation and resumption."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass
import random
import time
from typing import Any, Awaitable, Callable, Mapping

from .checkpoints import JsonCheckpointStore
from .errors import (
    AdmissionRejected,
    AuthorityInvariantViolation,
    PermanentBranchError,
    TransientBranchError,
)
from .idempotency import InMemoryIdempotencyStore
from .models import (
    AggregationPolicy,
    BranchExecutionRecord,
    BranchSpec,
    BranchStatus,
    ConcurrencyPolicy,
    FanInAggregationRecord,
    QueueHealthSnapshot,
    WorkItemEnvelope,
    WorkKind,
    canonical_digest,
)


@dataclass(frozen=True, slots=True)
class BranchExecutionContext:
    attempt: int
    worker_id: str
    cancellation_event: asyncio.Event
    deadline_epoch_s: float

    def ensure_active(self) -> None:
        if self.cancellation_event.is_set():
            raise asyncio.CancelledError("branch cancellation requested")
        if time.time() >= self.deadline_epoch_s:
            raise TimeoutError("branch deadline exceeded")


Handler = Callable[[Mapping[str, Any], BranchExecutionContext], Awaitable[Any]]


@dataclass(slots=True)
class _Ticket:
    envelope: WorkItemEnvelope
    future: asyncio.Future[BranchExecutionRecord]
    cancellation_event: asyncio.Event


class BoundedAsyncWorkerPool:
    """Shared bounded worker pool with queue backpressure and per-case fairness cap."""

    def __init__(
        self,
        policy: ConcurrencyPolicy,
        handlers: Mapping[str, Handler],
        idempotency: InMemoryIdempotencyStore,
        checkpoints: JsonCheckpointStore,
    ) -> None:
        policy.validate()
        self.policy = policy
        self.handlers = dict(handlers)
        self.idempotency = idempotency
        self.checkpoints = checkpoints
        self.queue: asyncio.Queue[_Ticket | None] = asyncio.Queue(maxsize=policy.queue_capacity)
        self._workers: list[asyncio.Task[None]] = []
        self._case_semaphores: dict[str, asyncio.Semaphore] = defaultdict(
            lambda: asyncio.Semaphore(policy.per_case_limit)
        )
        self._started = False
        self._active_workers = 0
        self._admitted_total = 0
        self._rejected_total = 0
        self._completed_total = 0
        self._duplicate_total = 0

    async def start(self) -> None:
        if self._started:
            return
        self._workers = [
            asyncio.create_task(self._worker_loop(index), name=f"northstar-worker-{index}")
            for index in range(self.policy.global_limit)
        ]
        self._started = True

    async def close(self) -> None:
        if not self._started:
            return
        for _ in self._workers:
            await self.queue.put(None)
        await asyncio.gather(*self._workers)
        self._workers.clear()
        self._started = False

    async def submit(
        self,
        envelope: WorkItemEnvelope,
        cancellation_event: asyncio.Event,
    ) -> asyncio.Future[BranchExecutionRecord]:
        if not self._started:
            await self.start()
        loop = asyncio.get_running_loop()
        future: asyncio.Future[BranchExecutionRecord] = loop.create_future()
        ticket = _Ticket(envelope=envelope, future=future, cancellation_event=cancellation_event)
        try:
            await asyncio.wait_for(
                self.queue.put(ticket),
                timeout=self.policy.admission_timeout_s,
            )
        except TimeoutError as exc:
            self._rejected_total += 1
            raise AdmissionRejected("bounded work queue admission timed out") from exc
        self._admitted_total += 1
        return future

    def health(self) -> QueueHealthSnapshot:
        return QueueHealthSnapshot(
            queue_capacity=self.policy.queue_capacity,
            queued=self.queue.qsize(),
            active_workers=self._active_workers,
            worker_limit=self.policy.global_limit,
            admitted_total=self._admitted_total,
            rejected_total=self._rejected_total,
            completed_total=self._completed_total,
            duplicate_total=self._duplicate_total,
        )

    async def _worker_loop(self, worker_index: int) -> None:
        worker_id = f"worker-{worker_index:02d}"
        while True:
            ticket = await self.queue.get()
            if ticket is None:
                self.queue.task_done()
                return
            self._active_workers += 1
            try:
                async with self._case_semaphores[ticket.envelope.case_id]:
                    record = await self._execute_ticket(ticket, worker_id)
                if not ticket.future.cancelled() and not ticket.future.done():
                    ticket.future.set_result(record)
            except BaseException as exc:
                if not ticket.future.cancelled() and not ticket.future.done():
                    ticket.future.set_exception(exc)
            finally:
                self._active_workers -= 1
                self._completed_total += 1
                self.queue.task_done()

    async def _execute_ticket(self, ticket: _Ticket, worker_id: str) -> BranchExecutionRecord:
        env = ticket.envelope
        started = time.time()
        record = BranchExecutionRecord(
            case_id=env.case_id,
            run_id=env.run_id,
            task_id=env.task_id,
            branch_id=env.branch_id,
            ordinal=env.ordinal,
            status=BranchStatus.RUNNING,
            attempts=0,
            started_epoch_s=started,
            idempotency_key=env.idempotency_key,
            input_digest=env.input_digest,
            worker_id=worker_id,
        )
        await self.checkpoints.save_record(record, env.graph_version)

        try:
            self._validate_authority(env)
            if ticket.cancellation_event.is_set():
                raise asyncio.CancelledError("cancelled before execution")
            handler = self.handlers.get(env.handler)
            if handler is None:
                raise PermanentBranchError(f"unknown handler: {env.handler}")

            attempt_counter = 0

            async def producer() -> Any:
                nonlocal attempt_counter
                for attempt in range(1, self.policy.max_attempts + 1):
                    attempt_counter = attempt
                    context = BranchExecutionContext(
                        attempt=attempt,
                        worker_id=worker_id,
                        cancellation_event=ticket.cancellation_event,
                        deadline_epoch_s=env.deadline_epoch_s,
                    )
                    try:
                        context.ensure_active()
                        remaining = max(0.001, env.deadline_epoch_s - time.time())
                        return await asyncio.wait_for(
                            handler(env.payload, context),
                            timeout=remaining,
                        )
                    except TransientBranchError:
                        if attempt >= self.policy.max_attempts:
                            raise
                        backoff = min(
                            self.policy.max_backoff_s,
                            self.policy.base_backoff_s * (2 ** (attempt - 1)),
                        )
                        seed = int(env.input_digest[:12], 16) + attempt
                        rng = random.Random(seed)
                        jitter = backoff * self.policy.jitter_ratio * rng.random()
                        await asyncio.sleep(backoff + jitter)
                raise AssertionError("unreachable")

            output, duplicate = await self.idempotency.execute_once(
                env.idempotency_key,
                env.input_digest,
                producer,
            )
            record.output = output
            record.attempts = max(1, attempt_counter)
            record.status = BranchStatus.DUPLICATE if duplicate else BranchStatus.SUCCEEDED
            if duplicate:
                record.duplicate_of = env.idempotency_key
                self._duplicate_total += 1
        except asyncio.CancelledError as exc:
            record.status = BranchStatus.CANCELLED
            record.error_code = "CANCELLED"
            record.error_message = str(exc)
        except TimeoutError as exc:
            record.status = BranchStatus.TIMED_OUT
            record.error_code = "TIMEOUT"
            record.error_message = str(exc)
        except AuthorityInvariantViolation as exc:
            record.status = BranchStatus.REJECTED
            record.error_code = "AUTHORITY_INVARIANT"
            record.error_message = str(exc)
        except PermanentBranchError as exc:
            record.status = BranchStatus.FAILED
            record.error_code = "PERMANENT_FAILURE"
            record.error_message = str(exc)
        except TransientBranchError as exc:
            record.status = BranchStatus.FAILED
            record.error_code = "TRANSIENT_RETRIES_EXHAUSTED"
            record.error_message = str(exc)
            record.attempts = self.policy.max_attempts
        except Exception as exc:  # deterministic evidence for unexpected reference failures
            record.status = BranchStatus.FAILED
            record.error_code = type(exc).__name__
            record.error_message = str(exc)
        finally:
            record.completed_epoch_s = time.time()
            await self.checkpoints.save_record(record, env.graph_version)
        return record

    def _validate_authority(self, env: WorkItemEnvelope) -> None:
        if env.agent_id != "AGT-001":
            raise AuthorityInvariantViolation("Stage 7A permits exactly one active AGT-001")
        if env.orchestrator_component != "CMP-003":
            raise AuthorityInvariantViolation("CMP-003 must remain the orchestration owner")
        if env.authority_issuer != "CMP-007":
            raise AuthorityInvariantViolation("CMP-007 must remain the sole authority issuer")
        if env.work_kind not in self.policy.allowed_work_kinds:
            raise AuthorityInvariantViolation(
                f"concurrent work kind {env.work_kind.value} is not allowed"
            )
        forbidden_claims = {
            "approve",
            "finalize",
            "route_case",
            "mutate_protected_state",
            "grant_authority",
            "create_agent",
            "terminate_system",
            "write_shared_memory",
        }
        overlap = forbidden_claims.intersection(env.authority_claims)
        if overlap:
            raise AuthorityInvariantViolation(
                f"branch requested prohibited authority claims: {sorted(overlap)}"
            )


class AsyncExecutionCoordinator:
    """CMP-003-owned fan-out/fan-in controller.

    AGT-001 remains the only active agent. Branches are workflow work items,
    not agents, and cannot approve, route, finalize, grant authority, or mutate
    protected state.
    """

    def __init__(
        self,
        policy: ConcurrencyPolicy,
        handlers: Mapping[str, Handler],
        checkpoint_path: str,
    ) -> None:
        self.policy = policy
        self.idempotency = InMemoryIdempotencyStore()
        self.checkpoints = JsonCheckpointStore(checkpoint_path)
        self.pool = BoundedAsyncWorkerPool(
            policy,
            handlers,
            self.idempotency,
            self.checkpoints,
        )

    async def __aenter__(self) -> "AsyncExecutionCoordinator":
        await self.pool.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.pool.close()

    def make_envelope(
        self,
        *,
        case_id: str,
        run_id: str,
        task_id: str,
        spec: BranchSpec,
        graph_version: str = "GRAPH-001/1.2.0",
    ) -> WorkItemEnvelope:
        timeout_s = spec.timeout_s or self.policy.branch_timeout_s
        return WorkItemEnvelope(
            case_id=case_id,
            run_id=run_id,
            task_id=task_id,
            branch_id=spec.branch_id,
            ordinal=spec.ordinal,
            handler=spec.handler,
            payload=spec.payload,
            work_kind=spec.work_kind,
            required=spec.required,
            input_digest=spec.input_digest,
            idempotency_key=spec.idempotency_key(case_id, run_id, graph_version),
            deadline_epoch_s=time.time() + timeout_s,
            graph_version=graph_version,
            authority_claims=spec.authority_claims,
        )

    async def run_fanout(
        self,
        *,
        case_id: str,
        run_id: str,
        task_id: str,
        specs: list[BranchSpec],
        aggregation_policy: AggregationPolicy = AggregationPolicy.ALL_REQUIRED,
        minimum_successes: int | None = None,
        satisfactory: Callable[[BranchExecutionRecord], bool] | None = None,
        cancellation_event: asyncio.Event | None = None,
    ) -> tuple[list[BranchExecutionRecord], FanInAggregationRecord]:
        if not self.policy.enabled:
            return await self._run_sequential_disabled(
                case_id=case_id,
                run_id=run_id,
                task_id=task_id,
                specs=specs,
                aggregation_policy=aggregation_policy,
                minimum_successes=minimum_successes,
            )
        if len({spec.branch_id for spec in specs}) != len(specs):
            raise ValueError("branch_id values must be unique within a fan-out")
        cancel = cancellation_event or asyncio.Event()
        futures: list[asyncio.Future[BranchExecutionRecord]] = []
        admission_records: list[BranchExecutionRecord] = []
        for spec in sorted(specs, key=lambda item: item.ordinal):
            env = self.make_envelope(
                case_id=case_id,
                run_id=run_id,
                task_id=task_id,
                spec=spec,
            )
            try:
                future = await self.pool.submit(env, cancel)
            except AdmissionRejected as exc:
                record = BranchExecutionRecord(
                    case_id=case_id,
                    run_id=run_id,
                    task_id=task_id,
                    branch_id=spec.branch_id,
                    ordinal=spec.ordinal,
                    status=BranchStatus.REJECTED,
                    attempts=0,
                    completed_epoch_s=time.time(),
                    error_code="BACKPRESSURE_REJECTION",
                    error_message=str(exc),
                    idempotency_key=env.idempotency_key,
                    input_digest=env.input_digest,
                )
                await self.checkpoints.save_record(record, env.graph_version)
                admission_records.append(record)
            else:
                futures.append(future)

        records = list(admission_records)
        winner: BranchExecutionRecord | None = None
        if aggregation_policy is AggregationPolicy.FIRST_SATISFACTORY:
            predicate = satisfactory or (
                lambda record: record.status in {BranchStatus.SUCCEEDED, BranchStatus.DUPLICATE}
            )
            pending = set(futures)
            while pending:
                done, pending = await asyncio.wait(
                    pending,
                    return_when=asyncio.FIRST_COMPLETED,
                )
                for future in done:
                    record = await future
                    records.append(record)
                    if winner is None and predicate(record):
                        winner = record
                        cancel.set()
                if winner is not None:
                    # Cooperative cancellation is authoritative. Await pending futures so
                    # terminal cancellation records are checkpointed and returned.
                    break
            if pending:
                settled = await asyncio.gather(*pending, return_exceptions=True)
                for item in settled:
                    if isinstance(item, BranchExecutionRecord):
                        records.append(item)
            # Load checkpointed cancellation records that may not have surfaced through cancelled futures.
            checkpoint = await self.checkpoints.load_run(case_id, run_id)
            if checkpoint:
                known = {record.branch_id for record in records}
                for item in checkpoint.records:
                    if item["branch_id"] not in known:
                        records.append(self._record_from_dict(item))
        else:
            settled = await asyncio.gather(*futures, return_exceptions=True)
            for item in settled:
                if isinstance(item, BranchExecutionRecord):
                    records.append(item)
                elif isinstance(item, BaseException):
                    raise item

        records.sort(key=lambda record: record.ordinal)
        required = minimum_successes
        if required is None:
            required = sum(1 for spec in specs if spec.required)
            if aggregation_policy is AggregationPolicy.FIRST_SATISFACTORY:
                required = 1
        aggregation = self._aggregate(
            case_id=case_id,
            run_id=run_id,
            task_id=task_id,
            records=records,
            policy=aggregation_policy,
            required_successes=required,
            winner=winner,
        )
        return records, aggregation

    async def resume_incomplete(
        self,
        *,
        case_id: str,
        run_id: str,
        task_id: str,
        specs: list[BranchSpec],
    ) -> tuple[list[BranchExecutionRecord], FanInAggregationRecord]:
        checkpoint = await self.checkpoints.load_run(case_id, run_id)
        completed_ids: set[str] = set()
        existing: list[BranchExecutionRecord] = []
        if checkpoint:
            for item in checkpoint.records:
                record = self._record_from_dict(item)
                existing.append(record)
                if record.status in {BranchStatus.SUCCEEDED, BranchStatus.DUPLICATE}:
                    completed_ids.add(record.branch_id)
        pending_specs = [spec for spec in specs if spec.branch_id not in completed_ids]
        new_records: list[BranchExecutionRecord] = []
        if pending_specs:
            new_records, _ = await self.run_fanout(
                case_id=case_id,
                run_id=run_id,
                task_id=task_id,
                specs=pending_specs,
            )
        by_id = {record.branch_id: record for record in existing}
        by_id.update({record.branch_id: record for record in new_records})
        records = sorted(by_id.values(), key=lambda record: record.ordinal)
        aggregation = self._aggregate(
            case_id=case_id,
            run_id=run_id,
            task_id=task_id,
            records=records,
            policy=AggregationPolicy.ALL_REQUIRED,
            required_successes=sum(1 for spec in specs if spec.required),
            winner=None,
        )
        return records, aggregation

    async def _run_sequential_disabled(
        self,
        *,
        case_id: str,
        run_id: str,
        task_id: str,
        specs: list[BranchSpec],
        aggregation_policy: AggregationPolicy,
        minimum_successes: int | None,
    ) -> tuple[list[BranchExecutionRecord], FanInAggregationRecord]:
        cancel = asyncio.Event()
        records: list[BranchExecutionRecord] = []
        for spec in sorted(specs, key=lambda item: item.ordinal):
            env = self.make_envelope(
                case_id=case_id,
                run_id=run_id,
                task_id=task_id,
                spec=spec,
            )
            # Directly use the same validated execution path, one submitted item at a time.
            future = await self.pool.submit(env, cancel)
            records.append(await future)
        required = minimum_successes or sum(1 for spec in specs if spec.required)
        return records, self._aggregate(
            case_id=case_id,
            run_id=run_id,
            task_id=task_id,
            records=records,
            policy=aggregation_policy,
            required_successes=required,
            winner=None,
        )

    def _aggregate(
        self,
        *,
        case_id: str,
        run_id: str,
        task_id: str,
        records: list[BranchExecutionRecord],
        policy: AggregationPolicy,
        required_successes: int,
        winner: BranchExecutionRecord | None,
    ) -> FanInAggregationRecord:
        successful_statuses = {BranchStatus.SUCCEEDED, BranchStatus.DUPLICATE}
        successful = [r for r in records if r.status in successful_statuses]
        failed = [r for r in records if r.status in {BranchStatus.FAILED, BranchStatus.TIMED_OUT, BranchStatus.REJECTED}]
        cancelled = [r for r in records if r.status is BranchStatus.CANCELLED]
        complete = len(successful) >= required_successes
        partial = bool(successful) and (bool(failed) or bool(cancelled))
        digest = canonical_digest([record.to_dict() for record in sorted(records, key=lambda r: r.ordinal)])
        return FanInAggregationRecord(
            case_id=case_id,
            run_id=run_id,
            task_id=task_id,
            policy=policy,
            required_successes=required_successes,
            ordered_branch_ids=tuple(r.branch_id for r in sorted(records, key=lambda r: r.ordinal)),
            successful_branch_ids=tuple(r.branch_id for r in successful),
            failed_branch_ids=tuple(r.branch_id for r in failed),
            cancelled_branch_ids=tuple(r.branch_id for r in cancelled),
            complete=complete,
            partial=partial,
            winner_branch_id=winner.branch_id if winner else None,
            aggregate_digest=digest,
        )

    @staticmethod
    def _record_from_dict(item: Mapping[str, Any]) -> BranchExecutionRecord:
        return BranchExecutionRecord(
            case_id=str(item["case_id"]),
            run_id=str(item["run_id"]),
            task_id=str(item["task_id"]),
            branch_id=str(item["branch_id"]),
            ordinal=int(item["ordinal"]),
            status=BranchStatus(str(item["status"])),
            attempts=int(item.get("attempts", 0)),
            started_epoch_s=item.get("started_epoch_s"),
            completed_epoch_s=item.get("completed_epoch_s"),
            output=item.get("output"),
            error_code=item.get("error_code"),
            error_message=item.get("error_message"),
            duplicate_of=item.get("duplicate_of"),
            idempotency_key=item.get("idempotency_key"),
            input_digest=item.get("input_digest"),
            worker_id=item.get("worker_id"),
            warnings=list(item.get("warnings", [])),
        )
