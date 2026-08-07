from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .intake import Publication


@dataclass(frozen=True)
class ModelResult:
    provider: str
    model: str
    payload: dict[str, Any]
    usage: dict[str, int]


class SummaryModel(Protocol):
    provider: str
    model: str

    def summarize(self, publication: Publication) -> ModelResult:
        """Return provider payload matching the Stage 1 model schema."""
        ...
