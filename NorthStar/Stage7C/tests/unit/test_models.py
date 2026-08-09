from dataclasses import replace
import pytest

from northstar_compliance.inference.models import (
    BatchingPolicy, CachePolicy, DeploymentKind, EvidenceKind, InferenceBenchmarkScenario,
    InferenceDeploymentProfile, InferenceOptimizationPolicy, OptimizationRecommendation,
    QualityParityRecord, SpeculativeDecodingPlan, WorkloadSignal,
)


def test_450_workload_id_guard():
    with pytest.raises(ValueError):
        WorkloadSignal("bad", "x", "active", 1, 1, 1, 1, 1, 0, 0, 0, False, False)


def test_451_workload_ratio_guard():
    with pytest.raises(ValueError):
        WorkloadSignal("WP-999", "x", "active", 1, 1, 1, 1, 1, 1.1, 0, 0, False, False)


def test_452_deployment_digest_stable(local_deployment):
    assert local_deployment.digest() == local_deployment.digest()
    assert len(local_deployment.digest()) == 64


def test_453_raw_payload_rejected(local_deployment):
    with pytest.raises(ValueError):
        replace(local_deployment, raw_payload_capture=True)


def test_454_cache_binding_required():
    with pytest.raises(ValueError):
        CachePolicy(True, "prefix_kv", "scope", False, True, True, True, True, 10, 1)


def test_455_regulatory_answer_cache_rejected():
    with pytest.raises(ValueError):
        CachePolicy(False, "none", "scope", True, True, True, True, True, 0, 0, True)


def test_456_batching_none_zero_tokens():
    with pytest.raises(ValueError):
        BatchingPolicy("none", 10, 1, 0, False, False)


def test_457_draft_model_requires_id():
    with pytest.raises(ValueError):
        SpeculativeDecodingPlan("draft_model", True, None, 4, .5, .1, .05, .2, True, ("WP-002",))


def test_458_wp008_cannot_be_allowlisted():
    with pytest.raises(ValueError):
        SpeculativeDecodingPlan("prompt_lookup", True, None, 4, .5, .1, .05, .2, True, ("WP-008",))


def test_459_semantic_cache_prohibited():
    cache = CachePolicy(False, "none", "scope", True, True, True, True, True, 0, 0)
    batch = BatchingPolicy("none", 0, 1, 0, False, False)
    spec = SpeculativeDecodingPlan("disabled", False, None, 0, .5, .1, .05, .2, True, tuple())
    with pytest.raises(ValueError):
        InferenceOptimizationPolicy("IOP-X", "1", 0, None, False, "none", 1, 1, 1, cache, batch, spec, True)


def test_460_automatic_admission_prohibited():
    cache = CachePolicy(False, "none", "scope", True, True, True, True, True, 0, 0)
    batch = BatchingPolicy("none", 0, 1, 0, False, False)
    spec = SpeculativeDecodingPlan("disabled", False, None, 0, .5, .1, .05, .2, True, tuple())
    with pytest.raises(ValueError):
        InferenceOptimizationPolicy("IOP-X", "1", 0, None, False, "none", 1, 1, 1, cache, batch, spec, automatic_admission_mutation_enabled=True)


def test_461_quality_record_bounds():
    with pytest.raises(ValueError):
        QualityParityRecord("QPR-1", "d", "a", "b", 1.2, 1.0, 0, 0, True, True)


def test_462_inactive_scenario_rejected(wp8, local_deployment):
    cache = CachePolicy(False, "none", "scope", True, True, True, True, True, 0, 0)
    batch = BatchingPolicy("none", 0, 1, 0, False, False)
    spec = SpeculativeDecodingPlan("disabled", False, None, 0, .5, .1, .05, .2, True, tuple())
    policy = InferenceOptimizationPolicy("IOP-X", "1", 0, 10, False, "none", 1, 1, 1, cache, batch, spec)
    with pytest.raises(ValueError):
        InferenceBenchmarkScenario("IBS-X", wp8, local_deployment, policy, EvidenceKind.SIMULATED, 1, 1, "cold", "q")


def test_463_recommendation_advisory_guard():
    with pytest.raises(ValueError):
        OptimizationRecommendation("IOR-X", "WP-001", "INF-001", tuple(), "IOP-X", False, False, False)
