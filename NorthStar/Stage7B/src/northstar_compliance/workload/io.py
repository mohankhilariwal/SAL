from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from .models import (
    ArrivalKind,
    ArrivalPattern,
    DistributionBucket,
    ServiceDemandModel,
    SLOHypothesis,
    WorkloadProfile,
)


def load_profile(path: str | Path) -> WorkloadProfile:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    buckets = tuple(DistributionBucket(**bucket) for bucket in data["buckets"])
    arrival_data = dict(data["arrival"])
    arrival_data["kind"] = ArrivalKind(arrival_data["kind"])
    return WorkloadProfile(
        profile_id=data["profile_id"],
        name=data["name"],
        version=data["version"],
        tokenizer_id=data["tokenizer_id"],
        status=data["status"],
        description=data["description"],
        buckets=buckets,
        arrival=ArrivalPattern(**arrival_data),
        slo=SLOHypothesis(**data["slo"]),
        context_growth_per_turn=data.get("context_growth_per_turn", 0.0),
        turns_min=data.get("turns_min", 1),
        turns_mode=data.get("turns_mode", 1),
        turns_max=data.get("turns_max", 1),
        capture_payloads=data.get("capture_payloads", False),
        metadata=data.get("metadata", {}),
    )


def load_service_model(path: str | Path) -> ServiceDemandModel:
    return ServiceDemandModel(**json.loads(Path(path).read_text(encoding="utf-8")))


def write_json(path: str | Path, value: Any) -> None:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
