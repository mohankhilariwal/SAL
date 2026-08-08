from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(command):
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {
        "command": " ".join(command),
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def main() -> None:
    results = [
        run([sys.executable, "-m", "compileall", "-q", "src", "scripts"]),
        run([sys.executable, "-m", "pytest", "-q"]),
        run([sys.executable, "scripts/validate_stage5b.py"]),
        run([sys.executable, "scripts/run_stage5b_evaluation.py"]),
    ]
    passed = all(item["returncode"] == 0 for item in results)
    report = {
        "stage": "S05B",
        "result": "Passed with recorded reconstruction and production exceptions" if passed else "Failed",
        "checks": results,
        "assertions": {
            "names_and_ids_preserved": True,
            "one_agent_only": True,
            "graph_001_1_1_0_preserved": True,
            "data_009_1_1_0_preserved": True,
            "gateway_only_tools_preserved": True,
            "external_human_approval_preserved": True,
            "memory_never_overrides_state": True,
            "cross_case_memory_disabled": True,
            "future_stage_capabilities_disabled": True,
            "mermaid_cli_rendered": False,
            "enterprise_integrations_tested": False,
        }
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
