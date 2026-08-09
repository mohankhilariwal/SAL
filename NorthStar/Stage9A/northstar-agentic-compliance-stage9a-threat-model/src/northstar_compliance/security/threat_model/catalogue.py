from __future__ import annotations
from typing import Any


def current_threats(catalogue: dict[str, Any]) -> list[dict[str, Any]]:
    return [x for x in catalogue["scenarios"] if x["scope"] == "current"]


def future_threats(catalogue: dict[str, Any]) -> list[dict[str, Any]]:
    return [x for x in catalogue["scenarios"] if x["scope"] == "future"]


def by_risk_id(catalogue: dict[str, Any], risk_id: str) -> dict[str, Any]:
    for row in catalogue["scenarios"]:
        if row["risk_id"] == risk_id:
            return row
    raise KeyError(risk_id)
