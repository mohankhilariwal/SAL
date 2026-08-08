from __future__ import annotations

import json
import tempfile
from pathlib import Path

from northstar_compliance.agent.decision import ScriptedDecisionProvider
from northstar_compliance.agent.factory import build_agent_runtime, default_goal, default_principal
from northstar_compliance.agent.models import AgentDecision, DecisionKind


def run_case(root: Path, name: str, provider=None, **kwargs):
    with tempfile.TemporaryDirectory(prefix=f"northstar-{name}-") as td:
        runtime = build_agent_runtime(root, Path(td), provider)
        state, outcome, _ = runtime.run(default_goal(), default_principal(), **kwargs)
        return {
            "case": name,
            "status": outcome.status.value,
            "termination_reason": outcome.termination_reason.value,
            "iterations": outcome.iterations,
            "milestones": len(outcome.progress_milestones),
            "tool_observations": len(state.observations),
        }


def main() -> None:
    root = Path(__file__).parents[1]
    early = ScriptedDecisionProvider([AgentDecision(DecisionKind.COMPLETE, "Done.", "Stop.")])
    explicit = ScriptedDecisionProvider([AgentDecision(DecisionKind.ESCALATE, "Ambiguous source identity.", "Return to Maya.")])
    results = [
        run_case(root, "happy_path"),
        run_case(root, "early_completion", early),
        run_case(root, "explicit_escalation", explicit),
        run_case(root, "iteration_guard", max_iterations=1),
    ]
    print(json.dumps({"schema_version": "1.0.0", "evaluations": results}, indent=2))


if __name__ == "__main__":
    main()
