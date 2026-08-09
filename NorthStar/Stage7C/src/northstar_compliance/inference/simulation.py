from __future__ import annotations

from dataclasses import dataclass
import math

from .models import InferenceBenchmarkObservation, InferenceBenchmarkScenario, QualityParityRecord


@dataclass(frozen=True, slots=True)
class ServiceRates:
    prefill_tokens_per_second: float = 6_000.0
    decode_tokens_per_second: float = 90.0
    fixed_request_ms: float = 45.0
    network_ms: float = 25.0
    bytes_per_kv_token: int = 131_072
    batching_throughput_gain: float = 0.25
    batching_ttft_penalty_ms: float = 8.0
    chunked_prefill_ttft_gain: float = 0.12
    prefix_cache_read_fraction: float = 0.10
    quantization_decode_gain: float = 0.15
    quantization_memory_reduction: float = 0.35
    parallelism_decode_gain: float = 0.10
    parallelism_overhead_ms: float = 12.0
    draft_token_ms: float = 1.8
    verification_cost_multiplier: float = 1.08

    def __post_init__(self) -> None:
        if self.prefill_tokens_per_second <= 0 or self.decode_tokens_per_second <= 0:
            raise ValueError("service rates must be positive")
        if self.bytes_per_kv_token <= 0:
            raise ValueError("bytes_per_kv_token must be positive")


def expected_accepted_draft_tokens(acceptance_rate: float, speculative_tokens: int) -> float:
    if speculative_tokens <= 0 or acceptance_rate <= 0:
        return 0.0
    if acceptance_rate >= 1.0:
        return float(speculative_tokens)
    return sum(acceptance_rate**i for i in range(1, speculative_tokens + 1))


def _baseline_metrics(scenario: InferenceBenchmarkScenario, rates: ServiceRates) -> dict[str, float]:
    workload = scenario.workload
    isl = float(workload.median_isl_tokens)
    osl = float(workload.median_osl_tokens)
    prefill_ms = isl / rates.prefill_tokens_per_second * 1_000.0
    decode_ms = osl / rates.decode_tokens_per_second * 1_000.0
    ttft_ms = rates.fixed_request_ms + rates.network_ms + prefill_ms
    itl_ms = 1_000.0 / rates.decode_tokens_per_second if osl > 1 else 0.0
    external_ms = (prefill_ms + decode_ms) * workload.external_latency_fraction / max(1e-9, 1 - workload.external_latency_fraction)
    e2e_ms = ttft_ms + decode_ms + external_ms
    output_tps = osl / max(decode_ms / 1_000.0, 1e-9)
    kv_mb = (isl + osl) * rates.bytes_per_kv_token * max(1, workload.expected_concurrency) / 1_000_000.0
    return {"prefill_ms": prefill_ms, "decode_ms": decode_ms, "ttft_ms": ttft_ms, "itl_ms": itl_ms, "external_ms": external_ms, "e2e_ms": e2e_ms, "output_tps": output_tps, "kv_mb": kv_mb}


