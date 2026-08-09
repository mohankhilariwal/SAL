from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        ROOT / "docs/stages/Stage-6B-Bounded-Agent-Handoff-Communication-and-Authority-Contracts.md",
        ROOT / "docs/source-of-truth/09-Stage-Handoff-Pack.md",
        ROOT / "config/architecture/handoff-policy-v1.json",
        ROOT / "config/agents/candidate-endpoints-v1.json",
    ]
    required.extend(ROOT.glob("schemas/DATA-09*.schema.json"))
    failures = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    policy = json.loads((ROOT / "config/architecture/handoff-policy-v1.json").read_text())
    if policy["active_agent_ids"] != ["AGT-001"]:
        failures.append("active_agent_inventory_changed")
    for flag in ("concurrent_execution", "protocol_selected", "mcp_enabled", "a2a_enabled", "shared_mutable_state", "shared_agent_memory"):
        if policy[flag] is not False:
            failures.append(f"future_capability_enabled:{flag}")
    text = "PASSED\n" if not failures else "FAILED\n" + "\n".join(failures) + "\n"
    (ROOT / "reports/Stage-6B-Validation-Report.txt").write_text(text)
    print(text, end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
