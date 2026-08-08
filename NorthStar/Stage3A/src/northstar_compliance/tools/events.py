from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from threading import Lock

from .models import ToolExecutionEvent


class JsonlToolEventWriter:
    """Local execution evidence only; not a tamper-evident enterprise audit ledger."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self.events: list[ToolExecutionEvent] = []
        self._lock = Lock()
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: ToolExecutionEvent) -> None:
        with self._lock:
            self.events.append(event)
            if self.path is not None:
                with self.path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(asdict(event), sort_keys=True, ensure_ascii=False) + "\n")
