from __future__ import annotations

from dataclasses import asdict
from enum import Enum
import json
from pathlib import Path
from typing import Any

from .models import DeploymentKind, InferenceDeploymentProfile, WorkloadSignal


class _Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)


def load_workload(path: str | Path) -> WorkloadSignal:
    return WorkloadSignal(**json.loads(Path(path).read_text(encoding="utf-8")))


def load_deployment(path: str | Path) -> InferenceDeploymentProfile:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    data["kind"] = DeploymentKind(data["kind"])
    return InferenceDeploymentProfile(**data)


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, tuple):
        return [to_jsonable(item) for item in value]
    return value


def write_json(path: str | Path, value: Any) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(to_jsonable(value), cls=_Encoder, indent=2, sort_keys=True) + "\n", encoding="utf-8")
