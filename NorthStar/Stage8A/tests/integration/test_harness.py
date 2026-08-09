from copy import deepcopy
import pytest
from northstar_compliance.evaluation.harness import EvaluationHarness
from northstar_compliance.evaluation.models import DatasetSplit

@pytest.mark.parametrize("run", range(3), ids=["TEST-545","TEST-546","TEST-547"])
def test_validation_run_is_deterministic(run, suite, validation_cases, candidates):
    result = EvaluationHarness(suite).run(validation_cases, candidates, split=DatasetSplit.VALIDATION, run_id=f"RUN-{run}")
    assert result.pass_rate == 1.0 and result.required_gate_passed

def test_test_split_blocked_by_default(registry, suite, candidates):
    with pytest.raises(PermissionError):
        EvaluationHarness(suite).run(registry.load_cases(DatasetSplit.TEST), candidates, split=DatasetSplit.TEST)

def test_missing_candidate_fails(suite, validation_cases):
    result = EvaluationHarness(suite).run(validation_cases, {}, split=DatasetSplit.VALIDATION)
    assert result.failed_trials == result.trial_count

def test_mutated_candidate_fails(suite, validation_cases, candidates):
    broken = deepcopy(candidates)
    broken[validation_cases[0].case_id]["status"] = "approved"
    result = EvaluationHarness(suite).run(validation_cases, broken, split=DatasetSplit.VALIDATION)
    assert result.failed_trials == suite.trial_count
