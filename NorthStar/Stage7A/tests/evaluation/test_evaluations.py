from __future__ import annotations

from northstar_compliance.concurrency.evaluation import run_evaluations_sync


def test_401_all_stage7a_evaluations_pass() -> None:
    results = run_evaluations_sync()
    assert len(results) == 10
    assert all(item["passed"] for item in results)


def test_402_evaluation_ids_are_contiguous() -> None:
    results = run_evaluations_sync()
    assert [item["evaluation_id"] for item in results] == [f"EVAL-{n:03d}" for n in range(79, 89)]
