from __future__ import annotations

import json
from pathlib import Path

from northstar_compliance.agent.factory import build_local_runtime
from northstar_compliance.agent.models import AgentGoal
from northstar_compliance.tools.gateway import Principal

out = Path("examples/stage3c-output")
out.mkdir(parents=True, exist_ok=True)
runtime, _, _ = build_local_runtime(out)
outcome = runtime.run(
    AgentGoal("GOAL-001", "PUB-NS-2026-017", "Prepare an evidence-backed unapproved impact package and queue human review."),
    Principal("maya.chen"),
)
(out / "outcome.json").write_text(json.dumps(outcome.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(outcome.to_dict(), indent=2, sort_keys=True))
