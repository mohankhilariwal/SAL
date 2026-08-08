from northstar_compliance.knowledge.chunker import ChunkingPolicy, StructureAwareLineChunker
from northstar_compliance.knowledge.schemas import (
    AccessScope,
    Classification,
    KnowledgeSourceDescriptor,
    SourceType,
)


def descriptor() -> KnowledgeSourceDescriptor:
    return KnowledgeSourceDescriptor(
        source_id="POL-999",
        title="Test policy",
        source_type=SourceType.POLICY,
        owner="Owner",
        relative_path="documents/test.md",
        version_label="1",
        effective_from="2026-01-01",
        effective_to=None,
        jurisdictions=("CA",),
        business_domains=("TEST",),
        access=AccessScope(Classification.INTERNAL, ("COMPLIANCE_ANALYST",)),
        retention_class="TEST",
    )


def test_chunker_is_deterministic_and_line_exact() -> None:
    lines = (
        "# A",
        "one",
        "two",
        "three",
        "## B",
        "four",
        "five",
    )
    chunker = StructureAwareLineChunker(ChunkingPolicy(max_chars=128, max_lines=3, overlap_lines=1))
    first = chunker.chunk(descriptor=descriptor(), source_version_id="KSV-ABC", lines=lines)
    second = chunker.chunk(descriptor=descriptor(), source_version_id="KSV-ABC", lines=lines)
    assert [item.chunk_id for item in first] == [item.chunk_id for item in second]
    for item in first:
        assert item.text == "\n".join(lines[item.line_start - 1 : item.line_end])
        assert item.line_end - item.line_start + 1 <= 3


def test_chunker_never_crosses_heading_sections() -> None:
    lines = ("# A", "a1", "a2", "# B", "b1", "b2")
    chunker = StructureAwareLineChunker(ChunkingPolicy(max_chars=128, max_lines=5, overlap_lines=1))
    chunks = chunker.chunk(descriptor=descriptor(), source_version_id="KSV-ABC", lines=lines)
    assert all(not (chunk.line_start <= 3 and chunk.line_end >= 4) for chunk in chunks)
    assert chunks[0].heading_path == ("A",)
    assert chunks[-1].heading_path == ("B",)


def test_chunk_coverage_has_no_nonempty_line_loss() -> None:
    lines = tuple(["# A"] + [f"line {i}" for i in range(1, 20)])
    chunker = StructureAwareLineChunker(ChunkingPolicy(max_chars=128, max_lines=5, overlap_lines=1))
    chunks = chunker.chunk(descriptor=descriptor(), source_version_id="KSV-ABC", lines=lines)
    covered = {line_no for chunk in chunks for line_no in range(chunk.line_start, chunk.line_end + 1)}
    assert covered == set(range(1, len(lines) + 1))
