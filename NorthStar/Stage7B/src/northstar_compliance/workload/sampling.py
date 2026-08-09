from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Iterable

from .models import ArrivalKind, DistributionBucket, WorkloadProfile


@dataclass(frozen=True, slots=True)
class SampledRequest:
    request_id: str
    arrival_s: float
    isl_tokens: int
    osl_tokens: int
    model_calls: int
    tool_calls: int
    retrieval_calls: int
    turns: int
    bucket_id: str


class WorkloadSampler:
    def __init__(self, profile: WorkloadProfile, seed: int) -> None:
        self.profile = profile
        self.rng = random.Random(seed)

    def _choose_bucket(self) -> DistributionBucket:
        threshold = self.rng.random() * self.profile.total_weight
        cumulative = 0.0
        for bucket in self.profile.buckets:
            cumulative += bucket.weight
            if threshold <= cumulative:
                return bucket
        return self.profile.buckets[-1]

    def _triangular_int(self, low: int, mode: int, high: int) -> int:
        if low == high:
            return low
        return max(low, min(high, int(round(self.rng.triangular(low, high, mode)))))

    def _arrival_times(self, count: int) -> list[float]:
        arrival = self.profile.arrival
        if arrival.kind is ArrivalKind.BATCH:
            return [0.0] * count
        if arrival.kind is ArrivalKind.CLOSED_LOOP:
            # Closed-loop concurrency is represented as an initial wave. The
            # simulator releases the next request when a slot becomes free.
            cap = arrival.max_concurrency or 1
            return [float(index // cap) * 1e-9 for index in range(count)]

        rate = arrival.request_rate_per_s or 1.0
        current = 0.0
        times: list[float] = []
        for index in range(count):
            if arrival.kind is ArrivalKind.CONSTANT:
                delta = 0.0 if index == 0 else 1.0 / rate
            elif arrival.kind is ArrivalKind.POISSON:
                delta = 0.0 if index == 0 else self.rng.expovariate(rate)
            elif arrival.kind is ArrivalKind.BURST:
                cycle = arrival.burst_duration_s + arrival.quiet_duration_s
                cycle_position = current % cycle
                effective_rate = rate * arrival.burst_multiplier if cycle_position < arrival.burst_duration_s else rate
                delta = 0.0 if index == 0 else self.rng.expovariate(effective_rate)
            else:
                raise AssertionError(f"unsupported arrival kind: {arrival.kind}")
            current += delta
            times.append(current)
        return times

    def sample(self, count: int) -> list[SampledRequest]:
        if count <= 0:
            raise ValueError("count must be positive")
        arrivals = self._arrival_times(count)
        requests: list[SampledRequest] = []
        for index, arrival_s in enumerate(arrivals):
            bucket = self._choose_bucket()
            turns = self._triangular_int(
                self.profile.turns_min, self.profile.turns_mode, self.profile.turns_max
            )
            base_isl = self._triangular_int(bucket.isl_min, bucket.isl_mode, bucket.isl_max)
            # The profile models retained context growth explicitly. This does
            # not imply that all systems retain every token.
            growth = 1.0 + self.profile.context_growth_per_turn * max(0, turns - 1)
            isl = max(1, int(round(base_isl * growth)))
            requests.append(
                SampledRequest(
                    request_id=f"REQ-{index + 1:06d}",
                    arrival_s=arrival_s,
                    isl_tokens=isl,
                    osl_tokens=self._triangular_int(bucket.osl_min, bucket.osl_mode, bucket.osl_max),
                    model_calls=self._triangular_int(
                        bucket.model_calls_min, bucket.model_calls_mode, bucket.model_calls_max
                    ),
                    tool_calls=self._triangular_int(
                        bucket.tool_calls_min, bucket.tool_calls_mode, bucket.tool_calls_max
                    ),
                    retrieval_calls=self._triangular_int(
                        bucket.retrieval_calls_min,
                        bucket.retrieval_calls_mode,
                        bucket.retrieval_calls_max,
                    ),
                    turns=turns,
                    bucket_id=bucket.bucket_id,
                )
            )
        return requests
