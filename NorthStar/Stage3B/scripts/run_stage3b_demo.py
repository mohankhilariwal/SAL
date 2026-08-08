from __future__ import annotations

import json
import os
from pathlib import Path

from northstar_compliance.agent.factory import build_agent_runtime, default_goal, default_principal


def main() -> None:
    root = Path(__file__).parents[1]
    artifact_root = Path(os.environ.get("NORTHSTAR_ARTIFACT_DIR", root / "examples" / "stage3b-output"))
    runtime = build_agent_runtime(root, artifact_root)
    state, outcome, path = runtime.run(default_goal(), default_principal())
    print(json.dumps(outcome.to_dict(), indent=2))
    print(f"run_artifact={path}")
    print(f"decisions={len(state.decisions)} observations={len(state.observations)}")


if __name__ == "__main__":
    main()
