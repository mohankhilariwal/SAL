import pytest

from governed_release.domain.enums import Scenario


def test_arbitrary_destination_is_not_exported(service) -> None:
    state = service.run_scenario(Scenario.INTERNAL_ALLOW)
    candidate = service.settings.data_dir / "candidate" / f"{state.candidate_id}_v1.csv"
    state.request.destination = "../outside"
    state.stage = "EVALUATED"
    with pytest.raises(PermissionError):
        service.export_gateway.release(
            state, candidate, service.settings.data_dir / "evidence" / state.workflow_id
        )


def test_export_is_idempotent(service) -> None:
    state = service.run_scenario(Scenario.INTERNAL_ALLOW)
    candidate = service.settings.data_dir / "candidate" / f"{state.candidate_id}_v1.csv"
    evidence = service.settings.data_dir / "evidence" / state.workflow_id
    receipt = service.export_gateway.release(state, candidate, evidence)
    assert receipt.idempotency_key == state.export_receipt.idempotency_key
