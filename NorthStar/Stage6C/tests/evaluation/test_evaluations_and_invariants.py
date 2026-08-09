import json
from pathlib import Path

from northstar_compliance.interoperability.evaluation import run_evaluations
from northstar_compliance.interoperability.fixtures import build_fixture

ROOT = Path(__file__).resolve().parents[2]


def test_355_all_stage6c_evaluations_pass():
    records = run_evaluations()
    assert len(records) == 9
    assert all(record["passed"] for record in records)


def test_356_evaluation_ids_are_contiguous():
    assert [record["evaluation_id"] for record in run_evaluations()] == [f"EVAL-{i:03d}" for i in range(70, 79)]


def test_357_one_active_agent_config():
    config = json.loads((ROOT / "config/agents/candidate-endpoints-v1.json").read_text())
    assert len(config["activeAgents"]) == 1
    assert config["activeAgents"][0]["endpointId"] == "AGT-001"


def test_358_concurrency_disabled_config():
    policy = json.loads((ROOT / "config/architecture/interoperability-policy-v1.json").read_text())
    assert policy["concurrencyEnabled"] is False
    assert policy["sharedMutableStateEnabled"] is False
    assert policy["sharedAgentMemoryEnabled"] is False


def test_359_protocol_statuses_explicit():
    profiles = json.loads((ROOT / "config/protocols/protocol-profiles-v1.json").read_text())
    assert all(item["implementation_status"] for item in profiles)


def test_360_fixture_digest_is_deterministic():
    first = build_fixture()["envelope"].digest
    second = build_fixture()["envelope"].digest
    assert first == second
