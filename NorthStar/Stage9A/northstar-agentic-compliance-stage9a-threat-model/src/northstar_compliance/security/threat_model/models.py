from __future__ import annotations
from dataclasses import dataclass
from typing import Any

STRIDE = {"Spoofing", "Tampering", "Repudiation", "Information Disclosure", "Denial of Service", "Elevation of Privilege"}
OWASP_ASI = {f"ASI{i:02d}" for i in range(1, 11)}


class ValidationError(ValueError):
    pass


@dataclass(frozen=True)
class Score:
    likelihood: int
    impact: int

    @property
    def value(self) -> int:
        return self.likelihood * self.impact

    def validate(self) -> None:
        if self.likelihood not in range(1, 6) or self.impact not in range(1, 6):
            raise ValidationError("likelihood and impact must be integers from 1 to 5")


@dataclass(frozen=True)
class Threat:
    risk_id: str
    title: str
    actor_id: str
    entry_flows: tuple[str, ...]
    stride: tuple[str, ...]
    owasp: str
    family: str
    inherent: Score
    residual: Score
    scope: str
    controls: tuple[str, ...]
    authority_effect: str

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "Threat":
        obj = cls(
            risk_id=row["risk_id"], title=row["title"], actor_id=row["actor_id"],
            entry_flows=tuple(row["entry_flows"]), stride=tuple(row["stride"]),
            owasp=row["owasp_agentic_top10"], family=row["threat_family"],
            inherent=Score(row["inherent_likelihood"], row["inherent_impact"]),
            residual=Score(row["residual_likelihood"], row["residual_impact"]),
            scope=row["scope"], controls=tuple(row["controls"]),
            authority_effect=row["authority_effect"],
        )
        obj.validate()
        return obj

    def validate(self) -> None:
        if not self.risk_id.startswith("RSK-"):
            raise ValidationError("invalid risk id")
        if not self.stride or not set(self.stride).issubset(STRIDE):
            raise ValidationError(f"invalid STRIDE categories for {self.risk_id}")
        if self.owasp not in OWASP_ASI:
            raise ValidationError(f"invalid OWASP ASI mapping for {self.risk_id}")
        self.inherent.validate(); self.residual.validate()
        if self.scope not in {"current", "future"}:
            raise ValidationError("scope must be current or future")
        if self.authority_effect != "none":
            raise ValidationError("threat evidence cannot grant authority")
        if not self.controls:
            raise ValidationError("every threat needs at least one control")
