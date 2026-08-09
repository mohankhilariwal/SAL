from __future__ import annotations

from dataclasses import dataclass

from .metrics import percentile, summarize
from .models import BenchmarkObservation, WorkloadProfile


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    evaluation_id: str
    passed: bool
    detail: str


def evaluate_profile(profile: WorkloadProfile, observations: list[BenchmarkObservation]) -> list[EvaluationResult]:
    metrics = summarize(observations, profile.slo)
    results = [
        EvaluationResult("EVAL-089", profile.total_weight > 0, "distribution weights are positive"),
        EvaluationResult(
            "EVAL-090",
            all(obs.isl_tokens >= 1 and obs.osl_tokens >= 1 for obs in observations),
            "all sampled sequence lengths are positive",
        ),
        EvaluationResult(
            "EVAL-091",
            all(obs.e2e_ms >= obs.ttft_ms for obs in observations),
            "end-to-end latency contains TTFT",
        ),
        EvaluationResult(
            "EVAL-092",
            float(metrics["success_rate"]) >= profile.slo.success_rate_min,
            "success-rate hypothesis",
        ),
        EvaluationResult(
            "EVAL-093",
            float(metrics["queue_p95_ms"]) <= profile.slo.queue_p95_ms,
            "queue-delay hypothesis",
        ),
        EvaluationResult(
            "EVAL-094",
            float(metrics["e2e_p95_ms"]) <= profile.slo.e2e_p95_ms,
            "end-to-end latency hypothesis",
        ),
        EvaluationResult(
            "EVAL-095",
            profile.slo.ttft_p95_ms is None
            or float(metrics["ttft_p95_ms"]) <= profile.slo.ttft_p95_ms,
            "TTFT hypothesis",
        ),
        EvaluationResult(
            "EVAL-096",
            profile.slo.itl_p95_ms is None
            or float(metrics["itl_p95_ms"]) <= profile.slo.itl_p95_ms,
            "ITL hypothesis",
        ),
        EvaluationResult(
            "EVAL-097",
            all(obs.model_calls >= 1 for obs in observations),
            "workflow call-count integrity",
        ),
        EvaluationResult(
            "EVAL-098",
            not profile.capture_payloads,
            "raw prompt/response capture is disabled",
        ),
        EvaluationResult(
            "EVAL-099",
            profile.status in {"bootstrap_assumption", "measured"},
            "only active profile states execute",
        ),
        EvaluationResult(
            "EVAL-100",
            len({obs.request_id for obs in observations}) == len(observations),
            "request identities are unique",
        ),
    ]
    return results
