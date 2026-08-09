from pathlib import Path
import pytest
from northstar_compliance.evaluation.models import DatasetSplit
from northstar_compliance.evaluation.registry import EvaluationRegistry

@pytest.fixture(scope="session")
def root():
    return Path(__file__).resolve().parents[1]

@pytest.fixture(scope="session")
def registry(root):
    return EvaluationRegistry(root)

@pytest.fixture(scope="session")
def suite(registry):
    return registry.load_suite()

@pytest.fixture(scope="session")
def validation_cases(registry):
    return registry.load_cases(DatasetSplit.VALIDATION)

@pytest.fixture(scope="session")
def candidates(registry):
    return registry.load_candidates()
