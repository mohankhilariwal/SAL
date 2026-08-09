from __future__ import annotations

from decimal import Decimal, ROUND_CEILING

from .models import CapacityEnvelope, WorkloadDemandProfile


def ceil_decimal(value: Decimal) -> int:
    return int(value.to_integral_value(rounding=ROUND_CEILING))


class CapacityPlanner:
    def estimate(self, profile: WorkloadDemandProfile, *, headroom_fraction: Decimal = Decimal("0.25")) -> CapacityEnvelope:
        if headroom_fraction < 0:
            raise ValueError("headroom must be non-negative")
        peak_rps = profile.arrival_rate_rps * profile.peak_multiplier
        offered_concurrency = peak_rps * profile.p95_service_time_seconds
        effective_worker_capacity = Decimal(profile.worker_concurrency) * profile.target_utilization
        base_workers = ceil_decimal(offered_concurrency / effective_worker_capacity) if peak_rps else 0
        required_workers = ceil_decimal(Decimal(base_workers) * (Decimal("1") + headroom_fraction)) if base_workers else 0
        queue_capacity = ceil_decimal(peak_rps * profile.maximum_queue_wait_seconds)
        protected_rate = peak_rps * profile.protected_write_fraction
        return CapacityEnvelope(
            profile_id=profile.profile_id,
            peak_rps=peak_rps,
            offered_concurrency=offered_concurrency,
            required_workers=required_workers,
            input_tokens_per_second=peak_rps * Decimal(profile.average_input_tokens),
            output_tokens_per_second=peak_rps * Decimal(profile.average_output_tokens),
            queue_capacity_requests=queue_capacity,
            protected_write_arrival_rate_rps=protected_rate,
            protected_write_concurrency_limit=1,
            headroom_fraction=headroom_fraction,
        )
