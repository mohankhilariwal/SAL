import json
from pathlib import Path

from northstar_compliance.handoff.fixtures import build_signed_fixture

ROOT = Path(__file__).resolve().parents[2]


def test_301_configuration_keeps_exactly_one_active_agent():
    data = json.loads((ROOT / "config/agents/candidate-endpoints-v1.json").read_text())
    assert [a["endpoint_id"] for a in data["active_agents"]] == ["AGT-001"]


def test_302_no_protocol_or_concurrency_is_enabled():
    data = json.loads((ROOT / "config/architecture/handoff-policy-v1.json").read_text())
    assert data["protocol_selected"] is False
    assert data["mcp_enabled"] is False
    assert data["a2a_enabled"] is False
    assert data["concurrent_execution"] is False


def test_303_no_shared_mutable_state_or_shared_memory():
    data = json.loads((ROOT / "config/architecture/handoff-policy-v1.json").read_text())
    assert data["shared_mutable_state"] is False
    assert data["shared_agent_memory"] is False


def test_304_handoff_payload_excludes_raw_memory_and_credentials():
    f = build_signed_fixture()
    text = repr(f["envelope"]).lower()
    for forbidden in ("password", "secret", "access_token", "refresh_token", "case_working", "hidden_reasoning"):
        assert forbidden not in text


def test_305_grant_is_bound_to_case_run_task_and_audience():
    f = build_signed_fixture()
    g = f["child"]
    assert (g.case_id, g.run_id, g.task_id, g.audience) == (
        f["envelope"].case_id,
        f["envelope"].run_id,
        f["envelope"].task_id,
        f["recipient"].endpoint_id,
    )
