import pytest

from northstar_compliance.interoperability.adapters.a2a import A2AMappingAdapter, NORTHSTAR_EXTENSION
from northstar_compliance.interoperability.fixtures import build_fixture


def test_336_agent_card_preserves_candidate_status():
    f = build_fixture()
    card = A2AMappingAdapter().build_agent_card(f["recipient"], endpoint_url="https://invalid.example/a2a")
    assert card["metadata"]["northstarRuntimeStatus"] == "candidate_sandbox_only"
    assert card["metadata"]["northstarNoAgentAllocation"] is True


def test_337_agent_card_requires_extension():
    f = build_fixture()
    card = A2AMappingAdapter().build_agent_card(f["recipient"], endpoint_url="https://invalid.example/a2a")
    extension = card["capabilities"]["extensions"][0]
    assert extension["uri"] == NORTHSTAR_EXTENSION and extension["required"] is True


def test_338_a2a_message_maps_task_and_context():
    f = build_fixture()
    message = A2AMappingAdapter().map_task_message(f["envelope"])["message"]
    assert message["taskId"] == f["envelope"].task_id
    assert message["contextId"] == f["envelope"].correlation_id


def test_339_a2a_message_preserves_security_metadata():
    f = build_fixture()
    metadata = A2AMappingAdapter().map_task_message(f["envelope"])["message"]["metadata"]
    assert metadata["northstarGrantDigest"] == f["grant"].digest
    assert metadata["northstarTerminationOwner"] == "CMP-003"
    assert metadata["northstarNotApproval"] is True


def test_340_a2a_with_extension_conforms():
    f = build_fixture()
    adapter = A2AMappingAdapter()
    assert adapter.conformance_for_message(adapter.map_task_message(f["envelope"], include_extension=True)).result == "pass"


def test_341_a2a_without_extension_fails():
    f = build_fixture()
    adapter = A2AMappingAdapter()
    result = adapter.conformance_for_message(adapter.map_task_message(f["envelope"], include_extension=False))
    assert result.result == "fail" and "required_northstar_extension_declaration" in result.lost_fields


@pytest.mark.parametrize(
    "state,expected",
    [
        ("offered", "TASK_STATE_SUBMITTED"),
        ("running", "TASK_STATE_WORKING"),
        ("completed", "TASK_STATE_COMPLETED"),
        ("failed", "TASK_STATE_FAILED"),
        ("cancelled", "TASK_STATE_CANCELED"),
        ("rejected", "TASK_STATE_REJECTED"),
    ],
)
def test_342_status_mapping(state, expected):
    assert A2AMappingAdapter().map_status(state) == expected


def test_343_unknown_status_fails():
    with pytest.raises(ValueError, match="unsupported"):
        A2AMappingAdapter().map_status("mystery")
