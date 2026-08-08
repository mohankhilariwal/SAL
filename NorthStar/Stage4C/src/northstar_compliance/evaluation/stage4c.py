from __future__ import annotations

import json
from pathlib import Path


def count_trace_events(workspace_path: str | Path) -> int:
    path = Path(workspace_path) / "trace.jsonl"
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def trace_contains_sensitive_material(workspace_path: str | Path) -> bool:
    text = (Path(workspace_path) / "trace.jsonl").read_text(encoding="utf-8")
    lowered = text.lower()
    return any(term in lowered for term in ('"approval_token"', "chain_of_thought", "hidden_reasoning", '"authorization"'))


def read_trace(workspace_path: str | Path) -> list[dict]:
    path = Path(workspace_path) / "trace.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
