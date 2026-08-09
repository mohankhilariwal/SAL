import json
from pathlib import Path
import pytest

from northstar_compliance.workload.adapters import build_aiperf_plan


def test_438_profiles_disable_raw_payload_capture(root):
    for path in (root / "config/workloads").glob("WP-*.json"):
        assert json.loads(path.read_text())["capture_payloads"] is False


def test_439_profiles_record_tokenizer_identity(root):
    for path in (root / "config/workloads").glob("WP-*.json"):
        assert json.loads(path.read_text())["tokenizer_id"]


def test_440_inactive_multi_agent_profile_is_not_executable(inactive_profile):
    with pytest.raises(ValueError):
        build_aiperf_plan(inactive_profile, endpoint="http://localhost", model="x")


def test_441_no_authority_fields_in_workload_profiles(root):
    forbidden = {"approval_grant", "authorization_token", "credential", "route_owner"}
    for path in (root / "config/workloads").glob("WP-*.json"):
        text = path.read_text().lower()
        assert not any(item in text for item in forbidden)


def test_442_capacity_script_does_not_modify_concurrency_config(root):
    text = (root / "scripts/run_stage7b_capacity_plan.py").read_text()
    assert "config/concurrency" not in text and "write_json(args.output" in text
