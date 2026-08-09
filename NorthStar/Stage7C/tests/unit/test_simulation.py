from dataclasses import replace
import pytest

from northstar_compliance.inference.models import InferenceBenchmarkScenario
from northstar_compliance.inference.planner import disable_speculation
from northstar_compliance.inference.simulation import ServiceRates, expected_accepted_draft_tokens, simulate_inference_candidate


def test_486_expected_accepted_monotonic():
    assert expected_accepted_draft_tokens(.8, 4) > expected_accepted_draft_tokens(.5, 4)


def test_487_simulation_metrics_positive(scenario, quality_pass):
    obs = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.75)
    assert obs.candidate_ttft_ms > 0 and obs.candidate_e2e_ms > obs.candidate_ttft_ms


def test_488_cache_hit_reduces_ttft(scenario, quality_pass):
    cold = simulate_inference_candidate(replace(scenario, cache_state="cold"), quality_pass, assumed_acceptance_rate=.75)
    warm = simulate_inference_candidate(replace(scenario, cache_state="warm"), quality_pass, assumed_acceptance_rate=.75)
    assert warm.candidate_ttft_ms < cold.candidate_ttft_ms


def test_489_high_acceptance_improves_decode(scenario, quality_pass):
    high = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.9)
    low = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.2)
    assert high.candidate_itl_ms < low.candidate_itl_ms


def test_490_external_latency_limits_e2e_gain(scenario, quality_pass):
    obs = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.9)
    assert obs.e2e_improvement < obs.decode_improvement


def test_491_speculation_memory_overhead(scenario, quality_pass):
    obs = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.8)
    assert obs.candidate_memory_overhead_ratio > 0


def test_492_disabled_speculation_has_no_acceptance(scenario, quality_pass):
    no_spec = replace(scenario, policy=disable_speculation(scenario.policy))
    obs = simulate_inference_candidate(no_spec, quality_pass)
    assert obs.acceptance_rate is None and obs.candidate_memory_overhead_ratio == 0


def test_493_invalid_service_rates():
    with pytest.raises(ValueError):
        ServiceRates(decode_tokens_per_second=0)
