from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    p = Path(path)
    with p.open('r', encoding='utf-8') as fh:
        return json.load(fh)


def write_json(path: str | Path, value: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')
