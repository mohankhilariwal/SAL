"""Version-stamped request logging (JSONL). Feeds the control-plane curation
loop, regression diffs, and calibration fitting. Swap for Postgres in prod."""
from __future__ import annotations
import json, os, time
from pathlib import Path

LOG_DIR = Path(os.environ.get("SPINCHECK_LOG_DIR", "logs"))

def log_request(resp_dict: dict, text_len: int) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    rec = {"ts": time.time(), "text_len": text_len, **resp_dict}
    rec.pop("analysis", None)  # PII-minimal by default; enable full logging per env
    with (LOG_DIR / "requests.jsonl").open("a") as f:
        f.write(json.dumps(rec) + "\n")
