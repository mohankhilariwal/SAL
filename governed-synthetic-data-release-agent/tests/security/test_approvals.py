import pytest

from governed_release.domain.enums import ApprovalRole, Scenario


def test_requester_cannot_self_approve(service) -> None:
    state = service.run_scenario(Scenario.EXTERNAL_APPROVAL)
    with pytest.raises(PermissionError):
        service.approve(
            state.workflow_id, ApprovalRole.DATA_OWNER, state.request.requester.id, "self approval"
        )


def test_duplicate_approval_is_rejected(service) -> None:
    state = service.run_scenario(Scenario.EXTERNAL_APPROVAL)
    service.approve(state.workflow_id, ApprovalRole.DATA_OWNER, "data_owner_001", "first")
    with pytest.raises(ValueError):
        service.approve(state.workflow_id, ApprovalRole.DATA_OWNER, "data_owner_002", "duplicate")
