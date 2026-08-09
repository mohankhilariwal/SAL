from northstar_compliance.inference.adapters import capability_plan
from northstar_compliance.inference.evaluation import evaluate_candidate
from northstar_compliance.inference.planner import build_recommendation
from northstar_compliance.inference.simulation import simulate_inference_candidate


def test_494_end_to_end_plan_simulate_evaluate(scenario, quality_pass):
    recommendation = build_recommendation(scenario.workload, scenario.deployment, scenario.policy)
    observation = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.82)
    evaluations = evaluate_candidate(observation, scenario.policy, quality_pass)
    assert recommendation.advisory_only
    assert len(evaluations) == 15
    assert all(item.passed for item in evaluations)


def test_495_capability_plan_contains_prohibitions(scenario):
    plan = capability_plan(scenario)
    assert "no automatic DATA-106 mutation" in plan["prohibitions"]
    assert "acceptance_rate" in plan["required_metrics"]


def test_496_scenario_digest_changes_with_cache_state(scenario):
    from dataclasses import replace
    assert scenario.digest() != replace(scenario, cache_state="cold").digest()
