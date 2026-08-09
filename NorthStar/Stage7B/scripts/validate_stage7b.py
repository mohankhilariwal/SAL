#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import py_compile

from northstar_compliance.workload.io import load_profile, load_service_model


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    profiles = sorted((root / "config/workloads").glob("WP-*.json"))
    assert len(profiles) == 8, f"expected 8 profiles, found {len(profiles)}"
    loaded = [load_profile(path) for path in profiles]
    assert len({profile.profile_id for profile in loaded}) == len(loaded)
    assert sum(profile.status != "inactive_future" for profile in loaded) == 7
    assert any(profile.status == "inactive_future" for profile in loaded)
    load_service_model(root / "config/workloads/service-model-local.json")
    for path in (root / "src").rglob("*.py"):
        py_compile.compile(str(path), doraise=True)
    for path in (root / "schemas").glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    print("Stage 7B structural validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
