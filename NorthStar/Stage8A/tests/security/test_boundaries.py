from copy import deepcopy
import pytest
from northstar_compliance.evaluation.graders import DEFAULT_GRADERS
from northstar_compliance.evaluation.harness import EvaluationHarness
from northstar_compliance.evaluation.models import DatasetSplit

@pytest.mark.parametrize("field,value", [
    ("authorization_bypass", True),
    ("policy_override", True),
    ("data_106_mutation", True),
    ("admission_mutation", True),
    ("hidden_chain_of_thought_retained", True),
    ("raw_payload_retained", True),
], ids=[f"TEST-{i}" for i in range(553,559)])
def test_security_mutations_fail(field, value, suite, validation_cases, candidates):
    broken = deepcopy(candidates)
    case = validation_cases[0]
    broken[case.case_id]["trace"][field] = value
    result = EvaluationHarness(suite).run(validation_cases, broken, split=DatasetSplit.VALIDATION)
    assert result.failed_trials >= suite.trial_count
