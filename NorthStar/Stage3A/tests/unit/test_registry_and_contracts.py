from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from northstar_compliance.tools.models import ImpactClass
from northstar_compliance.tools.registry import ToolRegistry, ToolRegistryError


def test_047_all_descriptors_validate_and_hash(repo_root):
    registry = ToolRegistry.load(repo_root / "config" / "tools")
    descriptors = registry.all()
    assert len(descriptors) == 6
    assert {d.tool_id for d in descriptors} == {f"TOOL-{i:03d}" for i in range(1, 7)}
    assert all(len(d.descriptor_hash) == 64 for d in descriptors)
    assert all(d.schema_version == "1.0.0" for d in descriptors)


def test_048_input_and_output_schemas_are_draft_2020_12(repo_root):
    registry = ToolRegistry.load(repo_root / "config" / "tools")
    for descriptor in registry.all():
        assert descriptor.input_schema["$schema"].endswith("2020-12/schema")
        assert descriptor.output_schema["$schema"].endswith("2020-12/schema")
        Draft202012Validator.check_schema(descriptor.input_schema)
        Draft202012Validator.check_schema(descriptor.output_schema)
        assert descriptor.input_schema["additionalProperties"] is False
        assert descriptor.output_schema["additionalProperties"] is False


def test_049_exact_version_resolution_and_unknown_rejection(repo_root):
    registry = ToolRegistry.load(repo_root / "config" / "tools")
    assert registry.resolve("TOOL-001", "1.0.0").name == "search_regulatory_catalogue"
    with pytest.raises(ToolRegistryError, match="version mismatch"):
        registry.resolve("TOOL-001", "9.9.9")
    with pytest.raises(ToolRegistryError, match="unknown tool"):
        registry.resolve("TOOL-999", "1.0.0")


def test_050_stage3a_registers_only_read_or_reversible_tools(repo_root):
    registry = ToolRegistry.load(repo_root / "config" / "tools")
    assert {d.impact_class for d in registry.all()} == {
        ImpactClass.READ_ONLY,
        ImpactClass.REVERSIBLE_WRITE,
    }
    for descriptor in registry.all():
        if descriptor.impact_class == ImpactClass.REVERSIBLE_WRITE:
            assert descriptor.idempotency_required is True
            assert descriptor.retry_policy.max_attempts == 1


def test_051_descriptor_hash_changes_on_contract_change(repo_root):
    path = repo_root / "config" / "tools" / "TOOL-001-search_regulatory_catalogue.json"
    raw = json.loads(path.read_text())
    registry = ToolRegistry.load(repo_root / "config" / "tools")
    original = registry.resolve("TOOL-001", "1.0.0").descriptor_hash
    raw["description"] += " Changed."
    from northstar_compliance.tools.utils import sha256_json
    assert sha256_json(raw) != original
