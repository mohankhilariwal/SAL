from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from enum import StrEnum
from typing import Mapping

MONEY_QUANTUM = Decimal("0.000001")


def money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


class CostCategory(StrEnum):
    MODEL_INPUT = "model_input_tokens"
    MODEL_OUTPUT = "model_output_tokens"
    MODEL_REASONING = "model_reasoning_tokens"
    EMBEDDING = "embedding_tokens"
    RERANKING = "reranking_units"
    TOOL = "tool_calls"
    COMPUTE = "compute_seconds"
    STORAGE = "storage_gb_month"
    NETWORK = "network_gb"
    OBSERVABILITY = "observability_gb"
    EVALUATION = "evaluation_cases"
    HUMAN_REVIEW = "human_review_minutes"
    SECURITY = "security_control_units"
    RECOVERY = "recovery_minutes"


@dataclass(frozen=True)
class CostRate:
    category: CostCategory
    rate: Decimal
    unit: str
    currency: str = "CAD"
    assumption: bool = True

    def __post_init__(self) -> None:
        if self.rate < 0:
            raise ValueError("rate must be non-negative")
        if self.currency != "CAD":
            raise ValueError("Stage 10C example is denominated in CAD")


@dataclass(frozen=True)
class CostEvent:
    run_id: str
    request_id: str
    category: CostCategory
    quantity: Decimal
    unit: str
    workload_profile_id: str
    business_unit: str
    jurisdiction: str
    environment: str
    case_id: str | None = None
    success: bool | None = None
    retry: bool = False
    recovered: bool = False
    metadata: Mapping[str, str] = field(default_factory=dict)
    authority_effect: str = "none"

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("quantity must be non-negative")
        if self.authority_effect != "none":
            raise ValueError("cost events cannot create authority")


@dataclass(frozen=True)
class CostLine:
    category: CostCategory
    quantity: Decimal
    unit_rate: Decimal
    amount: Decimal
    currency: str = "CAD"


@dataclass(frozen=True)
class UnitEconomicsReport:
    total_cost: Decimal
    request_count: int
    completed_task_count: int
    failed_run_count: int
    document_count: int
    human_escalation_count: int
    lines: tuple[CostLine, ...]
    currency: str = "CAD"
    authority_effect: str = "none"

    @property
    def cost_per_request(self) -> Decimal | None:
        return None if self.request_count == 0 else money(self.total_cost / self.request_count)

    @property
    def cost_per_completed_task(self) -> Decimal | None:
        return None if self.completed_task_count == 0 else money(self.total_cost / self.completed_task_count)

    @property
    def cost_per_document(self) -> Decimal | None:
        return None if self.document_count == 0 else money(self.total_cost / self.document_count)
