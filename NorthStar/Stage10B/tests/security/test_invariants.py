from dataclasses import fields

from northstar_compliance.reliability.models import FailureEnvelope, RecoveryDecision, ReleaseManifest


def test_reliability_objects_have_no_authority_effect():
    for cls in (FailureEnvelope, RecoveryDecision, ReleaseManifest):
        assert "authority_effect" in {f.name for f in fields(cls)}


def test_no_new_tool_identifier_in_source_tree():
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    text = "\n".join(p.read_text(errors="ignore") for p in (root / "src").rglob("*.py"))
    assert "TOOL-007" not in text


def test_no_route_activation_true_in_config():
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    text = "\n".join(p.read_text(errors="ignore") for p in (root / "config").rglob("*.json"))
    assert '"enabled": true' not in text


def test_checkpoint_docstring_denies_business_replay():
    from northstar_compliance.reliability.checkpoint import CheckpointStore
    assert "never writes to\nDATA-106" in CheckpointStore.__doc__
