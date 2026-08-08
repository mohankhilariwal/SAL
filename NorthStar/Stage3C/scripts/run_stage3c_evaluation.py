from __future__ import annotations

import json
import tempfile
from pathlib import Path

from northstar_compliance.agent.decision import DeterministicDecisionProvider, FlakyDecisionProvider
from northstar_compliance.agent.models import AgentGoal, RuntimeBudget
from northstar_compliance.agent.runtime import AgentRuntime
from northstar_compliance.state.checkpoint import LocalCheckpointStore
from northstar_compliance.tools.gateway import Principal, ToolGateway
from northstar_compliance.tools.local_tools import FailureInjector, LocalStores, NorthStarLocalTools


def build(path, plans=None, providers=None):
    stores = LocalStores()
    primary = NorthStarLocalTools(stores=stores, failures=FailureInjector(plans))
    fallback = NorthStarLocalTools(stores=stores, fallback=True)
    gateway = ToolGateway(
        {f"TOOL-{i:03d}": primary.adapter for i in range(1, 7)},
        {f"TOOL-{i:03d}": fallback.adapter for i in range(1, 4)},
    )
    return AgentRuntime(gateway, providers or [DeterministicDecisionProvider()], LocalCheckpointStore(path), reconciler=primary.reconcile)

results = {}
with tempfile.TemporaryDirectory() as td:
    goal = AgentGoal("GOAL-EVAL", "PUB-EVAL", "Prepare package")
    principal = Principal("maya.chen")

    results["EVAL-022"] = build(Path(td)/"happy").run(goal, principal).to_dict()
    results["EVAL-023"] = build(Path(td)/"fallback", {"TOOL-001": ["transient"]}).run(goal, principal).to_dict()
    results["EVAL-024"] = build(Path(td)/"write", {"TOOL-004": ["timeout_after_commit"]}).run(goal, principal).to_dict()
    providers = [FlakyDecisionProvider(DeterministicDecisionProvider()), DeterministicDecisionProvider()]
    results["EVAL-025"] = build(Path(td)/"model", providers=providers).run(goal, principal).to_dict()
    results["EVAL-026"] = build(Path(td)/"budget").run(goal, principal, budget=RuntimeBudget(max_tool_calls=2)).to_dict()

Path("Stage-3C-Evaluation-Report.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps({k: {"status": v["status"], "reason": v["termination_reason"]} for k,v in results.items()}, indent=2))
