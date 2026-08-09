from northstar_compliance.workload.evaluation import evaluate_profile
from northstar_compliance.workload.models import BenchmarkScenario
from northstar_compliance.workload.simulation import CapacitySimulator


def test_443_evaluation_ids_are_complete(short_profile, service_model):
    obs = CapacitySimulator(BenchmarkScenario("e", short_profile, service_model, 100, 1, 5)).run()
    ids = [r.evaluation_id for r in evaluate_profile(short_profile, obs)]
    assert ids == [f"EVAL-{n:03d}" for n in range(89, 101)]


def test_444_evaluation_result_count(short_profile, service_model):
    obs = CapacitySimulator(BenchmarkScenario("e", short_profile, service_model, 100, 1, 5)).run()
    assert len(evaluate_profile(short_profile, obs)) == 12


def test_445_integrity_evaluations_pass(short_profile, service_model):
    obs = CapacitySimulator(BenchmarkScenario("e", short_profile, service_model, 100, 1, 5)).run()
    results = {r.evaluation_id: r.passed for r in evaluate_profile(short_profile, obs)}
    assert all(results[eid] for eid in ["EVAL-089","EVAL-090","EVAL-091","EVAL-097","EVAL-098","EVAL-099","EVAL-100"])


def test_446_slo_results_are_boolean(short_profile, service_model):
    obs = CapacitySimulator(BenchmarkScenario("e", short_profile, service_model, 100, 1, 5)).run()
    assert all(isinstance(r.passed, bool) for r in evaluate_profile(short_profile, obs))
