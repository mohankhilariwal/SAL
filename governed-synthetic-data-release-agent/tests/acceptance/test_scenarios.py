from pathlib import Path

import pandas as pd

from governed_release.application.evidence import verify_evidence_directory
from governed_release.domain.enums import ApprovalRole, Decision, Scenario, WorkflowStage


def test_scenario_1_internal_allow(service) -> None:
    state = service.run_scenario(Scenario.INTERNAL_ALLOW)
    assert state.decision == Decision.ALLOW
    assert state.stage == WorkflowStage.RELEASED
    assert state.generation_run.row_count == 5000
    released = Path(state.export_receipt.released_path)
    assert released.exists()
    assert not ({"customer_id", "account_number"} & set(pd.read_csv(released, nrows=1).columns))
    assert verify_evidence_directory(service.settings.data_dir / "evidence" / state.workflow_id)[0]


def test_scenario_2_pauses_for_two_approvals(service) -> None:
    state = service.run_scenario(Scenario.EXTERNAL_APPROVAL)
    assert state.decision == Decision.REQUIRE_APPROVAL
    assert state.stage == WorkflowStage.AWAITING_APPROVAL
    state = service.approve(
        state.workflow_id, ApprovalRole.DATA_OWNER, "data_owner_001", "Reviewed evidence"
    )
    state = service.resume(state.workflow_id)
    assert state.decision == Decision.REQUIRE_APPROVAL
    state = service.approve(
        state.workflow_id,
        ApprovalRole.PRIVACY_OFFICER,
        "privacy_officer_001",
        "Reviewed residual risk",
    )
    state = service.resume(state.workflow_id)
    assert state.decision == Decision.ALLOW
    assert state.stage == WorkflowStage.RELEASED
    assert len(state.approvals) == 2


def test_scenario_3_privacy_leakage_denied(service) -> None:
    state = service.run_scenario(Scenario.PRIVACY_LEAKAGE)
    assert state.decision == Decision.DENY
    assert state.stage == WorkflowStage.QUARANTINED
    assert not state.privacy_report.passed
    assert Path(state.generation_run.path).parent.name == "quarantine"
    assert state.export_receipt is None
    assert "Regenerate" in state.remediation_proposal


def test_scenario_4_injection_suspended(service) -> None:
    state = service.run_scenario(Scenario.PROMPT_INJECTION)
    assert state.decision == Decision.DENY
    assert state.stage == WorkflowStage.SUSPENDED
    assert state.security_events
    assert state.generation_run is None
    assert "POL-INJ-001" in state.policy_decision.triggered_policies
