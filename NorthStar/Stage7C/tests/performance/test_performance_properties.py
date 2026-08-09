from dataclasses import replace

from northstar_compliance.inference.planner import build_selected_policy, disable_speculation
from northstar_compliance.inference.simulation import simulate_inference_candidate


def test_505_context_reduction_lowers_ttft(scenario, quality_pass):
    optimized = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.8)
    no_reduction_policy = replace(scenario.policy, context_reduction_ratio=0.0)
    baseline_candidate = simulate_inference_candidate(replace(scenario, policy=no_reduction_policy), quality_pass, assumed_acceptance_rate=.8)
    assert optimized.candidate_ttft_ms < baseline_candidate.candidate_ttft_ms


def test_506_speculation_can_hurt_at_low_acceptance(scenario, quality_pass):
    with_spec = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.05)
    no_spec = simulate_inference_candidate(replace(scenario, policy=disable_speculation(scenario.policy)), quality_pass)
    assert with_spec.candidate_itl_ms > no_spec.candidate_itl_ms


def test_507_tool_heavy_policy_does_not_speculate(wp5, local_deployment):
    assert not build_selected_policy(wp5, local_deployment).speculative_plan.enabled
