from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from governed_release.application.scenarios import request_for_scenario
from governed_release.domain.enums import Scenario


def main() -> None:
    output = ROOT / "data" / "test_vectors" / "scenario_requests.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        scenario.value: request_for_scenario(scenario).model_dump(mode="json")
        for scenario in Scenario
    }
    output.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"Seeded four scenario request templates: {output}")


if __name__ == "__main__":
    main()
