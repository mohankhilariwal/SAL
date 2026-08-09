from __future__ import annotations

import pytest

from northstar_compliance.concurrency.models import (
    BranchSpec,
    ConcurrencyPolicy,
    WorkKind,
    canonical_digest,
)


def test_361_canonical_digest_is_order_independent() -> None:
    assert canonical_digest({"a": 1, "b": 2}) == canonical_digest({"b": 2, "a": 1})


def test_362_branch_input_digest_is_stable() -> None:
    one = BranchSpec("b", 1, "h", {"x": 1, "y": 2})
    two = BranchSpec("b", 1, "h", {"y": 2, "x": 1})
    assert one.input_digest == two.input_digest


def test_363_idempotency_key_scopes_case_run_graph_and_branch() -> None:
    spec = BranchSpec("b", 1, "h", {"x": 1})
    key = spec.idempotency_key("CASE", "RUN", "GRAPH-001/1.2.0")
    assert key != spec.idempotency_key("CASE-2", "RUN", "GRAPH-001/1.2.0")
    assert key != spec.idempotency_key("CASE", "RUN-2", "GRAPH-001/1.2.0")


def test_364_policy_defaults_allow_only_read_and_compute() -> None:
    policy = ConcurrencyPolicy()
    assert policy.allowed_work_kinds == (WorkKind.READ_ONLY, WorkKind.PURE_COMPUTE)


def test_365_policy_rejects_invalid_global_limit() -> None:
    with pytest.raises(ValueError):
        ConcurrencyPolicy(global_limit=0).validate()


def test_366_policy_rejects_per_case_above_global() -> None:
    with pytest.raises(ValueError):
        ConcurrencyPolicy(global_limit=2, per_case_limit=3).validate()


def test_367_policy_rejects_small_queue() -> None:
    with pytest.raises(ValueError):
        ConcurrencyPolicy(global_limit=4, per_case_limit=2, queue_capacity=3).validate()


def test_368_policy_rejects_invalid_jitter() -> None:
    with pytest.raises(ValueError):
        ConcurrencyPolicy(jitter_ratio=1.1).validate()
