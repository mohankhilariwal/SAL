from pathlib import Path

from northstar_compliance.agent.factory import build_agent_runtime, default_goal, default_principal
from northstar_compliance.agent.models import RunStatus


def test_test086_termination_accuracy_evaluation(tmp_path: Path):
    root = Path(__file__).parents[2]
    runtime = build_agent_runtime(root, tmp_path)
    state, outcome, _ = runtime.run(default_goal(), default_principal())
    assert outcome.status == RunStatus.COMPLETED
    assert state.iteration == 7
    assert len(state.observations) == 6
    assert len(state.progress_milestones) == 6


def test_test087_no_graph_memory_or_multi_agent_modules(tmp_path: Path):
    root = Path(__file__).parents[2]
    src = root / "src" / "northstar_compliance"
    assert not (src / "graph").exists()
    assert not (src / "memory").exists()
    agent_ids = set()
    for path in src.rglob("*.py"):
        text = path.read_text()
        if "AGT-001" in text:
            agent_ids.add("AGT-001")
        assert "AGT-002" not in text
    assert agent_ids == {"AGT-001"}
