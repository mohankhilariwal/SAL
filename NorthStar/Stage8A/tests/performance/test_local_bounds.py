from time import perf_counter
from northstar_compliance.evaluation.harness import EvaluationHarness
from northstar_compliance.evaluation.models import DatasetSplit

def test_local_validation_completes_quickly(suite, validation_cases, candidates):
    start = perf_counter()
    EvaluationHarness(suite).run(validation_cases, candidates, split=DatasetSplit.VALIDATION)
    assert perf_counter() - start < 2.0

def test_bounded_trial_count(suite, validation_cases, candidates):
    result = EvaluationHarness(suite).run(validation_cases, candidates, split=DatasetSplit.VALIDATION)
    assert result.trial_count == len(validation_cases) * suite.trial_count
