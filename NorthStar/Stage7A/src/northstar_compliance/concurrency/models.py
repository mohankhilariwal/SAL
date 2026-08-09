"""Typed Stage 7A data objects.

The runtime deliberately keeps orchestration, protected state, authorization,
human approval, and system termination outside branch handlers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
import hashlib
import json
import time
from typing import Any, Mapping


class WorkKind(StrEnum):
    READ_ONLY = "read_only"
    PURE_COMPUTE = "pure_compute"
    REVERSIBLE_WRITE = "reversible_write"
    IRREVERSIBLE_WRITE = "irreversible_write"


class BranchStatus(StrEnum):
    PENDING = "pending"
    ADMITTED = "admitted"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    DUPLICATE = "duplicate"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class AggregationPolicy(StrEnum):
    ALL_REQUIRED = "all_required"
    MINIMUM_SUCCESSES = "minimum_successes"
    FIRST_SATISFACTORY = "first_satisfactory"


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class ConcurrencyPolicy:
    policy_id: str = "CONC-POL-001"
    enabled: bool = True
    global_limit: int = 8
    per_case_limit: int = 4
    queue_capacity: int = 32
    admission_timeout_s: float = 0.25
    branch_timeout_s: float = 2.0
    max_attempts: int = 3
    base_backoff_s: float = 0.01
    max_backoff_s: float = 0.10
    jitter_ratio: float = 0.10
    allowed_work_kinds: tuple[WorkKind, ...] = (
        WorkKind.READ_ONLY,
        WorkKind.PURE_COMPUTE,
    )

    def validate(self) -> None:
        if self.global_limit < 1:
            raise ValueError("global_limit must be >= 1")
        if self.per_case_limit < 1 or self.per_case_limit > self.global_limit:
            raise ValueError("per_case_limit must be between 1 and global_limit")
        if self.queue_capacity < self.global_limit:
            raise ValueError("queue_capacity must be >= global_limit")
        if self.admission_timeout_s <= 0 or self.branch_timeout_s <= 0:
            raise ValueError("timeouts must be positive")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if not 0 <= self.jitter_ratio <= 1:
            raise ValueError("jitter_ratio must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class BranchSpec:
    branch_id: str
    ordinal: int
    handler: str
    payload: Mapping[str, Any]
    work_kind: WorkKind = WorkKind.READ_ONLY
    required: bool = True
    timeout_s: float | None = None
    authority_claims: tuple[str, ...] = ()

    @property
    def input_digest(self) -> str:
        return canonical_digest(
            {
                "branch_id": self.branch_id,
                "handler": self.handler,
                "payload": self.payload,
                "work_kind": self.work_kind,
                "required": self.required,
            }
        )

    def idempotency_key(self, case_id: str, run_id: str, graph_version: str) -> str:
        return canonical_digest(
            {
                "case_id": case_id,
                "run_id": run_id,
                "graph_version": graph_version,
                "branch_id": self.branch_id,
                "input_digest": self.input_digest,
            }
        )


@dataclass(frozen=True, slots=True)
class WorkItemEnvelope:
    case_id: str
    run_id: str
    task_id: str
    branch_id: str
    ordinal: int
    handler: str
    payload: Mapping[str, Any]
    work_kind: WorkKind
    required: bool
    input_digest: str
    idempotency_key: str
    deadline_epoch_s: float
    graph_version: str = "GRAPH-001/1.2.0"
    agent_id: str = "AGT-001"
    orchestrator_component: str = "CMP-003"
    runtime_component: str = "CMP-010"
    authority_issuer: str = "CMP-007"
    authority_claims: tuple[str, ...] = ()


@dataclass(slots=True)
class BranchExecutionRecord:
    case_id: str
    run_id: str
    task_id: str
    branch_id: str
    ordinal: int
    status: BranchStatus
    attempts: int
    started_epoch_s: float | None = None
    completed_epoch_s: float | None = None
    output: Any = None
    error_code: str | None = None
    error_message: str | None = None
    duplicate_of: str | None = None
    idempotency_key: str | None = None
    input_digest: str | None = None
    worker_id: str | None = None
    warnings: list[str] = field(default_factory=list)

    @property
    def latency_ms(self) -> float | None:
        if self.started_epoch_s is None or self.completed_epoch_s is None:
            return None
        return round((self.completed_epoch_s - self.started_epoch_s) * 1000, 3)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["latency_ms"] = self.latency_ms
        return data


@dataclass(frozen=True, slots=True)
class FanInAggregationRecord:
    case_id: str
    run_id: str
    task_id: str
    policy: AggregationPolicy
    required_successes: int
    ordered_branch_ids: tuple[str, ...]
    successful_branch_ids: tuple[str, ...]
    failed_branch_ids: tuple[str, ...]
    cancelled_branch_ids: tuple[str, ...]
    complete: bool
    partial: bool
    winner_branch_id: str | None
    aggregate_digest: str
    created_epoch_s: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["policy"] = self.policy.value
        return data


@dataclass(frozen=True, slots=True)
class CancellationRecord:
    case_id: str
    run_id: str
    requested_by: str
    reason: str
    requested_epoch_s: float
    scope: str = "workflow_branches_only"
    approval_effect: str = "none"
    termination_owner: str = "CMP-003"


@dataclass(frozen=True, slots=True)
class QueueHealthSnapshot:
    queue_capacity: int
    queued: int
    active_workers: int
    worker_limit: int
    admitted_total: int
    rejected_total: int
    completed_total: int
    duplicate_total: int
    captured_epoch_s: float = field(default_factory=time.time)


@dataclass(frozen=True, slots=True)
class ResumptionCheckpoint:
    case_id: str
    run_id: str
    graph_version: str
    records: tuple[dict[str, Any], ...]
    checkpoint_digest: str
    written_epoch_s: float
