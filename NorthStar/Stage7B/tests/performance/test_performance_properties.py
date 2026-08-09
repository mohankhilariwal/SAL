from dataclasses import replace

from northstar_compliance.workload.models import BenchmarkScenario
from northstar_compliance.workload.simulation import CapacitySimulator


def test_447_simulation_is_deterministic(short_profile, service_model):
    s = BenchmarkScenario("p", short_profile, service_model, 250, 99, 10)
    assert CapacitySimulator(s).summarize() == CapacitySimulator(s).summarize()


def test_448_output_throughput_is_positive(short_profile, service_model):
    s = BenchmarkScenario("p", short_profile, service_model, 250, 99, 10)
    assert CapacitySimulator(s).summarize()["output_token_throughput_per_s"] > 0


def test_449_contention_penalty_increases_latency(short_profile, service_model):
    no_penalty = replace(service_model, contention_penalty_per_active_request=0.0)
    high_penalty = replace(service_model, contention_penalty_per_active_request=0.2)
    a = CapacitySimulator(BenchmarkScenario("a", short_profile, no_penalty, 250, 99, 10)).summarize()
    b = CapacitySimulator(BenchmarkScenario("b", short_profile, high_penalty, 250, 99, 10)).summarize()
    assert b["e2e_p95_ms"] >= a["e2e_p95_ms"]
