from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .models import WorkloadProfile


@dataclass(frozen=True, slots=True)
class ExternalBenchmarkPlan:
    tool: str
    command: tuple[str, ...]
    notes: tuple[str, ...]


def _weighted_mode(profile: WorkloadProfile, field: str) -> int:
    numerator = sum(getattr(bucket, field) * bucket.weight for bucket in profile.buckets)
    return max(1, int(round(numerator / profile.total_weight)))


def build_aiperf_plan(profile: WorkloadProfile, *, endpoint: str, model: str, request_count: int = 200) -> ExternalBenchmarkPlan:
    """Create, but do not execute, an AIPerf bootstrap command.

    The command uses weighted modal lengths only as a smoke-test. The profile's
    mixture distribution remains authoritative and should be exported to a
    dataset/trace for a real benchmark.
    """
    if profile.status == "inactive_future":
        raise ValueError("inactive profile cannot be benchmarked")
    concurrency = profile.arrival.max_concurrency or 1
    command = (
        "aiperf", "profile",
        "--model", model,
        "--endpoint-type", "chat",
        "--endpoint", "/v1/chat/completions",
        "--url", endpoint,
        "--streaming",
        "--concurrency", str(concurrency),
        "--request-count", str(request_count),
        "--synthetic-input-tokens-mean", str(_weighted_mode(profile, "isl_mode")),
        "--output-tokens-mean", str(_weighted_mode(profile, "osl_mode")),
    )
    if profile.arrival.request_rate_per_s is not None:
        command += ("--request-rate", str(profile.arrival.request_rate_per_s), "--request-rate-mode", "poisson")
    return ExternalBenchmarkPlan(
        tool="NVIDIA AIPerf",
        command=command,
        notes=(
            "Smoke-test only; use a trace or sequence-length distribution for decision evidence.",
            "Record tokenizer identity and actual observed input/output token counts.",
            "Do not change DATA-106 automatically from this command's result.",
        ),
    )


def build_vllm_plan(profile: WorkloadProfile, *, endpoint: str, model: str, request_count: int = 200) -> ExternalBenchmarkPlan:
    if profile.status == "inactive_future":
        raise ValueError("inactive profile cannot be benchmarked")
    command = (
        "vllm", "bench", "serve",
        "--backend", "openai-chat",
        "--base-url", endpoint,
        "--model", model,
        "--dataset-name", "random",
        "--num-prompts", str(request_count),
        "--input-len", str(_weighted_mode(profile, "isl_mode")),
        "--output-len", str(_weighted_mode(profile, "osl_mode")),
        "--max-concurrency", str(profile.arrival.max_concurrency or 1),
    )
    if profile.arrival.request_rate_per_s is not None:
        command += ("--request-rate", str(profile.arrival.request_rate_per_s),)
    return ExternalBenchmarkPlan(
        tool="vLLM bench serve",
        command=command,
        notes=(
            "Smoke-test only; fixed lengths do not replace the joint ISL/OSL profile.",
            "Run a rate/concurrency sweep and retain per-request results.",
        ),
    )


def export_sample_trace(profile: WorkloadProfile, sampled: list[object], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in sampled:
        rows.append({
            "request_id": getattr(item, "request_id"),
            "scheduled_timestamp_s": getattr(item, "arrival_s"),
            "isl_tokens": getattr(item, "isl_tokens"),
            "osl_tokens": getattr(item, "osl_tokens"),
            "model_calls": getattr(item, "model_calls"),
            "tool_calls": getattr(item, "tool_calls"),
            "retrieval_calls": getattr(item, "retrieval_calls"),
            "turns": getattr(item, "turns"),
            "profile_id": profile.profile_id,
            "profile_version": profile.version,
            "profile_digest": profile.digest,
            "tokenizer_id": profile.tokenizer_id,
        })
    target.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
