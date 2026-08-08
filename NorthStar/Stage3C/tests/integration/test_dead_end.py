from conftest import make_runtime


def test_101_no_progress_triggers_bounded_replan_then_completes(tmp_path, goal, principal):
    runtime, _, _ = make_runtime(tmp_path, {"TOOL-001": ["empty_success", "empty_success"]}, no_progress_window=1)
    out = runtime.run(goal, principal)
    assert out.status == "completed"
    assert any(r["action"] == "bounded_replan" for r in out.recovery_records)
    assert out.budget_ledger["replans"] >= 1
