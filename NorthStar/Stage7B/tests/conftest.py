from pathlib import Path
import pytest

from northstar_compliance.workload.io import load_profile, load_service_model


@pytest.fixture(scope="session")
def root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def short_profile(root):
    return load_profile(root / "config/workloads/WP-001.json")


@pytest.fixture(scope="session")
def long_profile(root):
    return load_profile(root / "config/workloads/WP-002.json")


@pytest.fixture(scope="session")
def inactive_profile(root):
    return load_profile(root / "config/workloads/WP-008.json")


@pytest.fixture(scope="session")
def service_model(root):
    return load_service_model(root / "config/workloads/service-model-local.json")
