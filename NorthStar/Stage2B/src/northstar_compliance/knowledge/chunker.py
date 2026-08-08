from __future__ import annotations

from hashlib import sha256
import re

from .schemas import KnowledgeChunk, KnowledgeSourceDescriptor, SCHEMA_VERSION

CHUNKER_VERSION = "northstar-markdown-line-window-v1"
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _chunk_id(source_version_id: str, start: int, end: int, text: str) -> str:
    material = f"{source_version_id}|{start}|{end}|{text}".encode("utf-8")
    return "CHK-" + sha256(material).hexdigest()[:20].upper()


def chunk_document(
    descriptor: KnowledgeSourceDescriptor,
    source_version_id: str,
    normalized_sha256: str,
    lines: tuple[str, ...],
    risk_flags: tuple[str, ...],
    window_lines: int = 6,
    overlap_lines: int = 1,
) -> tuple[KnowledgeChunk, ...]:
    if window_lines < 1 or overlap_lines < 0 or overlap_lines >= window_lines:
        raise ValueError("invalid chunking policy")
    sections: list[tuple[tuple[str, ...], int, int]] = []
    path: list[str] = []
    section_start = 1
    current_path: tuple[str, ...] = ()
    for i, line in enumerate(lines, start=1):
        match = HEADING.match(line)
        if match:
            if i > section_start:
                sections.append((current_path, section_start, i - 1))
            level = len(match.group(1))
            path = path[: level - 1]
            path.append(match.group(2))
            current_path = tuple(path)
            section_start = i
    if lines:
        sections.append((current_path, section_start, len(lines)))

    chunks: list[KnowledgeChunk] = []
    for heading_path, section_start, section_end in sections:
        start = section_start
        while start <= section_end:
            end = min(section_end, start + window_lines - 1)
            text = "\n".join(lines[start - 1 : end])
            if text.strip():
                chunks.append(
                    KnowledgeChunk(
                        schema_version=SCHEMA_VERSION,
                        source_id=descriptor.source_id,
                        source_version_id=source_version_id,
                        chunk_id=_chunk_id(source_version_id, start, end, text),
                        title=descriptor.title,
                        source_type=descriptor.source_type,
                        owner=descriptor.owner,
                        version_label=descriptor.version_label,
                        authoritative=descriptor.authoritative,
                        effective_from=descriptor.effective_from,
                        effective_to=descriptor.effective_to,
                        jurisdictions=descriptor.jurisdictions,
                        business_domains=descriptor.business_domains,
                        access=descriptor.access,
                        heading_path=heading_path,
                        line_start=start,
                        line_end=end,
                        text=text,
                        text_sha256=sha256(text.encode("utf-8")).hexdigest(),
                        normalized_source_sha256=normalized_sha256,
                        risk_flags=risk_flags,
                    )
                )
            if end == section_end:
                break
            start = end - overlap_lines + 1
    return tuple(chunks)
