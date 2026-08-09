from northstar_compliance.handoff.artifacts import InMemoryArtifactStore
from northstar_compliance.handoff.fixtures import build_signed_fixture
from northstar_compliance.handoff.lifecycle import HandoffCoordinator
from northstar_compliance.handoff.models import HandoffStatus
from northstar_compliance.handoff.simulator import SequentialHandoffSandbox


def test_298_contract_sandbox_executes_sequential_verification():
    f = build_signed_fixture()
    coordinator = HandoffCoordinator()
    sandbox = SequentialHandoffSandbox(
        sender=f["sender"], recipient=f["recipient"], authority=f["authority"], envelopes=f["envelopes"],
        coordinator=coordinator, artifacts=InMemoryArtifactStore()
    )
    receipt, output = sandbox.execute_verification(
        envelope=f["envelope"], grant=f["child"], input_content=f["content"], now=f["now"]
    )
    assert receipt.accepted
    assert output.schema_id == "DATA-096"
    assert coordinator.current(f["envelope"].envelope_id).status is HandoffStatus.COMPLETED
    assert len(coordinator.events(f["envelope"].envelope_id)) == 4


def test_299_contract_sandbox_does_not_activate_candidate_runtime():
    f = build_signed_fixture()
    assert f["recipient"].runtime_status == "candidate_sandbox_only"
    assert f["policy"].active_agent_ids == ("AGT-001",)
    assert f["policy"].current_runtime_mode == "contract_sandbox_only"


def test_300_candidate_has_no_tool_memory_route_or_approval_authority():
    f = build_signed_fixture()
    r = f["recipient"]
    assert r.allowed_tools == ()
    assert not r.may_write_memory
    assert not r.may_route
    assert not r.may_approve
    assert not r.may_finalize
    assert not r.may_delegate
    assert not r.may_run_concurrently
