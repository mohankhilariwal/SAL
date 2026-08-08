from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import Any


class LocalToolStore:
    """Local tutorial store. It is not an enterprise case or records system."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self.write_counts: dict[str, int] = {"cases": 0, "mappings": 0, "reviews": 0}

    def _collection(self, name: str) -> Path:
        path = self.root / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _path(self, collection: str, record_id: str) -> Path:
        if not record_id or any(token in record_id for token in ("/", "\\", "..")):
            raise ValueError("invalid record identifier")
        return self._collection(collection) / f"{record_id}.json"

    def write_once(self, collection: str, record_id: str, value: dict[str, Any]) -> bool:
        path = self._path(collection, record_id)
        with self._lock:
            if path.exists():
                return False
            temp = path.with_suffix(".json.tmp")
            temp.write_text(
                json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            os.replace(temp, path)
            self.write_counts[collection] += 1
            return True

    def read(self, collection: str, record_id: str) -> dict[str, Any] | None:
        path = self._path(collection, record_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list(self, collection: str) -> list[dict[str, Any]]:
        return [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(self._collection(collection).glob("*.json"))
        ]
