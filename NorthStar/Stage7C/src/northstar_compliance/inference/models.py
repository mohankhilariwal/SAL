from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
import hashlib
import json
from typing import Any


class DeploymentKind(StrEnum):
    MANAGED_API = "managed_api"
    SELF_HOSTED = "self_hosted"
    LOCAL_SIMULATED = "local_simulated"


class EvidenceKind(StrEnum):
    SIMULATED = "simulated"
    SYNTHETIC_ENDPOINT = "synthetic_endpoint"
    TRACE_REPLAY = "trace_replay"
    PRODUCTION = "production"


class OptimizationTechnique(StrEnum):
    CONTEXT_REDUCTION = "context_reduction"
    OUTPUT_LENGTH_CONTROL = "output_length_control"
    STREAMING = "streaming"
    PREFIX_CACHING = "prefix_caching"
    EXACT_RESPONSE_CACHING = "exact_response_caching"
    SEMANTIC_RESPONSE_CACHING = "semantic_response_caching"
    DYNAMIC_BATCHING = "dynamic_batching"
    CONTINUOUS_BATCHING = "continuous_batching"
    CHUNKED_PREFILL = "chunked_prefill"
    QUANTIZATION = "quantization"
    TENSOR_PARALLELISM = "tensor_parallelism"
    PIPELINE_PARALLELISM = "pipeline_parallelism"
    DATA_PARALLELISM = "data_parallelism"
    SPECULATIVE_PROMPT_LOOKUP = "speculative_prompt_lookup"
    SPECULATIVE_DRAFT_MODEL = "speculative_draft_model"
    SELF_SPECULATIVE = "self_speculative"
    MULTI_TOKEN_PREDICTION = "multi_token_prediction"
    MODEL_ROUTING = "model_routing"


