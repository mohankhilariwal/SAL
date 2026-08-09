from collections import Counter
import pytest

from northstar_compliance.workload.models import ArrivalKind, ArrivalPattern
from northstar_compliance.workload.sampling import WorkloadSampler


def test_420_sampling_is_seed_reproducible(short_profile):
    a = WorkloadSampler(short_profile, 10).sample(20)
    b = WorkloadSampler(short_profile, 10).sample(20)
    assert a == b


def test_421_sampling_changes_with_seed(short_profile):
    assert WorkloadSampler(short_profile, 10).sample(10) != WorkloadSampler(short_profile, 11).sample(10)


def test_422_sample_lengths_stay_in_profile_bounds(short_profile):
    samples = WorkloadSampler(short_profile, 1).sample(100)
    assert min(x.isl_tokens for x in samples) >= 256
    assert max(x.osl_tokens for x in samples) <= 1400


def test_423_request_ids_are_unique(short_profile):
    samples = WorkloadSampler(short_profile, 1).sample(50)
    assert len({x.request_id for x in samples}) == 50


def test_424_poisson_arrivals_are_nondecreasing(short_profile):
    arrivals = [x.arrival_s for x in WorkloadSampler(short_profile, 1).sample(50)]
    assert arrivals == sorted(arrivals)


def test_425_bucket_mixture_reaches_multiple_buckets(short_profile):
    buckets = Counter(x.bucket_id for x in WorkloadSampler(short_profile, 1).sample(500))
    assert len(buckets) >= 2


def test_426_context_growth_increases_possible_isl(short_profile):
    samples = WorkloadSampler(short_profile, 8).sample(300)
    assert any(x.turns > 1 and x.isl_tokens > 1200 for x in samples)


def test_427_sampler_rejects_zero_count(short_profile):
    with pytest.raises(ValueError):
        WorkloadSampler(short_profile, 1).sample(0)
