from governed_release.domain.enums import Scenario


def test_workflow_persists(service) -> None:
    state = service.run_scenario(Scenario.PROMPT_INJECTION)
    loaded = service.store.get(state.workflow_id)
    assert loaded.workflow_id == state.workflow_id
    assert loaded.security_events == state.security_events
