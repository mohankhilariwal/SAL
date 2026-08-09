from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from hashlib import sha256
import json
from typing import Any, Iterable


class ArrivalKind(StrEnum):
    CLOSED_LOOP = "closed_loop"
    CONSTANT = "constant"
    POISSON = "poisson"
    BURST = "burst"
    BATCH = "batch"


@dataclass(frozen=True, slots=True)
class DistributionBucket:
    """One weighted, tokenizer-specific workload bucket.

    Length values are request-level token counts. They are assumptions until
    replaced by measured traces. A bucket may represent one model call or an
    aggregate workflow call depending on the profile's documented semantics.
    """

    bucket_id: str
    weight: float
    isl_min: int
    isl_mode: int
    isl_max: int
    osl_min: int
    osl_mode: int
    osl_max: int
    model_calls_min: int = 1
    model_calls_mode: int = 1
    model_calls_max: int = 1
    tool_calls_min: int = 0
    tool_calls_mode: int = 0
    tool_calls_max: int = 0
    retrieval_calls_min: int = 0
    retrieval_calls_mode: int = 0
    retrieval_calls_max: int = 0

    def __post_init__(self) -> None:
        if not self.bucket_id.strip():
            raise ValueError("bucket_id is required")
        if self.weight <= 0:
            raise ValueError("weight must be positive")
        self._validate_triangular("isl", self.isl_min, self.isl_mode, self.isl_max, minimum=1)
        self._validate_triangular("osl", self.osl_min, self.osl_mode, self.osl_max, minimum=1)
        self._validate_triangular(
            "model_calls", self.model_calls_min, self.model_calls_mode, self.model_calls_max, minimum=1
        )
        self._validate_triangular(
            "tool_calls", self.tool_calls_min, self.tool_calls_mode, self.tool_calls_max, minimum=0
        )
        self._validate_triangular(
            "retrieval_calls",
            self.retrieval_calls_min,
            self.retrieval_calls_mode,
            self.retrieval_calls_max,
            minimum=0,
        )

    @staticmethod
    def _validate_triangular(name: str, low: int, mode: int, high: int, *, minimum: int) -> None:
        if low < minimum or not low <= mode <= high:
            raise ValueError(f"invalid {name} triangular range: {low}, {mode}, {high}")


@dataclass(frozen=True, slots=True)
class ArrivalPattern:
    kind: ArrivalKind
    request_rate_per_s: float | None = None
    max_concurrency: int | None = None
    burst_multiplier: float = 1.0
    burst_duration_s: float = 0.0
    quiet_duration_s: float = 0.0

    def __post_init__(self) -> None:
        if self.request_rate_per_s is not None and self.request_rate_per_s <= 0:
            raise ValueError("request_rate_per_s must be positive")
        if self.max_concurrency is not None and self.max_concurrency <= 0:
            raise ValueError("max_concurrency must be positive")
        if self.kind in {ArrivalKind.CONSTANT, ArrivalKind.POISSON, ArrivalKind.BURST}:
            if self.request_rate_per_s is None:
                raise ValueError(f"{self.kind} requires request_rate_per_s")
        if self.kind is ArrivalKind.CLOSED_LOOP and self.max_concurrency is None:
            raise ValueError("closed_loop requires max_concurrency")
        if self.kind is ArrivalKind.BURST:
            if self.burst_multiplier <= 1:
                raise ValueError("burst_multiplier must be > 1")
            if self.burst_duration_s <= 0 or self.quiet_duration_s <= 0:
                raise ValueError("burst timing must be positive")


@dataclass(frozen=True, slots=True)
class SLOHypothesis:
    """A profile-specific hypothesis, not a production commitment."""

    ttft_p95_ms: float | None
    itl_p95_ms: float | None
    e2e_p95_ms: float
    queue_p95_ms: float
    success_rate_min: float = 0.99
    rationale: str = "bootstrap hypothesis pending measured evidence"

    def __post_init__(self) -> None:
        for name in ("ttft_p95_ms", "itl_p95_ms", "e2e_p95_ms", "queue_p95_ms"):
            value = getattr(self, name)
            if value is not None and value <= 0:
                raise ValueError(f"{name} must be positive")
        if not 0 < self.success_rate_min <= 1:
            raise ValueError("success_rate_min must be in (0, 1]")


