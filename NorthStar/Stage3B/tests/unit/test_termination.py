from northstar_compliance.agent.factory import default_goal
from northstar_compliance.agent.models import AgentRunState, RunStatus, TerminationReason
from northstar_compliance.agent.termination import TerminationEvaluator


def make_state(**kwargs):
    return AgentRunState("1.0.0", "RUN-TEST", "AGT-001", default_goal(), **kwargs)


def test_test076_iteration_guard_terminates():
    state = make_state(max_iterations=0)
    assert TerminationEvaluator().pre_iteration(state)
    assert state.status == RunStatus.TERMINATED_GUARD
    assert state.termination_reason == TerminationReason.ITERATION_LIMIT


def test_test077_completion_invariant_requires_all_artifacts():
    state = make_state()
    assert not TerminationEvaluator.completion_invariants_met(state)
