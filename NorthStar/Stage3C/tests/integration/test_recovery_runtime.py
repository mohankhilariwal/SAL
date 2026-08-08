from northstar_compliance.agent.decision import DeterministicDecisionProvider, FlakyDecisionProvider
from northstar_compliance.agent.models import RuntimeBudget
from northstar_compliance.agent.cancellation import CancellationToken
from conftest import make_runtime


def test_093_happy_path_preserves_unapproved_semantics(tmp_path, goal, principal):
    runtime, _, _ = make_runtime(tmp_path)
    out = runtime.run(goal, principal)
    assert out.status == "completed"
    assert out.termination_reason == "goal_complete"
    assert out.final_disposition == "preliminary_grounded_unapproved"
    assert out.human_review_required is True


def test_094_read_transient_uses_fallback(tmp_path, goal, principal):
    runtime, primary, fallback = make_runtime(tmp_path, {"TOOL-001": ["transient"]})
    out = runtime.run(goal, principal)
    assert out.status == "completed"
    assert any(r["action"] == "tool_fallback" for r in out.recovery_records)
    assert fallback.call_counts["TOOL-001"] == 1


def test_095_ambiguous_write_reconciled_without_duplicate(tmp_path, goal, principal):
    runtime, primary, _ = make_runtime(tmp_path, {"TOOL-004": ["timeout_after_commit"]})
    out = runtime.run(goal, principal)
    assert out.status == "completed"
    assert len(primary.stores.drafts) == 1
    assert any(r["action"] == "reconcile_write" and r["outcome"] == "committed" for r in out.recovery_records)
    write_obs = [o for o in runtime.checkpoint_store.load(out.run_id).observations if o["tool_id"] == "TOOL-004"][0]
    assert write_obs["reconciled"] is True


def test_096_model_fallback(tmp_path, goal, principal):
    providers = [FlakyDecisionProvider(DeterministicDecisionProvider()), DeterministicDecisionProvider()]
    runtime, _, _ = make_runtime(tmp_path, providers=providers)
    out = runtime.run(goal, principal)
    assert out.status == "completed"
    assert any(r["action"] == "model_fallback" for r in out.recovery_records)


def test_097_tool_budget_partial_outcome(tmp_path, goal, principal):
    runtime, _, _ = make_runtime(tmp_path)
    out = runtime.run(goal, principal, budget=RuntimeBudget(max_tool_calls=2))
    assert out.status == "terminated_guard"
    assert out.termination_reason == "tool_call_budget_exhausted"
    assert len(out.completed_milestones) == 2
    assert out.missing_milestones


def test_098_failure_budget_exhaustion(tmp_path, goal, principal):
    runtime, _, _ = make_runtime(tmp_path, {"TOOL-004": ["timeout_before_dispatch", "timeout_before_dispatch"]})
    out = runtime.run(goal, principal, budget=RuntimeBudget(max_failures=1, max_retries=5))
    assert out.status == "terminated_guard"
    assert out.termination_reason == "failure_budget_exhausted"


def test_099_checkpoint_resume_does_not_repeat_completed_work(tmp_path, goal, principal):
    runtime, primary, _ = make_runtime(tmp_path)
    interim = runtime.run(goal, principal, max_new_iterations=3)
    assert interim.status == "running"
    first_counts = dict(primary.call_counts)
    final = runtime.run(goal, principal, resume_run_id=interim.run_id)
    assert final.status == "completed"
    assert primary.call_counts["TOOL-001"] == first_counts["TOOL-001"]
    assert primary.call_counts["TOOL-003"] == first_counts["TOOL-003"]
    assert primary.call_counts["TOOL-002"] == first_counts["TOOL-002"]


def test_100_external_cancellation_before_run(tmp_path, goal, principal):
    runtime, _, _ = make_runtime(tmp_path)
    token = CancellationToken()
    token.cancel("maya_cancelled")
    out = runtime.run(goal, principal, cancellation=token)
    assert out.status == "cancelled"
    assert out.termination_reason == "maya_cancelled"


def test_109_retry_budget_exhaustion(tmp_path, goal, principal):
    runtime, _, _ = make_runtime(tmp_path, {"TOOL-004": ["timeout_before_dispatch"]})
    out = runtime.run(goal, principal, budget=RuntimeBudget(max_retries=0))
    assert out.status == "terminated_guard"
    assert out.termination_reason == "retry_budget_exhausted"
