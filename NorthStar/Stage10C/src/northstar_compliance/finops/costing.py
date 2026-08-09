from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from typing import Iterable, Mapping

from .models import CostCategory, CostEvent, CostLine, CostRate, UnitEconomicsReport, money


class RateCard:
    def __init__(self, rates: Iterable[CostRate]):
        self._rates = {rate.category: rate for rate in rates}
        if len(self._rates) == 0:
            raise ValueError("at least one rate is required")

    def rate_for(self, category: CostCategory) -> CostRate:
        try:
            return self._rates[category]
        except KeyError as exc:
            raise KeyError(f"missing rate for {category}") from exc


class CostCalculator:
    def __init__(self, rate_card: RateCard):
        self.rate_card = rate_card

    def price_event(self, event: CostEvent) -> CostLine:
        rate = self.rate_card.rate_for(event.category)
        if rate.unit != event.unit:
            raise ValueError(f"unit mismatch for {event.category}: {event.unit} != {rate.unit}")
        amount = money(event.quantity * rate.rate)
        return CostLine(event.category, event.quantity, rate.rate, amount, rate.currency)

    def report(
        self,
        events: Iterable[CostEvent],
        *,
        completed_task_ids: Iterable[str],
        document_ids: Iterable[str],
        human_escalation_ids: Iterable[str],
    ) -> UnitEconomicsReport:
        events = tuple(events)
        grouped_quantity: dict[CostCategory, Decimal] = defaultdict(lambda: Decimal("0"))
        request_ids: set[str] = set()
        failed_runs: set[str] = set()
        for event in events:
            grouped_quantity[event.category] += event.quantity
            request_ids.add(event.request_id)
            if event.success is False:
                failed_runs.add(event.run_id)
        lines = []
        for category, quantity in sorted(grouped_quantity.items(), key=lambda item: item[0].value):
            rate = self.rate_card.rate_for(category)
            lines.append(CostLine(category, quantity, rate.rate, money(quantity * rate.rate), rate.currency))
        total = money(sum((line.amount for line in lines), Decimal("0")))
        return UnitEconomicsReport(
            total_cost=total,
            request_count=len(request_ids),
            completed_task_count=len(set(completed_task_ids)),
            failed_run_count=len(failed_runs),
            document_count=len(set(document_ids)),
            human_escalation_count=len(set(human_escalation_ids)),
            lines=tuple(lines),
        )


def failed_run_cost(events: Iterable[CostEvent], calculator: CostCalculator) -> Decimal:
    failed_ids = {event.run_id for event in events if event.success is False}
    return money(sum((calculator.price_event(event).amount for event in events if event.run_id in failed_ids), Decimal("0")))


def retry_cost(events: Iterable[CostEvent], calculator: CostCalculator) -> Decimal:
    return money(sum((calculator.price_event(event).amount for event in events if event.retry), Decimal("0")))


def human_escalation_cost(minutes: Decimal, loaded_hourly_rate: Decimal, queue_overhead: Decimal = Decimal("0")) -> Decimal:
    if minutes < 0 or loaded_hourly_rate < 0 or queue_overhead < 0:
        raise ValueError("human review cost inputs must be non-negative")
    return money((minutes / Decimal("60")) * loaded_hourly_rate + queue_overhead)
