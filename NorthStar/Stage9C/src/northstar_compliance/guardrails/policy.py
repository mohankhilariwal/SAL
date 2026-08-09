from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .canonical import sha256_digest
from .models import GuardrailStage, Outcome


@dataclass(frozen=True)
class GuardrailControl:
    control_id: str
    name: str
    stage: GuardrailStage
    validator: str
    hard: bool
    synchronous: bool
    overrideable: bool
    model_assisted: bool
    outcome_on_fail: Outcome
    parameters: dict[str, Any]
    owner: str


@dataclass(frozen=True)
class PolicyBundle:
    bundle_id: str
    version: str
    status: str
    effective_at: str
    expires_at: str
    controls: tuple[GuardrailControl, ...]
    digest: str

    @classmethod
    def load(cls, path: str | Path) -> "PolicyBundle":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        controls = tuple(
            GuardrailControl(
                control_id=item["control_id"],
                name=item["name"],
                stage=GuardrailStage(item["stage"]),
                validator=item["validator"],
                hard=bool(item["hard"]),
                synchronous=bool(item["synchronous"]),
                overrideable=bool(item["overrideable"]),
                model_assisted=bool(item.get("model_assisted", False)),
                outcome_on_fail=Outcome(item["outcome_on_fail"]),
                parameters=dict(item.get("parameters", {})),
                owner=item["owner"],
            )
            for item in raw["controls"]
        )
        payload = {k: v for k, v in raw.items() if k != "digest"}
        bundle = cls(
            bundle_id=raw["bundle_id"],
            version=raw["version"],
            status=raw["status"],
            effective_at=raw["effective_at"],
            expires_at=raw["expires_at"],
            controls=controls,
            digest=sha256_digest(payload),
        )
        bundle.validate()
        return bundle

    def validate(self) -> None:
        seen: set[str] = set()
        for control in self.controls:
            if control.control_id in seen:
                raise ValueError(f"duplicate control_id: {control.control_id}")
            seen.add(control.control_id)
            if control.hard and control.overrideable:
                raise ValueError(f"hard control cannot be overrideable: {control.control_id}")
            if control.hard and not control.synchronous:
                raise ValueError(f"hard control must be synchronous: {control.control_id}")
            if control.hard and control.model_assisted:
                raise ValueError(f"model-assisted control cannot be the sole hard control: {control.control_id}")
            if control.outcome_on_fail is Outcome.ALLOW:
                raise ValueError(f"failure outcome cannot be allow: {control.control_id}")

    def controls_for(self, stage: GuardrailStage) -> tuple[GuardrailControl, ...]:
        return tuple(c for c in self.controls if c.stage is stage)
