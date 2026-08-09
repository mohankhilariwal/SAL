from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class WorkloadDemandProfile:
    profile_id: str
    arrival_rate_rps: Decimal
    peak_multiplier: Decimal
    p95_service_time_seconds: Decimal
    worker_concurrency: int
    target_utilization: Decimal
    average_input_tokens: int
    average_output_tokens: int
    protected_write_fraction: Decimal = Decimal("0")
    maximum_queue_wait_seconds: Decimal = Decimal("30")
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if self.arrival_rate_rps < 0 or self.peak_multiplier < 1:
            raise ValueError("invalid arrival or peak multiplier")
        if self.p95_service_time_seconds <= 0 or self.worker_concurrency <= 0:
            raise ValueError("invalid service time or concurrency")
        if not (Decimal("0") < self.target_utilization <= Decimal("1")):
            raise ValueError("target utilization must be in (0,1]")
        if not (Decimal("0") <= self.protected_write_fraction <= Decimal("1")):
            raise ValueError("protected write fraction must be in [0,1]")
        if self.authority_effect != "none":
            raise ValueError("capacity profiles cannot create authority")


@dataclass(frozen=True)
class CapacityEnvelope:
    profile_id: str
    peak_rps: Decimal
    offered_concurrency: Decimal
    required_workers: int
    input_tokens_per_second: Decimal
    output_tokens_per_second: Decimal
    queue_capacity_requests: int
    protected_write_arrival_rate_rps: Decimal
    protected_write_concurrency_limit: int = 1
    headroom_fraction: Decimal = Decimal("0.25")
    authority_effect: str = "none"
