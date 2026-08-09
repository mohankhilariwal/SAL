"""Bounded concurrency primitives for NorthStar Stage 7A."""

from .errors import (
    AdmissionRejected,
    AuthorityInvariantViolation,
    IdempotencyConflict,
    PermanentBranchError,
    TransientBranchError,
)
from .execution import AsyncExecutionCoordinator, BoundedAsyncWorkerPool
from .models import (
    AggregationPolicy,
    BranchExecutionRecord,
    BranchSpec,
    BranchStatus,
    ConcurrencyPolicy,
    WorkKind,
)

__all__ = [
    "AdmissionRejected",
    "AuthorityInvariantViolation",
    "IdempotencyConflict",
    "PermanentBranchError",
    "TransientBranchError",
    "AsyncExecutionCoordinator",
    "BoundedAsyncWorkerPool",
    "AggregationPolicy",
    "BranchExecutionRecord",
    "BranchSpec",
    "BranchStatus",
    "ConcurrencyPolicy",
    "WorkKind",
]
