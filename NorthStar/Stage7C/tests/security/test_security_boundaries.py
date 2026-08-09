from dataclasses import asdict
import json

from northstar_compliance.inference.planner import build_recommendation


def test_497_no_raw_payload_fields_in_configs(root):
    for path in root.glob("config/**/*.json"):
        text = path.read_text(encoding="utf-8")
        assert '"prompt"' not in text and '"response"' not in text


def test_498_recommendation_cannot_mutate_admission(wp2, local_deployment):
    rec = build_recommendation(wp2, local_deployment)
    assert not rec.may_mutate_admission


def test_499_recommendation_cannot_grant_authority(wp2, local_deployment):
    rec = build_recommendation(wp2, local_deployment)
    assert not rec.may_grant_authority


def test_500_cache_scope_is_authorization_bound(scenario):
    policy = scenario.policy.cache_policy
    assert policy.tenant_isolated and policy.authorization_scope_bound


def test_501_semantic_cache_flag_absent_from_selected_policy(scenario):
    assert not scenario.policy.semantic_response_cache_enabled
