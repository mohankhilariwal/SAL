from governed_release.domain.enums import Decision, Scenario


def test_global_kill_switch_suspends(service) -> None:
    service.set_kill_switch("global_workflow", True, "operator test")
    state = service.run_scenario(Scenario.INTERNAL_ALLOW)
    assert state.decision == Decision.SUSPEND
    assert state.export_receipt is None
