from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from .schemas import KnowledgeError

PARSER_VERSION = "northstar-text-parser-1.0.0"
_ALLOWED_SUFFIXES = {".txt", ".md"}
_SUSPICIOUS_PATTERNS = {
    "indirect_prompt_instruction": re.compile(
        r"\b(ignore|disregard|override)\b.{0,40}\b(instruction|system|policy|prompt)\b",
        re.IGNORECASE,
    ),
    "model_or_tool_directive": re.compile(
        r"\b(system prompt|developer message|tool call|function call|execute code)\b",
        re.IGNORECASE,
    ),
    "credential_request": re.compile(
        r"\b(api key|password|secret token|access token|private key)\b",
        re.IGNORECASE,
    ),
}


@dataclass(frozen=True, slots=True)
class ParsedDocument:
    raw_bytes: bytes
    normalized_text: str
    lines: tuple[str, ...]
    raw_sha256: str
    normalized_sha256: str
    risk_flags: tuple[str, ...]


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve_bounded_path(root: Path, relative_path: str) -> Path:
    if Path(relative_path).is_absolute():
        raise KnowledgeError("absolute source paths are prohibited")
    resolved_root = root.resolve()
    candidate = (resolved_root / relative_path).resolve()
    if not candidate.is_relative_to(resolved_root):
        raise KnowledgeError("source path escapes the approved corpus root")
    if candidate.is_symlink():
        raise KnowledgeError("symbolic-link sources are prohibited")
    return candidate


def parse_text_document(path: Path, *, max_bytes: int = 2_000_000) -> ParsedDocument:
    suffix = path.suffix.lower()
    if suffix not in _ALLOWED_SUFFIXES:
        raise KnowledgeError(f"unsupported source type: {suffix or '<none>'}")
    raw = path.read_bytes()
    if not raw:
        raise KnowledgeError("source document is empty")
    if len(raw) > max_bytes:
        raise KnowledgeError(f"source exceeds max_bytes={max_bytes}")
    if b"\x00" in raw:
        raise KnowledgeError("NUL byte detected; binary or malformed input rejected")
    try:
        decoded = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise KnowledgeError("source is not strict UTF-8") from exc

    # Normalize only line endings. Preserve all other characters for stable coordinates.
    normalized = decoded.replace("\r\n", "\n").replace("\r", "\n")
    lines = tuple(normalized.splitlines())
    flags = tuple(sorted(name for name, pattern in _SUSPICIOUS_PATTERNS.items() if pattern.search(normalized)))
    return ParsedDocument(
        raw_bytes=raw,
        normalized_text=normalized,
        lines=lines,
        raw_sha256=sha256_hex(raw),
        normalized_sha256=sha256_hex(normalized.encode("utf-8")),
        risk_flags=flags,
    )
