from dataclasses import replace

from northstar_compliance.workload.metrics import littles_law_concurrency, summarize
from northstar_compliance.workload.models import BenchmarkScenario
from northstar_compliance.workload.simulation import CapacitySimulator, derive_capacity_envelope


def scenario(profile, service, count=100, seed=42):
    return BenchmarkScenario("SC-TEST", profile, service, count, seed, warmup_requests=5)


def test_428_simulator_returns_expected_count(short_profile, service_model):
    assert len(CapacitySimulator(scenario(short_profile, service_model)).run()) == 95


def test_429_simulator_timestamps_are_ordered(short_profile, service_model):
    obs = CapacitySimulator(scenario(short_profile, service_model)).run()
    assert all(x.arrival_s <= x.start_s <= x.end_s for x in obs)


def test_430_e2e_contains_ttft(short_profile, service_model):
    obs = CapacitySimulator(scenario(short_profile, service_model)).run()
    assert all(x.e2e_ms >= x.ttft_ms for x in obs)


def test_431_summary_has_percentiles(short_profile, service_model):
    result = CapacitySimulator(scenario(short_profile, service_model)).summarize()
    assert result["e2e_p99_ms"] >= result["e2e_p95_ms"] >= result["e2e_p50_ms"]


def test_432_higher_arrival_rate_increases_queue(short_profile, service_model):
    low = replace(short_profile, arrival=replace(short_profile.arrival, request_rate_per_s=0.1))
    high = replace(short_profile, arrival=replace(short_profile.arrival, request_rate_per_s=5.0))
    low_q = CapacitySimulator(scenario(low, service_model, 300, 7)).summarize()["queue_p95_ms"]
    high_q = CapacitySimulator(scenario(high, service_model, 300, 7)).summarize()["queue_p95_ms"]
    assert high_q > low_q


def test_433_more_slots_reduce_queue(short_profile, service_model):
    one = replace(service_model, workflow_slots=1)
    many = replace(service_model, workflow_slots=16)
    one_q = CapacitySimulator(scenario(short_profile, one, 200, 9)).summarize()["queue_p95_ms"]
    many_q = CapacitySimulator(scenario(short_profile, many, 200, 9)).summarize()["queue_p95_ms"]
    assert many_q <= one_q


def test_434_long_profile_has_larger_mean_isl(short_profile, long_profile, service_model):
    short = CapacitySimulator(scenario(short_profile, service_model, 100, 4)).summarize()
    long = CapacitySimulator(scenario(long_profile, service_model, 100, 4)).summarize()
    assert long["mean_isl"] > short["mean_isl"]


def test_435_capacity_envelope_is_advisory(short_profile, service_model):
    env = derive_capacity_envelope(scenario(short_profile, service_model, 200, 5), [0.1, 0.2, 0.4])
    assert env.evidence_kind == "simulated" and "planning" in env.recommendation.lower()


def test_436_capacity_rate_is_from_candidates(short_profile, service_model):
    candidates = [0.1, 0.2, 0.4]
    env = derive_capacity_envelope(scenario(short_profile, service_model, 200, 5), candidates)
    assert env.max_sustainable_request_rate_per_s in [0.0, *candidates]


def test_437_littles_law_calculation():
    assert littles_law_concurrency(2.0, 0.5) == 1.0
