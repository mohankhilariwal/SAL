from dataclasses import replace
import pytest

from northstar_compliance.harness.validation import ValidationError


def test_159_manifest_binds_accepted_runtime(harness):
    assert harness.manifest.agent_id == "AGT-001"
    assert harness.manifest.graph_id == "GRAPH-001"
    assert harness.manifest.graph_version == "1.1.0"
    assert sorted(harness.manifest.tool_versions) == [f"TOOL-{i:03d}" for i in range(1, 7)]
    harness.validators.run("pre_start", harness.manifest)


def test_160_future_stage_flags_fail_closed(harness):
    bad = replace(harness.manifest, memory_enabled=True)
    with pytest.raises(ValidationError, match="future_stage_capability_enabled"):
        harness.validators.run("pre_start", bad)
