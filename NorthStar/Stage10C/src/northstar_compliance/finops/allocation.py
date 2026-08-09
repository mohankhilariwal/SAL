from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from .costing import CostCalculator
from .models import CostEvent, money


@dataclass(frozen=True)
class AllocationRecord:
    dimension: str
    value: str
    amount: Decimal
    currency: str = "CAD"
    authority_effect: str = "none"


_ALLOWED_DIMENSIONS = {
    "business_unit", "jurisdiction", "environment", "workload_profile_id", "case_id", "run_id"
}


def allocate(events: Iterable[CostEvent], calculator: CostCalculator, dimension: str) -> tuple[AllocationRecord, ...]:
    if dimension not in _ALLOWED_DIMENSIONS:
        raise ValueError(f"unsupported allocation dimension: {dimension}")
    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for event in events:
        value = getattr(event, dimension) or "unassigned"
        totals[str(value)] += calculator.price_event(event).amount
    return tuple(
        AllocationRecord(dimension, value, money(amount))
        for value, amount in sorted(totals.items())
    )
