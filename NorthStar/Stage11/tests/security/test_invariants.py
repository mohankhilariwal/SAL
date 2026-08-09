import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("num", [279, 280, 281])
def test_schema_authority_effect_none(num):
    schema = json.loads((ROOT / f"schemas/DATA-{num}.schema.json").read_text())
    assert schema["properties"]["authority_effect"]["const"] == "none"


def test_final_assessment_route_disabled():
    cfg = json.loads((ROOT / "config/capstone/final-assessment.json").read_text())
    assert cfg["production_route_enabled"] is False


def test_exactly_one_active_agent():
    cfg = json.loads((ROOT / "config/capstone/final-assessment.json").read_text())
    assert cfg["active_agent_count"] == 1


def test_multi_agent_candidate_inactive():
    cfg = json.loads((ROOT / "config/capstone/topology-comparison.json").read_text())
    assert cfg["multi_agent_candidate"]["status"] == "inactive_future"


def test_no_agent_is_accountable_in_raci():
    cfg = json.loads((ROOT / "config/capstone/raci.json").read_text())
    assert cfg["agent_accountable_for_any_activity"] is False


def test_all_blockers_have_no_authority():
    cfg = json.loads((ROOT / "config/capstone/final-assessment.json").read_text())
    assert all(item["authority_effect"] == "none" for item in cfg["blockers"])


def test_release_manifest_is_non_authorizing():
    manifest = json.loads((ROOT / "reports/stage11-release-manifest.json").read_text())
    assert manifest["id"] == "DATA-287"
    assert manifest["version"] == "1.0.0"
    assert manifest["authority_effect"] == "none"
    assert manifest["payload"]["production_route_enabled"] is False


def test_checksum_manifest_verifies_stage_and_handoff():
    import hashlib

    lines = (ROOT / "Stage11-SHA256SUMS.txt").read_text().splitlines()
    recorded = {}
    for line in lines:
        digest, rel = line.split("  ", 1)
        recorded[rel] = digest
    for rel in (
        "docs/stages/NorthStar-Stage-11-Final-Capstone.md",
        "docs/source-of-truth/09-Stage-Handoff-Pack.md",
    ):
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        assert recorded[rel] == actual
