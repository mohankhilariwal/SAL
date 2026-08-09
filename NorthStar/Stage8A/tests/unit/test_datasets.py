import json
from pathlib import Path
import pytest
from northstar_compliance.evaluation.datasets import contamination_report, jaccard_similarity, load_jsonl, parse_case, validate_cases
from northstar_compliance.evaluation.models import DatasetSplit

@pytest.mark.parametrize("split,count", [(DatasetSplit.DEV,10),(DatasetSplit.VALIDATION,8),(DatasetSplit.TEST,6)], ids=["TEST-516","TEST-517","TEST-518"])
def test_split_counts(registry, split, count):
    assert len(registry.load_cases(split)) == count

def test_validation_categories(validation_cases):
    assert {c.category for c in validation_cases} == {"normal","negative","permission","tool_failure","adversarial","temporal","multilingual","conflicting_evidence"}

def test_test_is_sealed(registry):
    assert all(c.sealed for c in registry.load_cases(DatasetSplit.TEST))

def test_non_test_not_sealed(registry):
    assert all(not c.sealed for c in registry.load_cases(DatasetSplit.DEV) + registry.load_cases(DatasetSplit.VALIDATION))

def test_no_cross_split_contamination(registry):
    all_cases = sum((registry.load_cases(s) for s in DatasetSplit), [])
    assert contamination_report(all_cases)["passed"]

def test_jaccard_identity():
    assert jaccard_similarity("one two three four", "one two three four") == 1.0
