from pathlib import Path

from northstar_compliance.agent.decision import ScriptedDecisionProvider
from northstar_compliance.agent.factory import build_agent_runtime, default_goal, default_principal
from northstar_compliance.agent.models import AgentDecision, DecisionKind, RunStatus, TerminationReason


def test_test078_happy_path_completes_with_human_review(tmp_path: Path):
    root = Path(__file__).parents[2]
    runtime = build_agent_runtime(root, tmp_path)
    state, outcome, path = runtime.run(default_goal(), default_principal())
    assert outcome.status == RunStatus.COMPLETED
    assert outcome.termination_reason == TerminationReason.GOAL_COMPLETE
    assert outcome.final_disposition == "preliminary_grounded_unapproved"
    assert outcome.human_review_required is True
    assert state.artifacts["draft_case"]["status"] == "draft_unapproved"
    assert state.artifacts["candidate_mapping"]["status"] == "candidate_unapproved"
    assert state.artifacts["review_request"]["status"] == "queued_for_human_review"
    assert path.exists()


def test_test079_invalid_early_completion_escalates(tmp_path: Path):
    root = Path(__file__).parents[2]
    provider = ScriptedDecisionProvider([
        AgentDecision(DecisionKind.COMPLETE, "The model claims the goal is complete.", "Stop now.")
    ])
    runtime = build_agent_runtime(root, tmp_path, provider)
    _, outcome, _ = runtime.run(default_goal(), default_principal())
    assert outcome.status == RunStatus.ESCALATED
    assert outcome.termination_reason == TerminationReason.INVALID_COMPLETION


def test_test080_max_iterations_stops_partial_run(tmp_path: Path):
    root = Path(__file__).parents[2]
    runtime = build_agent_runtime(root, tmp_path)
    _, outcome, _ = runtime.run(default_goal(), default_principal(), max_iterations=1)
    assert outcome.status == RunStatus.TERMINATED_GUARD
    assert outcome.termination_reason == TerminationReason.ITERATION_LIMIT
    assert outcome.final_disposition == "preliminary_grounded_unapproved"


def test_test081_repeated_action_terminates(tmp_path: Path):
    root = Path(__file__).parents[2]
    repeat = AgentDecision(
        DecisionKind.CALL_TOOL,
        "Repeat the same search.",
        "Search again.",
        "TOOL-001", "1.0.0",
        {"query": "automated credit controls", "jurisdictions": ["CA"], "max_results": 5},
    )
    provider = ScriptedDecisionProvider([repeat, repeat, repeat, repeat])
    runtime = build_agent_runtime(root, tmp_path, provider)
    _, outcome, _ = runtime.run(default_goal(), default_principal(), repeat_limit=2, no_progress_limit=10)
    assert outcome.status == RunStatus.TERMINATED_GUARD
    assert outcome.termination_reason == TerminationReason.REPEATED_ACTION


def test_test082_explicit_escalation_returns_control(tmp_path: Path):
    root = Path(__file__).parents[2]
    provider = ScriptedDecisionProvider([
        AgentDecision(DecisionKind.ESCALATE, "The publication identity is ambiguous.", "Request analyst clarification.")
    ])
    runtime = build_agent_runtime(root, tmp_path, provider)
    _, outcome, _ = runtime.run(default_goal(), default_principal())
    assert outcome.status == RunStatus.ESCALATED
    assert outcome.termination_reason == TerminationReason.HUMAN_ESCALATION