@dataclass(frozen=True, slots=True)
class WorkloadSignal:
    profile_id: str
    name: str
    status: str
    median_isl_tokens: int
    median_osl_tokens: int
    p95_isl_tokens: int
    p95_osl_tokens: int
    expected_concurrency: int
    repeated_prefix_ratio: float
    input_output_overlap: float
    external_latency_fraction: float
    interactive: bool
    batch: bool
    context_growth: bool = False

    def __post_init__(self) -> None:
        if not self.profile_id.startswith("WP-"):
            raise ValueError("profile_id must use WP-* format")
        if self.status not in {"active", "inactive_future"}:
            raise ValueError("unsupported workload status")
        for value in (
            self.median_isl_tokens,
            self.median_osl_tokens,
            self.p95_isl_tokens,
            self.p95_osl_tokens,
            self.expected_concurrency,
        ):
            if value < 0:
                raise ValueError("token and concurrency values must be non-negative")
        for value in (
            self.repeated_prefix_ratio,
            self.input_output_overlap,
            self.external_latency_fraction,
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError("ratio values must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class InferenceDeploymentProfile:
    deployment_id: str
    name: str
    version: str
    kind: DeploymentKind
    provider_or_runtime: str
    model_id: str
    tokenizer_id: str
    server_version: str
    hardware: str
    region_or_location: str
    data_residency: str
    supports_streaming: bool
    supports_prefix_cache: bool
    supports_continuous_batching: bool
    supports_chunked_prefill: bool
    supports_quantization: bool
    supports_speculative_decoding: bool
    supports_parallelism: bool
    raw_payload_capture: bool = False

    def __post_init__(self) -> None:
        if not self.deployment_id.startswith("INF-"):
            raise ValueError("deployment_id must use INF-* format")
        if self.raw_payload_capture:
            raise ValueError("raw payload capture is prohibited in the local reference")
        for value in (
            self.name,
            self.version,
            self.provider_or_runtime,
            self.model_id,
            self.tokenizer_id,
            self.server_version,
            self.hardware,
            self.region_or_location,
            self.data_residency,
        ):
            if not value.strip():
                raise ValueError("deployment metadata must be populated")

    def digest(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class CachePolicy:
    enabled: bool
    cache_type: str
    scope: str
    tenant_isolated: bool
    model_bound: bool
    tokenizer_bound: bool
    prompt_version_bound: bool
    authorization_scope_bound: bool
    ttl_seconds: int
    minimum_prefix_tokens: int
    allow_regulatory_answer_cache: bool = False

    def __post_init__(self) -> None:
        allowed = {"none", "provider_prompt", "prefix_kv", "exact_response"}
        if self.cache_type not in allowed:
            raise ValueError("unsupported cache type")
        if self.enabled and self.cache_type == "none":
            raise ValueError("enabled cache requires a cache type")
        if self.ttl_seconds < 0 or self.minimum_prefix_tokens < 0:
            raise ValueError("cache limits must be non-negative")
        if self.enabled and not all(
            (
                self.tenant_isolated,
                self.model_bound,
                self.tokenizer_bound,
                self.prompt_version_bound,
                self.authorization_scope_bound,
            )
        ):
            raise ValueError("enabled caches require all NorthStar binding controls")
        if self.allow_regulatory_answer_cache:
            raise ValueError("regulatory assessment answers cannot be cached as authoritative results")


@dataclass(frozen=True, slots=True)
class BatchingPolicy:
    mode: str
    max_batch_tokens: int
    max_concurrent_requests: int
    max_wait_ms: float
    chunked_prefill: bool
    priority_aware: bool

    def __post_init__(self) -> None:
        if self.mode not in {"none", "dynamic", "continuous", "offline_batch"}:
            raise ValueError("unsupported batching mode")
        if self.max_batch_tokens < 0 or self.max_concurrent_requests < 1 or self.max_wait_ms < 0:
            raise ValueError("invalid batching limits")
        if self.mode == "none" and self.max_batch_tokens != 0:
            raise ValueError("no batching must have zero max_batch_tokens")


@dataclass(frozen=True, slots=True)
class SpeculativeDecodingPlan:
    method: str
    enabled: bool
    draft_model_id: str | None
    num_speculative_tokens: int
    minimum_acceptance_rate: float
    minimum_decode_improvement: float
    minimum_e2e_improvement: float
    maximum_memory_overhead_ratio: float
    require_lossless_distribution: bool
    profile_allowlist: tuple[str, ...]

    def __post_init__(self) -> None:
        allowed = {
            "disabled",
            "prompt_lookup",
            "draft_model",
            "self_speculative",
            "mtp",
            "medusa_style",
        }
        if self.method not in allowed:
            raise ValueError("unsupported speculative method")
        if self.enabled and self.method == "disabled":
            raise ValueError("enabled plan requires a method")
        if not self.enabled and self.method != "disabled":
            raise ValueError("disabled plan must use disabled method")
        if self.num_speculative_tokens < 0:
            raise ValueError("num_speculative_tokens must be non-negative")
        for value in (
            self.minimum_acceptance_rate,
            self.minimum_decode_improvement,
            self.minimum_e2e_improvement,
            self.maximum_memory_overhead_ratio,
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError("speculative gate values must be in [0, 1]")
        if self.method == "draft_model" and self.enabled and not self.draft_model_id:
            raise ValueError("draft-model speculation requires draft_model_id")
        if "WP-008" in self.profile_allowlist:
            raise ValueError("inactive future profile cannot be allowlisted")


@dataclass(frozen=True, slots=True)
class InferenceOptimizationPolicy:
    policy_id: str
    version: str
    context_reduction_ratio: float
    output_token_cap: int | None
    streaming_enabled: bool
    quantization: str
    tensor_parallel_size: int
    pipeline_parallel_size: int
    data_parallel_size: int
    cache_policy: CachePolicy
    batching_policy: BatchingPolicy
    speculative_plan: SpeculativeDecodingPlan
    semantic_response_cache_enabled: bool = False
    automatic_model_routing_enabled: bool = False
    automatic_admission_mutation_enabled: bool = False

    def __post_init__(self) -> None:
        if not self.policy_id.startswith("IOP-"):
            raise ValueError("policy_id must use IOP-* format")
        if not 0.0 <= self.context_reduction_ratio <= 0.8:
            raise ValueError("context reduction ratio must be in [0, 0.8]")
        if self.output_token_cap is not None and self.output_token_cap < 1:
            raise ValueError("output token cap must be positive")
        if self.quantization not in {"none", "fp8", "int8", "int4", "provider_managed"}:
            raise ValueError("unsupported quantization mode")
        if min(self.tensor_parallel_size, self.pipeline_parallel_size, self.data_parallel_size) < 1:
            raise ValueError("parallelism sizes must be positive")
        if self.semantic_response_cache_enabled:
            raise ValueError("semantic response caching is prohibited for regulatory conclusions")
        if self.automatic_model_routing_enabled:
            raise ValueError("automatic model routing is deferred to a later explicit decision")
        if self.automatic_admission_mutation_enabled:
            raise ValueError("optimization policy cannot mutate DATA-106 admission automatically")

    def digest(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class InferenceBenchmarkScenario:
    scenario_id: str
    workload: WorkloadSignal
    deployment: InferenceDeploymentProfile
    policy: InferenceOptimizationPolicy
    evidence_kind: EvidenceKind
    request_count: int
    seed: int
    cache_state: str
    quality_dataset_id: str

    def __post_init__(self) -> None:
        if not self.scenario_id.startswith("IBS-"):
            raise ValueError("scenario_id must use IBS-* format")
        if self.workload.status != "active":
            raise ValueError("inactive workload profiles cannot execute")
        if self.request_count < 1:
            raise ValueError("request_count must be positive")
        if self.cache_state not in {"cold", "warm", "representative"}:
            raise ValueError("cache_state must be declared")
        if not self.quality_dataset_id:
            raise ValueError("quality dataset is mandatory")
        if self.policy.speculative_plan.enabled and self.workload.profile_id not in self.policy.speculative_plan.profile_allowlist:
            raise ValueError("workload is not allowlisted for speculative decoding")

    def digest(self) -> str:
        body: dict[str, Any] = {
            "scenario_id": self.scenario_id,
            "workload": asdict(self.workload),
            "deployment_digest": self.deployment.digest(),
            "policy_digest": self.policy.digest(),
            "evidence_kind": str(self.evidence_kind),
            "request_count": self.request_count,
            "seed": self.seed,
            "cache_state": self.cache_state,
            "quality_dataset_id": self.quality_dataset_id,
        }
        payload = json.dumps(body, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class QualityParityRecord:
    record_id: str
    dataset_id: str
    baseline_digest: str
    candidate_digest: str
    exact_match_rate: float
    structured_validity_rate: float
    groundedness_delta: float
    task_success_delta: float
    lossless_distribution_verified: bool
    passed: bool
    notes: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.record_id.startswith("QPR-"):
            raise ValueError("record_id must use QPR-* format")
        for value in (self.exact_match_rate, self.structured_validity_rate):
            if not 0.0 <= value <= 1.0:
                raise ValueError("rates must be in [0, 1]")
        for value in (self.groundedness_delta, self.task_success_delta):
            if not -1.0 <= value <= 1.0:
                raise ValueError("deltas must be in [-1, 1]")


@dataclass(frozen=True, slots=True)
class InferenceBenchmarkObservation:
    observation_id: str
    scenario_digest: str
    profile_id: str
    evidence_kind: EvidenceKind
    baseline_ttft_ms: float
    candidate_ttft_ms: float
    baseline_itl_ms: float
    candidate_itl_ms: float
    baseline_e2e_ms: float
    candidate_e2e_ms: float
    baseline_output_tps: float
    candidate_output_tps: float
    acceptance_rate: float | None
    mean_accepted_tokens: float | None
    kv_cache_mb: float
    candidate_memory_overhead_ratio: float
    cache_hit_rate: float
    quality_parity_record_id: str
    success: bool
    raw_payload_captured: bool = False

    def __post_init__(self) -> None:
        if not self.observation_id.startswith("IBO-"):
            raise ValueError("observation_id must use IBO-* format")
        values = (
            self.baseline_ttft_ms,
            self.candidate_ttft_ms,
            self.baseline_itl_ms,
            self.candidate_itl_ms,
            self.baseline_e2e_ms,
            self.candidate_e2e_ms,
            self.baseline_output_tps,
            self.candidate_output_tps,
            self.kv_cache_mb,
            self.candidate_memory_overhead_ratio,
            self.cache_hit_rate,
        )
        if any(value < 0 for value in values):
            raise ValueError("metrics must be non-negative")
        if self.acceptance_rate is not None and not 0.0 <= self.acceptance_rate <= 1.0:
            raise ValueError("acceptance_rate must be in [0, 1]")
        if self.raw_payload_captured:
            raise ValueError("raw payload capture is prohibited")

    @property
    def decode_improvement(self) -> float:
        if self.baseline_itl_ms == 0:
            return 0.0
        return (self.baseline_itl_ms - self.candidate_itl_ms) / self.baseline_itl_ms

    @property
    def e2e_improvement(self) -> float:
        if self.baseline_e2e_ms == 0:
            return 0.0
        return (self.baseline_e2e_ms - self.candidate_e2e_ms) / self.baseline_e2e_ms


@dataclass(frozen=True, slots=True)
class TechniqueAssessment:
    technique: OptimizationTechnique
    suitability_score: int
    decision: str
    rationale: str
    required_gates: tuple[str, ...]

    def __post_init__(self) -> None:
        if not 0 <= self.suitability_score <= 5:
            raise ValueError("suitability_score must be 0..5")
        if self.decision not in {"select", "benchmark", "defer", "prohibit", "not_applicable"}:
            raise ValueError("unsupported decision")


@dataclass(frozen=True, slots=True)
class OptimizationRecommendation:
    recommendation_id: str
    profile_id: str
    deployment_id: str
    assessments: tuple[TechniqueAssessment, ...]
    selected_policy_id: str
    advisory_only: bool
    may_mutate_admission: bool
    may_grant_authority: bool

    def __post_init__(self) -> None:
        if not self.recommendation_id.startswith("IOR-"):
            raise ValueError("recommendation_id must use IOR-* format")
        if not self.advisory_only:
            raise ValueError("optimization recommendations must remain advisory")
        if self.may_mutate_admission or self.may_grant_authority:
            raise ValueError("recommendation cannot mutate admission or grant authority")
