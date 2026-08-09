from northstar_compliance.reliability.chaos import ChaosHarness


def test_local_chaos_invariant_passes():
    state = {"dependency": True, "effect": False}
    result = ChaosHarness().run("C1", lambda: state.update(dependency=False), lambda: not state["dependency"] and not state["effect"])
    assert result.injected and result.invariant_passed


def test_local_chaos_can_report_invariant_failure():
    result = ChaosHarness().run("C2", lambda: None, lambda: False)
    assert not result.invariant_passed
