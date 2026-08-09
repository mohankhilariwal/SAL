from __future__ import annotations

from dataclasses import replace
import heapq
from math import ceil

from .metrics import summarize
from .models import BenchmarkObservation, BenchmarkScenario, CapacityEnvelope, ServiceDemandModel
from .sampling import SampledRequest, WorkloadSampler


class CapacitySimulator:
    """Deterministic discrete-event planning simulator.

    It is deliberately conservative and calibratable. It does not model GPU
    kernels, scheduler internals, cache eviction or vendor-specific batching.
    Its output is evidence of scenario arithmetic, not production capacity.
    """

    def __init__(self, scenario: BenchmarkScenario) -> None:
        self.scenario = scenario

    def _service_demand(self, request: SampledRequest, active_hint: int) -> tuple[float, float, float]:
        model = self.scenario.service_model
        contention = 1.0 + model.contention_penalty_per_active_request * max(0, active_hint - 1)
        prefill_s = (
            request.model_calls * (request.isl_tokens / model.prefill_tokens_per_s)
            + request.model_calls * model.fixed_model_overhead_ms / 1000.0
        ) * contention
        decode_s = (
            request.model_calls * (request.osl_tokens / model.decode_tokens_per_s)
        ) * contention
        external_s = (
            request.retrieval_calls * model.retrieval_latency_p50_ms
            + request.tool_calls * model.tool_latency_p50_ms
            + request.model_calls * model.network_latency_p50_ms
        ) / 1000.0
        return prefill_s, decode_s, external_s

    def run(self) -> list[BenchmarkObservation]:
        profile = self.scenario.profile
        requests = WorkloadSampler(profile, self.scenario.seed).sample(self.scenario.request_count)
        slots = self.scenario.service_model.workflow_slots
        slot_heap: list[tuple[float, int]] = [(0.0, index) for index in range(slots)]
        heapq.heapify(slot_heap)
        observations: list[BenchmarkObservation] = []

        for request in requests:
            available_s, slot_id = heapq.heappop(slot_heap)
            start_s = max(request.arrival_s, available_s)
            # Approximate active pressure using occupied slots at admission time.
            active_hint = 1 + sum(1 for free_s, _ in slot_heap if free_s > start_s)
            prefill_s, decode_s, external_s = self._service_demand(request, active_hint)
            network_s = self.scenario.service_model.network_latency_p50_ms / 1000.0
            queue_s = start_s - request.arrival_s
            # Retrieval commonly precedes the first grounded model call.
            retrieval_before_first_s = (
                min(1, request.retrieval_calls)
                * self.scenario.service_model.retrieval_latency_p50_ms
                / 1000.0
            )
            ttft_s = queue_s + retrieval_before_first_s + network_s + prefill_s / max(1, request.model_calls)
            service_s = prefill_s + decode_s + external_s
            end_s = start_s + service_s
            itl_ms = 0.0
            if request.osl_tokens > 1:
                itl_ms = decode_s * 1000.0 / max(1, request.model_calls * (request.osl_tokens - 1))
            observations.append(
                BenchmarkObservation(
                    request_id=request.request_id,
                    profile_id=profile.profile_id,
                    arrival_s=request.arrival_s,
                    start_s=start_s,
                    end_s=end_s,
                    queue_ms=queue_s * 1000.0,
                    ttft_ms=ttft_s * 1000.0,
                    itl_ms=itl_ms,
                    e2e_ms=(end_s - request.arrival_s) * 1000.0,
                    isl_tokens=request.isl_tokens,
                    osl_tokens=request.osl_tokens,
                    model_calls=request.model_calls,
                    tool_calls=request.tool_calls,
                    retrieval_calls=request.retrieval_calls,
                    turns=request.turns,
                    success=True,
                )
            )
            heapq.heappush(slot_heap, (end_s, slot_id))

        if self.scenario.warmup_requests:
            return observations[self.scenario.warmup_requests :]
        return observations

    def summarize(self) -> dict[str, float | int]:
        return summarize(self.run(), self.scenario.profile.slo)


def derive_capacity_envelope(
    base_scenario: BenchmarkScenario,
    candidate_rates: list[float],
    *,
    minimum_slo_attainment: float = 0.95,
) -> CapacityEnvelope:
    if not candidate_rates:
        raise ValueError("candidate_rates cannot be empty")
    if not 0 < minimum_slo_attainment <= 1:
        raise ValueError("minimum_slo_attainment must be in (0,1]")

    best_rate = 0.0
    best_summary: dict[str, float | int] | None = None
    for rate in sorted(candidate_rates):
        arrival = replace(base_scenario.profile.arrival, request_rate_per_s=rate)
        profile = replace(base_scenario.profile, arrival=arrival)
        scenario = replace(base_scenario, profile=profile, scenario_id=f"{base_scenario.scenario_id}-R{rate:g}")
        summary = CapacitySimulator(scenario).summarize()
        if float(summary["slo_attainment"]) >= minimum_slo_attainment:
            best_rate = rate
            best_summary = summary
        else:
            break

    if best_summary is None:
        # Return a zero-rate envelope with evidence from the lowest tested rate.
        rate = min(candidate_rates)
        profile = replace(
            base_scenario.profile,
            arrival=replace(base_scenario.profile.arrival, request_rate_per_s=rate),
        )
        best_summary = CapacitySimulator(replace(base_scenario, profile=profile)).summarize()

    return CapacityEnvelope(
        profile_id=base_scenario.profile.profile_id,
        max_sustainable_request_rate_per_s=best_rate,
        max_tested_concurrency=base_scenario.service_model.workflow_slots,
        ttft_p95_ms=float(best_summary["ttft_p95_ms"]),
        itl_p95_ms=float(best_summary["itl_p95_ms"]),
        e2e_p95_ms=float(best_summary["e2e_p95_ms"]),
        queue_p95_ms=float(best_summary["queue_p95_ms"]),
        throughput_output_tokens_per_s=float(best_summary["output_token_throughput_per_s"]),
        slo_attainment=float(best_summary["slo_attainment"]),
        evidence_kind="simulated",
        recommendation=(
            "Use only as a lower-confidence planning envelope. Replace with tokenizer-accurate trace replay "
            "and endpoint measurements before changing DATA-106 admission limits."
        ),
    )
