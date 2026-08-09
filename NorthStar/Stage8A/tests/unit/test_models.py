import pytest
from northstar_compliance.evaluation.models import DatasetSplit, EvaluationCase, EvaluationSuite, GraderFinding, TrialRecord, EvaluationResult

@pytest.mark.parametrize("trial_count", [0, 11], ids=["TEST-508", "TEST-509"])
def test_suite_rejects_invalid_trial_count(trial_count):
    with pytest.raises(ValueError):
        EvaluationSuite("EVAL-SUITE-X", "1", "x", "AGT-001", True, (), (), (), (DatasetSplit.DEV,), trial_count, 1)

@pytest.mark.parametrize("concurrency", [0, 5], ids=["TEST-510", "TEST-511"])
def test_suite_rejects_invalid_concurrency(concurrency):
    with pytest.raises(ValueError):
        EvaluationSuite("EVAL-SUITE-X", "1", "x", "AGT-001", True, (), (), (), (DatasetSplit.DEV,), 1, concurrency)

def test_suite_rejects_authority_effect():
    with pytest.raises(ValueError):
        EvaluationSuite("EVAL-SUITE-X", "1", "x", "AGT-001", True, (), (), (), (DatasetSplit.DEV,), 1, 1, "grant")

def test_suite_rejects_wp008():
    with pytest.raises(ValueError):
        EvaluationSuite("EVAL-SUITE-X", "1", "x", "WP-008", True, (), (), (), (DatasetSplit.DEV,), 1, 1)

def test_finding_score_bounds():
    with pytest.raises(ValueError):
        GraderFinding("G", True, 1.1, "x")

def test_trial_rejects_raw_payload():
    with pytest.raises(ValueError):
        TrialRecord("R", "T", "C", "X", "d", (), True, "E", True)
