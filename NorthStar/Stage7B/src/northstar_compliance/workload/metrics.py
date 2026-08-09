from __future__ import annotations

from dataclasses import asdict
import math
from statistics import mean
from typing import Iterable

from .models import BenchmarkObservation, SLOHypothesis


def percentile(values: Iterable[float], quantile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("values cannot be empty")
    if not 0 <= quantile <= 1:
        raise ValueError("quantile must be in [0,1]")
    if len(ordered) == 1:
        return float(ordered[0])
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    fraction = position - lower
    return float(ordered[lower] + (ordered[upper] - ordered[lower]) * fraction)


def summarize(observations: list[BenchmarkObservation], slo: SLOHypothesis) -> dict[str, float | int]:
    if not observations:
        raise ValueError("observations cannot be empty")
    duration = max(obs.end_s for obs in observations) - min(obs.arrival_s for obs in observations)
    duration = max(duration, 1e-9)
    success_count = sum(obs.success for obs in observations)
    output_tokens = sum(obs.osl_tokens * obs.model_calls for obs in observations if obs.success)
    input_tokens = sum(obs.isl_tokens * obs.model_calls for obs in observations if obs.success)

    def p(field: str, q: float) -> float:
        return percentile([float(getattr(obs, field)) for obs in observations], q)

    compliant = []
    for obs in observations:
        ok = obs.success and obs.e2e_ms <= slo.e2e_p95_ms and obs.queue_ms <= slo.queue_p95_ms
        if slo.ttft_p95_ms is not None:
            ok = ok and obs.ttft_ms <= slo.ttft_p95_ms
        if slo.itl_p95_ms is not None:
            ok = ok and obs.itl_ms <= slo.itl_p95_ms
        compliant.append(ok)

    return {
        "requests": len(observations),
        "success_rate": success_count / len(observations),
        "slo_attainment": sum(compliant) / len(compliant),
        "duration_s": duration,
        "request_throughput_per_s": success_count / duration,
        "input_token_throughput_per_s": input_tokens / duration,
        "output_token_throughput_per_s": output_tokens / duration,
        "queue_p50_ms": p("queue_ms", 0.50),
        "queue_p95_ms": p("queue_ms", 0.95),
        "queue_p99_ms": p("queue_ms", 0.99),
        "ttft_p50_ms": p("ttft_ms", 0.50),
        "ttft_p95_ms": p("ttft_ms", 0.95),
        "ttft_p99_ms": p("ttft_ms", 0.99),
        "itl_p50_ms": p("itl_ms", 0.50),
        "itl_p95_ms": p("itl_ms", 0.95),
        "itl_p99_ms": p("itl_ms", 0.99),
        "e2e_p50_ms": p("e2e_ms", 0.50),
        "e2e_p95_ms": p("e2e_ms", 0.95),
        "e2e_p99_ms": p("e2e_ms", 0.99),
        "mean_isl": mean(obs.isl_tokens for obs in observations),
        "mean_osl": mean(obs.osl_tokens for obs in observations),
        "mean_model_calls": mean(obs.model_calls for obs in observations),
        "mean_tool_calls": mean(obs.tool_calls for obs in observations),
        "mean_retrieval_calls": mean(obs.retrieval_calls for obs in observations),
    }


def littles_law_concurrency(request_rate_per_s: float, mean_latency_s: float) -> float:
    if request_rate_per_s < 0 or mean_latency_s < 0:
        raise ValueError("inputs cannot be negative")
    return request_rate_per_s * mean_latency_s
