import pytest

from northstar_compliance.inference.models import OptimizationTechnique
from northstar_compliance.inference.planner import build_recommendation, build_selected_policy, recommend_techniques


def by_name(items):
    return {item.technique: item for item in items}


def test_464_long_document_selects_context_reduction(wp2, local_deployment):
    result = by_name(recommend_techniques(wp2, local_deployment))
    assert result[OptimizationTechnique.CONTEXT_REDUCTION].decision == "select"


def test_465_prefix_cache_selected_for_wp2(wp2, local_deployment):
    result = by_name(recommend_techniques(wp2, local_deployment))
    assert result[OptimizationTechnique.PREFIX_CACHING].decision == "select"


def test_466_semantic_cache_prohibited(wp2, local_deployment):
    result = by_name(recommend_techniques(wp2, local_deployment))
    assert result[OptimizationTechnique.SEMANTIC_RESPONSE_CACHING].decision == "prohibit"


def test_467_prompt_lookup_candidate_wp2(wp2, local_deployment):
    policy = build_selected_policy(wp2, local_deployment)
    assert policy.speculative_plan.enabled
    assert policy.speculative_plan.method == "prompt_lookup"


def test_468_tool_heavy_disables_speculation(wp5, local_deployment):
    policy = build_selected_policy(wp5, local_deployment)
    assert not policy.speculative_plan.enabled


def test_469_managed_hides_batching(wp2, managed_deployment):
    result = by_name(recommend_techniques(wp2, managed_deployment))
    assert result[OptimizationTechnique.CONTINUOUS_BATCHING].decision == "not_applicable"


def test_470_self_hosted_batch_profile_selects_continuous(root, self_hosted_deployment):
    from northstar_compliance.inference.io import load_workload
    wp6 = load_workload(root / "config/workloads/WP-006.json")
    policy = build_selected_policy(wp6, self_hosted_deployment)
    assert policy.batching_policy.mode == "continuous"


def test_471_streaming_selected_for_interactive(root, local_deployment):
    from northstar_compliance.inference.io import load_workload
    wp7 = load_workload(root / "config/workloads/WP-007.json")
    assert build_selected_policy(wp7, local_deployment).streaming_enabled


def test_472_wp008_planner_rejected(wp8, local_deployment):
    with pytest.raises(ValueError):
        build_selected_policy(wp8, local_deployment)


def test_473_recommendation_has_no_authority(wp2, local_deployment):
    rec = build_recommendation(wp2, local_deployment)
    assert rec.advisory_only and not rec.may_grant_authority and not rec.may_mutate_admission
