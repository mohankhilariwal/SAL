import math
import pytest

from northstar_compliance.inference.speculative import (
    MarkovModel, baseline_sample, empirical_first_token_distribution, expected_acceptance_probability,
    kl_divergence, normalize, speculative_sample, total_variation_distance,
    verify_empirical_distribution_parity,
)


def models():
    target = MarkovModel(
        start={"A": .55, "B": .30, "C": .15},
        transitions={
            "A": {"A": .10, "B": .65, "C": .25},
            "B": {"A": .50, "B": .20, "C": .30},
            "C": {"A": .35, "B": .35, "C": .30},
        },
    )
    close = MarkovModel(
        start={"A": .52, "B": .32, "C": .16},
        transitions={
            "A": {"A": .12, "B": .62, "C": .26},
            "B": {"A": .46, "B": .24, "C": .30},
            "C": {"A": .33, "B": .37, "C": .30},
        },
    )
    poor = MarkovModel(
        start={"A": .15, "B": .30, "C": .55},
        transitions={
            "A": {"A": .70, "B": .20, "C": .10},
            "B": {"A": .10, "B": .20, "C": .70},
            "C": {"A": .10, "B": .75, "C": .15},
        },
    )
    return target, close, poor


def test_474_normalize():
    assert normalize({"A": 2, "B": 2}) == {"A": .5, "B": .5}


def test_475_negative_probability_rejected():
    with pytest.raises(ValueError):
        normalize({"A": -1, "B": 2})


def test_476_baseline_is_deterministic():
    target, _, _ = models()
    assert baseline_sample(target, max_tokens=10, seed=3) == baseline_sample(target, max_tokens=10, seed=3)


def test_477_speculative_is_deterministic():
    target, close, _ = models()
    assert speculative_sample(target, close, max_tokens=20, speculative_tokens=4, seed=7) == speculative_sample(target, close, max_tokens=20, speculative_tokens=4, seed=7)


def test_478_speculative_length():
    target, close, _ = models()
    trace = speculative_sample(target, close, max_tokens=37, speculative_tokens=4, seed=8)
    assert len(trace.tokens) == 37


def test_479_close_draft_high_acceptance():
    target, close, _ = models()
    trace = speculative_sample(target, close, max_tokens=500, speculative_tokens=4, seed=9)
    assert trace.acceptance_rate > .70


def test_480_poor_draft_lower_acceptance():
    target, close, poor = models()
    close_trace = speculative_sample(target, close, max_tokens=500, speculative_tokens=4, seed=10)
    poor_trace = speculative_sample(target, poor, max_tokens=500, speculative_tokens=4, seed=10)
    assert poor_trace.acceptance_rate < close_trace.acceptance_rate


def test_481_expected_acceptance_matches_overlap():
    assert expected_acceptance_probability({"A": .6, "B": .4}, {"A": .5, "B": .5}) == pytest.approx(.9)


def test_482_kl_zero_for_identical():
    assert kl_divergence({"A": .4, "B": .6}, {"A": .4, "B": .6}) == pytest.approx(0)


def test_483_kl_infinite_if_missing_mass():
    assert math.isinf(kl_divergence({"A": .4, "B": .6}, {"A": 1.0}))


def test_484_empirical_parity():
    target, close, _ = models()
    passed, distance = verify_empirical_distribution_parity(target, close, trials=10000, tolerance=.04, seed=12)
    assert passed, distance


def test_485_total_variation_bounds():
    distance = total_variation_distance({"A": 1}, {"B": 1})
    assert distance == pytest.approx(1.0)
