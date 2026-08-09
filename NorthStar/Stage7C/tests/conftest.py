from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pytest

from northstar_compliance.inference.io import load_deployment, load_workload
from northstar_compliance.inference.models import EvidenceKind, InferenceBenchmarkScenario, QualityParityRecord
from northstar_compliance.inference.planner import build_selected_policy


@pytest.fixture
def root() -> Path:
    return ROOT


@pytest.fixture
def wp2(root: Path):
    return load_workload(root / "config/workloads/WP-002.json")


@pytest.fixture
def wp5(root: Path):
    return load_workload(root / "config/workloads/WP-005.json")


@pytest.fixture
def wp8(root: Path):
    return load_workload(root / "config/workloads/WP-008.json")


@pytest.fixture
def local_deployment(root: Path):
    return load_deployment(root / "config/inference/INF-003.json")


@pytest.fixture
def managed_deployment(root: Path):
    return load_deployment(root / "config/inference/INF-001.json")


@pytest.fixture
def self_hosted_deployment(root: Path):
    return load_deployment(root / "config/inference/INF-002.json")


@pytest.fixture
def quality_pass() -> QualityParityRecord:
    return QualityParityRecord(
        record_id="QPR-001",
        dataset_id="DATASET-S07C-QUALITY-001",
        baseline_digest="a" * 64,
        candidate_digest="b" * 64,
        exact_match_rate=1.0,
        structured_validity_rate=1.0,
        groundedness_delta=0.0,
        task_success_delta=0.0,
        lossless_distribution_verified=True,
        passed=True,
        notes=("synthetic local parity record",),
    )


@pytest.fixture
def scenario(wp2, local_deployment):
    policy = build_selected_policy(wp2, local_deployment)
    return InferenceBenchmarkScenario(
        scenario_id="IBS-001",
        workload=wp2,
        deployment=local_deployment,
        policy=policy,
        evidence_kind=EvidenceKind.SIMULATED,
        request_count=100,
        seed=42,
        cache_state="representative",
        quality_dataset_id="DATASET-S07C-QUALITY-001",
    )