@dataclass(frozen=True, slots=True)
class WorkloadProfile:
    profile_id: str
    name: str
    version: str
    tokenizer_id: str
    status: str
    description: str
    buckets: tuple[DistributionBucket, ...]
    arrival: ArrivalPattern
    slo: SLOHypothesis
    context_growth_per_turn: float = 0.0
    turns_min: int = 1
    turns_mode: int = 1
    turns_max: int = 1
    capture_payloads: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.profile_id or not self.name or not self.version or not self.tokenizer_id:
            raise ValueError("profile identity fields are required")
        if self.status not in {"bootstrap_assumption", "measured", "inactive_future"}:
            raise ValueError("invalid status")
        if not self.buckets:
            raise ValueError("at least one bucket is required")
        if self.turns_min < 1 or not self.turns_min <= self.turns_mode <= self.turns_max:
            raise ValueError("invalid turn range")
        if self.context_growth_per_turn < 0:
            raise ValueError("context_growth_per_turn cannot be negative")
        if self.capture_payloads:
            raise ValueError("Stage 7B profiles must not capture raw prompts or responses")

    @property
    def total_weight(self) -> float:
        return sum(bucket.weight for bucket in self.buckets)

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "name": self.name,
            "version": self.version,
            "tokenizer_id": self.tokenizer_id,
            "status": self.status,
            "description": self.description,
            "buckets": [asdict(bucket) for bucket in self.buckets],
            "arrival": {**asdict(self.arrival), "kind": self.arrival.kind.value},
            "slo": asdict(self.slo),
            "context_growth_per_turn": self.context_growth_per_turn,
            "turns_min": self.turns_min,
            "turns_mode": self.turns_mode,
            "turns_max": self.turns_max,
            "capture_payloads": self.capture_payloads,
            "metadata": self.metadata,
        }

    @property
    def digest(self) -> str:
        payload = json.dumps(self.canonical_dict(), sort_keys=True, separators=(",", ":"), default=str)
        return sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class ServiceDemandModel:
    """Calibratable planning model; not a substitute for hardware benchmarking."""

    model_id: str
    prefill_tokens_per_s: float
    decode_tokens_per_s: float
    fixed_model_overhead_ms: float
    retrieval_latency_p50_ms: float
    tool_latency_p50_ms: float
    network_latency_p50_ms: float
    contention_penalty_per_active_request: float = 0.015
    workflow_slots: int = 8

    def __post_init__(self) -> None:
        for name in (
            "prefill_tokens_per_s",
            "decode_tokens_per_s",
            "fixed_model_overhead_ms",
            "retrieval_latency_p50_ms",
            "tool_latency_p50_ms",
            "network_latency_p50_ms",
        ):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")
        if self.contention_penalty_per_active_request < 0:
            raise ValueError("contention penalty cannot be negative")
        if self.workflow_slots <= 0:
            raise ValueError("workflow_slots must be positive")


@dataclass(frozen=True, slots=True)
class BenchmarkScenario:
    scenario_id: str
    profile: WorkloadProfile
    service_model: ServiceDemandModel
    request_count: int
    seed: int
    warmup_requests: int = 0

    def __post_init__(self) -> None:
        if not self.scenario_id:
            raise ValueError("scenario_id is required")
        if self.request_count <= 0:
            raise ValueError("request_count must be positive")
        if self.warmup_requests < 0 or self.warmup_requests >= self.request_count:
            raise ValueError("warmup_requests must be >=0 and less than request_count")
        if self.profile.status == "inactive_future":
            raise ValueError("inactive_future profiles cannot be executed")


@dataclass(frozen=True, slots=True)
class BenchmarkObservation:
    request_id: str
    profile_id: str
    arrival_s: float
    start_s: float
    end_s: float
    queue_ms: float
    ttft_ms: float
    itl_ms: float
    e2e_ms: float
    isl_tokens: int
    osl_tokens: int
    model_calls: int
    tool_calls: int
    retrieval_calls: int
    turns: int
    success: bool

    def __post_init__(self) -> None:
        if self.start_s < self.arrival_s or self.end_s < self.start_s:
            raise ValueError("invalid observation timestamps")
        if min(self.queue_ms, self.ttft_ms, self.itl_ms, self.e2e_ms) < 0:
            raise ValueError("latencies cannot be negative")
        if self.e2e_ms + 1e-6 < self.ttft_ms:
            raise ValueError("e2e latency cannot be less than TTFT")


@dataclass(frozen=True, slots=True)
class CapacityEnvelope:
    profile_id: str
    max_sustainable_request_rate_per_s: float
    max_tested_concurrency: int
    ttft_p95_ms: float
    itl_p95_ms: float
    e2e_p95_ms: float
    queue_p95_ms: float
    throughput_output_tokens_per_s: float
    slo_attainment: float
    evidence_kind: str
    recommendation: str

    def __post_init__(self) -> None:
        if self.max_sustainable_request_rate_per_s < 0:
            raise ValueError("rate cannot be negative")
        if self.max_tested_concurrency <= 0:
            raise ValueError("concurrency must be positive")
        if not 0 <= self.slo_attainment <= 1:
            raise ValueError("slo_attainment must be in [0, 1]")
        if self.evidence_kind not in {"simulated", "synthetic_endpoint", "trace_replay", "production"}:
            raise ValueError("invalid evidence_kind")


def weighted_mean(values: Iterable[tuple[float, float]]) -> float:
    pairs = list(values)
    denominator = sum(weight for _, weight in pairs)
    if denominator <= 0:
        raise ValueError("weights must total > 0")
    return sum(value * weight for value, weight in pairs) / denominator
