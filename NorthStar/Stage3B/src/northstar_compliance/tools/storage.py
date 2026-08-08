from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


class LocalJsonStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _atomic_write(self, path: Path, data: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as tmp:
            json.dump(data, tmp, indent=2, sort_keys=True)
            tmp.write("\n")
            tmp.flush()
            os.fsync(tmp.fileno())
            temp_path = Path(tmp.name)
        os.replace(temp_path, path)

    def write_once(self, category: str, identifier: str, data: dict[str, Any]) -> dict[str, Any]:
        path = self.root / category / f"{identifier}.json"
        if path.exists():
            return json.loads(path.read_text())
        self._atomic_write(path, data)
        return data

    def write_run(self, run_id: str, data: dict[str, Any]) -> Path:
        path = self.root / "runs" / f"{run_id}.json"
        self._atomic_write(path, data)
        return path

    def append_event(self, event: dict[str, Any]) -> None:
        path = self.root / "events" / "tool-events.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
