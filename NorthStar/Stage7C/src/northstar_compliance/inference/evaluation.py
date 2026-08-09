from __future__ import annotations

from dataclasses import dataclass

from .models import InferenceBenchmarkObservation, InferenceOptimizationPolicy, QualityParityRecord


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    evaluation_id: str
    passed: bool
    observed: float | bool | str
    threshold: float | bool | str
    message: str


def evaluate_candidate(observation: InferenceBenchmarkObservation, policy: InferenceOptimizationPolicy, quality: QualityParityRecord) -> tuple[EvaluationResult, ...]:
    results: list[EvaluationResult] = []
    results.append(EvaluationResult("EVAL-101", not observation.raw_payload_captured, observation.raw_payload_captured, False, "Raw payload capture remains disabled."))
    results.append(EvaluationResult("EVAL-102", quality.passed, quality.passed, True, "Quality parity gate."))
    results.append(EvaluationResult("EVAL-103", quality.structured_validity_rate >= 0.99, quality.structured_validity_rate, 0.99, "Structured output validity gate."))
    results.append(EvaluationResult("EVAL-104", quality.groundedness_delta >= -0.01, quality.groundedness_delta, -0.01, "Groundedness regression tolerance."))
    results.append(EvaluationResult("EVAL-105", quality.task_success_delta >= -0.01, quality.task_success_delta, -0.01, "Task-success regression tolerance."))
    plan = policy.speculative_plan
    if plan.enabled:
        acceptance = observation.acceptance_rate or 0.0
        results.append(EvaluationResult("EVAL-106", acceptance >= plan.minimum_acceptance_rate, acceptance, plan.minimum_acceptance_rate, "Speculative acceptance-rate gate."))
        results.append(EvaluationResult("EVAL-107", observation.decode_improvement >= plan.minimum_decode_improvement, observation.decode_improvement, plan.minimum_decode_improvement, "Decode improvement gate."))
        results.append(EvaluationResult("EVAL-108", observation.e2e_improvement >= plan.minimum_e2e_improvement, observation.e2e_improvement, plan.minimum_e2e_improvement, "End-to-end improvement gate."))
        results.append(EvaluationResult("EVAL-109", observation.candidate_memory_overhead_ratio <= plan.maximum_memory_overhead_ratio, observation.candidate_memory_overhead_ratio, plan.maximum_memory_overhead_ratio, "Memory overhead gate."))
        results.append(EvaluationResult("EVAL-110", quality.lossless_distribution_verified if plan.require_lossless_distribution else True, quality.lossless_distribution_verified, True, "Lossless-distribution verification gate."))
    else:
        for eval_id in ("EVAL-106", "EVAL-107", "EVAL-108", "EVAL-109", "EVAL-110"):
            results.append(EvaluationResult(eval_id, True, "not_applicable", "not_applicable", "Speculation disabled."))
    results.append(EvaluationResult("EVAL-111", observation.candidate_ttft_ms >= 0, observation.candidate_ttft_ms, 0.0, "TTFT is present and non-negative."))
    results.append(EvaluationResult("EVAL-112", observation.candidate_itl_ms >= 0, observation.candidate_itl_ms, 0.0, "ITL is present and non-negative."))
    results.append(EvaluationResult("EVAL-113", observation.candidate_e2e_ms >= observation.candidate_ttft_ms, observation.candidate_e2e_ms, observation.candidate_ttft_ms, "End-to-end latency contains TTFT."))
    results.append(EvaluationResult("EVAL-114", 0.0 <= observation.cache_hit_rate <= 1.0, observation.cache_hit_rate, 1.0, "Cache-hit rate is bounded and declared."))
    prior_pass = observation.success and all(item.passed for item in results)
    results.append(EvaluationResult("EVAL-115", prior_pass, prior_pass, True, "Overall candidate gate."))
    return tuple(results)
