from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterable

from .schemas import AccessScope, KnowledgeChunk, KnowledgeError, KnowledgeSourceDescriptor

CHUNKER_VERSION = "northstar-structure-line-chunker-1.0.0"
_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass(frozen=True, slots=True)
class ChunkingPolicy:
    max_chars: int = 1_200
    max_lines: int = 24
    overlap_lines: int = 2

    def __post_init__(self) -> None:
        if self.max_chars < 128:
            raise KnowledgeError("max_chars must be at least 128")
        if self.max_lines < 2:
            raise KnowledgeError("max_lines must be at least 2")
        if self.overlap_lines < 0 or self.overlap_lines >= self.max_lines:
            raise KnowledgeError("overlap_lines must be >=0 and < max_lines")


@dataclass(frozen=True, slots=True)
class _Section:
    start: int
    end: int
    heading_path: tuple[str, ...]


def _section_ranges(lines: tuple[str, ...]) -> list[_Section]:
    if not lines:
        return []
    sections: list[_Section] = []
    heading_stack: list[str] = []
    section_start = 1
    current_path: tuple[str, ...] = ()

    for line_no, line in enumerate(lines, start=1):
        match = _HEADING.match(line)
        if not match:
            continue
        if line_no > section_start:
            sections.append(_Section(section_start, line_no - 1, current_path))
        level = len(match.group(1))
        title = match.group(2).strip()
        heading_stack = heading_stack[: level - 1]
        heading_stack.append(title)
        current_path = tuple(heading_stack)
        section_start = line_no

    sections.append(_Section(section_start, len(lines), current_path))
    return [section for section in sections if section.end >= section.start]


def _chunk_hash(source_version_id: str, start: int, end: int, text: str) -> str:
    payload = f"{source_version_id}|{start}|{end}|".encode("utf-8") + text.encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class StructureAwareLineChunker:
    """Deterministic line-preserving chunker that never crosses Markdown sections."""

    def __init__(self, policy: ChunkingPolicy | None = None) -> None:
        self.policy = policy or ChunkingPolicy()

    def chunk(
        self,
        *,
        descriptor: KnowledgeSourceDescriptor,
        source_version_id: str,
        lines: tuple[str, ...],
        document_risk_flags: tuple[str, ...] = (),
    ) -> list[KnowledgeChunk]:
        chunks: list[KnowledgeChunk] = []
        ordinal = 1
        for section in _section_ranges(lines):
            cursor = section.start
            while cursor <= section.end:
                end = cursor - 1
                selected: list[str] = []
                while end < section.end:
                    candidate = lines[end]
                    candidate_text = "\n".join([*selected, candidate])
                    candidate_line_count = len(selected) + 1
                    if selected and (
                        candidate_line_count > self.policy.max_lines
                        or len(candidate_text) > self.policy.max_chars
                    ):
                        break
                    selected.append(candidate)
                    end += 1
                    if candidate_line_count >= self.policy.max_lines or len(candidate_text) >= self.policy.max_chars:
                        break

                if not selected:
                    # One oversize line is retained rather than dropped; validation flags the limit exception.
                    selected = [lines[cursor - 1]]
                    end = cursor

                text = "\n".join(selected)
                digest = _chunk_hash(source_version_id, cursor, end, text)
                risk_flags = list(document_risk_flags)
                if len(text) > self.policy.max_chars:
                    risk_flags.append("oversize_single_line")
                chunk = KnowledgeChunk(
                    chunk_id=f"CHK-{digest[:20].upper()}",
                    source_id=descriptor.source_id,
                    source_version_id=source_version_id,
                    ordinal=ordinal,
                    heading_path=section.heading_path,
                    line_start=cursor,
                    line_end=end,
                    char_count=len(text),
                    content_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    text=text,
                    access=descriptor.access,
                    jurisdictions=descriptor.jurisdictions,
                    business_domains=descriptor.business_domains,
                    effective_from=descriptor.effective_from,
                    effective_to=descriptor.effective_to,
                    risk_flags=tuple(sorted(set(risk_flags))),
                )
                chunks.append(chunk)
                ordinal += 1

                if end >= section.end:
                    break
                next_cursor = end - self.policy.overlap_lines + 1
                if next_cursor <= cursor:
                    next_cursor = cursor + 1
                cursor = next_cursor

        return chunks

    def policy_dict(self) -> dict[str, int | str]:
        return {
            "chunker_version": CHUNKER_VERSION,
            "max_chars": self.policy.max_chars,
            "max_lines": self.policy.max_lines,
            "overlap_lines": self.policy.overlap_lines,
        }