def simulate_inference_candidate(scenario: InferenceBenchmarkScenario, quality: QualityParityRecord, *, rates: ServiceRates | None = None, assumed_acceptance_rate: float | None = None, cache_hit_rate: float | None = None) -> InferenceBenchmarkObservation:
    rates = rates or ServiceRates()
    baseline = _baseline_metrics(scenario, rates)
    workload = scenario.workload
    policy = scenario.policy
    effective_isl = workload.median_isl_tokens * (1.0 - policy.context_reduction_ratio)
    chosen_cache_hit = 0.0
    if policy.cache_policy.enabled:
        if cache_hit_rate is None:
            chosen_cache_hit = workload.repeated_prefix_ratio if scenario.cache_state == "representative" else (0.0 if scenario.cache_state == "cold" else 0.85)
        else:
            chosen_cache_hit = cache_hit_rate
        chosen_cache_hit = min(max(chosen_cache_hit, 0.0), 1.0)
    prefill_work_tokens = effective_isl
    if policy.cache_policy.enabled:
        cached_fraction = chosen_cache_hit * workload.repeated_prefix_ratio
        prefill_work_tokens *= 1.0 - cached_fraction * (1.0 - rates.prefix_cache_read_fraction)
    candidate_prefill_ms = prefill_work_tokens / rates.prefill_tokens_per_second * 1_000.0
    candidate_osl = float(workload.median_osl_tokens)
    if policy.output_token_cap is not None:
        candidate_osl = min(candidate_osl, float(policy.output_token_cap))
    decode_tps = rates.decode_tokens_per_second
    memory_reduction = 0.0
    if policy.quantization in {"fp8", "int8", "int4"}:
        decode_tps *= 1.0 + rates.quantization_decode_gain
        memory_reduction = rates.quantization_memory_reduction
    if policy.tensor_parallel_size > 1:
        decode_tps *= 1.0 + rates.parallelism_decode_gain * math.log2(policy.tensor_parallel_size)
    acceptance = None
    accepted_tokens = None
    memory_overhead_ratio = 0.0
    if policy.speculative_plan.enabled:
        acceptance = 0.60 if assumed_acceptance_rate is None else min(max(assumed_acceptance_rate, 0.0), 1.0)
        accepted_tokens = expected_accepted_draft_tokens(acceptance, policy.speculative_plan.num_speculative_tokens)
        target_steps = candidate_osl / max(1.0 + accepted_tokens, 1.0)
        target_step_ms = 1_000.0 / decode_tps * rates.verification_cost_multiplier
        draft_ms = target_steps * policy.speculative_plan.num_speculative_tokens * rates.draft_token_ms
        candidate_decode_ms = target_steps * target_step_ms + draft_ms
        memory_overhead_ratio = min(1.0, 0.04 * policy.speculative_plan.num_speculative_tokens)
    else:
        candidate_decode_ms = candidate_osl / decode_tps * 1_000.0
    ttft_penalty = 0.0
    if policy.batching_policy.mode in {"dynamic", "continuous", "offline_batch"}:
        candidate_decode_ms /= 1.0 + rates.batching_throughput_gain
        ttft_penalty = rates.batching_ttft_penalty_ms + policy.batching_policy.max_wait_ms / 2.0
    if policy.batching_policy.chunked_prefill:
        candidate_prefill_ms *= 1.0 - rates.chunked_prefill_ttft_gain
    parallel_overhead = rates.parallelism_overhead_ms if policy.tensor_parallel_size > 1 else 0.0
    candidate_ttft = rates.fixed_request_ms + rates.network_ms + candidate_prefill_ms + ttft_penalty + parallel_overhead
    candidate_itl = candidate_decode_ms / max(candidate_osl - 1.0, 1.0)
    candidate_e2e = candidate_ttft + candidate_decode_ms + baseline["external_ms"]
    candidate_tps = candidate_osl / max(candidate_decode_ms / 1_000.0, 1e-9)
    candidate_kv_mb = baseline["kv_mb"] * (1.0 - memory_reduction) * (1.0 + memory_overhead_ratio)
    return InferenceBenchmarkObservation(
        observation_id=f"IBO-{scenario.scenario_id[4:]}", scenario_digest=scenario.digest(), profile_id=workload.profile_id, evidence_kind=scenario.evidence_kind,
        baseline_ttft_ms=baseline["ttft_ms"], candidate_ttft_ms=candidate_ttft, baseline_itl_ms=baseline["itl_ms"], candidate_itl_ms=candidate_itl,
        baseline_e2e_ms=baseline["e2e_ms"], candidate_e2e_ms=candidate_e2e, baseline_output_tps=baseline["output_tps"], candidate_output_tps=candidate_tps,
        acceptance_rate=acceptance, mean_accepted_tokens=accepted_tokens, kv_cache_mb=candidate_kv_mb, candidate_memory_overhead_ratio=memory_overhead_ratio,
        cache_hit_rate=chosen_cache_hit, quality_parity_record_id=quality.record_id, success=quality.passed,
    )
