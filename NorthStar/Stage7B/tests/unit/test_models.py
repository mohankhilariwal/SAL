import pytest

from northstar_compliance.workload.models import (
    ArrivalKind,
    ArrivalPattern,
    BenchmarkObservation,
    BenchmarkScenario,
    CapacityEnvelope,
    DistributionBucket,
    ServiceDemandModel,
    SLOHypothesis,
    WorkloadProfile,
)


def test_408_distribution_bucket_accepts_valid_range():
    assert DistributionBucket("b", 1, 1, 2, 3, 1, 2, 3).isl_mode == 2


def test_409_distribution_bucket_rejects_zero_weight():
    with pytest.raises(ValueError):
        DistributionBucket("b", 0, 1, 2, 3, 1, 2, 3)


def test_410_distribution_bucket_rejects_bad_mode():
    with pytest.raises(ValueError):
        DistributionBucket("b", 1, 5, 2, 3, 1, 2, 3)


def test_411_arrival_poisson_requires_rate():
    with pytest.raises(ValueError):
        ArrivalPattern(ArrivalKind.POISSON)


def test_412_arrival_closed_loop_requires_concurrency():
    with pytest.raises(ValueError):
        ArrivalPattern(ArrivalKind.CLOSED_LOOP)


def test_413_slo_rejects_invalid_success_rate():
    with pytest.raises(ValueError):
        SLOHypothesis(1, 1, 1, 1, 1.1)


def test_414_profile_digest_is_stable(short_profile):
    assert short_profile.digest == short_profile.digest and len(short_profile.digest) == 64


def test_415_profile_rejects_payload_capture(short_profile):
    with pytest.raises(ValueError):
        WorkloadProfile(
            profile_id="WP-999", name="x", version="1", tokenizer_id="t", status="bootstrap_assumption",
            description="x", buckets=short_profile.buckets, arrival=short_profile.arrival, slo=short_profile.slo,
            capture_payloads=True,
        )


def test_416_service_model_rejects_nonpositive_rate():
    with pytest.raises(ValueError):
        ServiceDemandModel("m", 0, 1, 1, 1, 1, 1)


def test_417_inactive_profile_cannot_form_scenario(inactive_profile, service_model):
    with pytest.raises(ValueError):
        BenchmarkScenario("x", inactive_profile, service_model, 1, 1)


def test_418_observation_rejects_end_before_start():
    with pytest.raises(ValueError):
        BenchmarkObservation("r", "p", 0, 2, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, True)


def test_419_capacity_envelope_validates_attainment():
    with pytest.raises(ValueError):
        CapacityEnvelope("p", 1, 1, 1, 1, 1, 1, 1, 1.2, "simulated", "x")
