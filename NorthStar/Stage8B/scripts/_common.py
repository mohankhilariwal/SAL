from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets/evaluation/judge-calibration/v1.0.0"
CONFIG = ROOT / "config/evaluation/judges/JUDGE-POLICY-001.json"
REPORTS = ROOT / "reports"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_report(name: str, value) -> Path:
    REPORTS.mkdir(exist_ok=True)
    path = REPORTS / name
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
