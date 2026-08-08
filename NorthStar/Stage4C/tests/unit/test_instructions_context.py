from dataclasses import replace
import pytest

from northstar_compliance.harness.context import ContextAssembler, ContextAssemblyError, ContextSource
from northstar_compliance.harness.instructions import InstructionError, InstructionStore


def test_161_instruction_hash_is_verified(harness, tmp_path):
    bundle = harness.instructions.load()
    assert bundle.critical_controls_external is True
    path = tmp_path / "instruction.txt"
    path.write_text("tampered", encoding="utf-8")
    bad = InstructionStore(path, name=bundle.instruction_name, version=bundle.instruction_version, expected_sha256=bundle.content_sha256)
    with pytest.raises(InstructionError, match="instruction_hash_mismatch"):
        bad.load()


def test_162_access_is_checked_before_context_loader(now):
    touched = {"value": False}
    def loader():
        touched["value"] = True
        return "forbidden"
    source = ContextSource("SECRET-1", "evidence", "RESTRICTED", "analysis", False, 1, loader)
    envelope = ContextAssembler().assemble(agent_id="AGT-001", sources=[source], now=now)
    assert touched["value"] is False
    assert envelope.items == ()
    assert envelope.omitted_source_ids == ("SECRET-1",)


def test_163_memory_context_is_rejected(now):
    source = ContextSource("MEM-1", "memory", "INTERNAL", "analysis", True, 1, lambda: "memory")
    with pytest.raises(ContextAssemblyError, match="memory_not_enabled"):
        ContextAssembler().assemble(agent_id="AGT-001", sources=[source], now=now)


def test_164_context_budget_is_deterministic(now):
    sources = [
        ContextSource("A", "evidence", "INTERNAL", "analysis", True, 2, lambda: "BBBB"),
        ContextSource("B", "evidence", "INTERNAL", "analysis", True, 1, lambda: "AAAAAA"),
    ]
    assembler = ContextAssembler(max_items=2, max_characters=7)
    envelope = assembler.assemble(agent_id="AGT-001", sources=sources, now=now)
    assert [x.source_id for x in envelope.items] == ["B", "A"]
    assert envelope.items[1].content == "B"
    assert envelope.total_characters == 7
