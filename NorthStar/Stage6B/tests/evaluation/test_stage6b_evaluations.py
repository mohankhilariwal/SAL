import json
from pathlib import Path

from northstar_compliance.handoff.fixtures import build_signed_fixture

ROOT = Path(__file__).resolve().parents[2]


def test_306_evaluation_register_is_complete_and_fixture_digest_is_deterministic():
    data = json.loads((ROOT / "config/evaluation/stage6b-cases.json").read_text())
    assert data["evaluation_ids"] == [f"EVAL-{n:03d}" for n in range(62, 70)]
    assert build_signed_fixture()["fixture_digest"] == build_signed_fixture()["fixture_digest"]
