from dataclasses import replace

from northstar_compliance.inference.evaluation import evaluate_candidate
from northstar_compliance.inference.simulation import simulate_inference_candidate


def test_502_good_candidate_passes(scenario, quality_pass):
    obs = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.85)
    assert all(item.passed for item in evaluate_candidate(obs, scenario.policy, quality_pass))


def test_503_low_acceptance_fails(scenario, quality_pass):
    obs = simulate_inference_candidate(scenario, quality_pass, assumed_acceptance_rate=.10)
    results = {item.evaluation_id: item for item in evaluate_candidate(obs, scenario.policy, quality_pass)}
    assert not results["EVAL-106"].passed
    assert not results["EVAL-115"].passed


def test_504_quality_failure_fails_overall(scenario, quality_pass):
    bad_quality = replace(quality_pass, passed=False, structured_validity_rate=.90)
    obs = simulate_inference_candidate(scenario, bad_quality, assumed_acceptance_rate=.85)
    results = {item.evaluation_id: item for item in evaluate_candidate(obs, scenario.policy, bad_quality)}
    assert not results["EVAL-102"].passed and not results["EVAL-115"].passed
