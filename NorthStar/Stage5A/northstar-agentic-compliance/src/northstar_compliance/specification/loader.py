from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .canonical import sha256_digest
from .models import AgentSpecification


class AgentSpecificationStore:
    """Loads one immutable, repository-controlled agent specification."""

    def __init__(self, path: Path):
        self._path = path

    def load(self) -> AgentSpecification:
        if not self._path.is_file():
            raise FileNotFoundError(f"specification_not_found:{self._path}")
        raw_text = self._path.read_text(encoding="utf-8")
        if not raw_text.strip():
            raise ValueError("empty_agent_specification")
        value: Any = json.loads(raw_text)
        if not isinstance(value, dict):
            raise ValueError("agent_specification_must_be_object")
        return AgentSpecification(raw=value, digest=sha256_digest(value))
