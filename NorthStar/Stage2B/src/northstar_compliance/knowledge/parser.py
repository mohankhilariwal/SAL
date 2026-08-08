from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re

PARSER_VERSION = "northstar-text-parser-v1"
SUPPORTED_SUFFIXES = {".txt", ".md"}
RISK_PATTERNS = {
    "INSTRUCTION_LIKE_CONTENT": re.compile(r"(?i)ignore (all|any|previous)|system prompt|developer message"),
    "CREDENTIAL_SEEKING_CONTENT": re.compile(r"(?i)password|api key|secret token|credential"),
}


@dataclass(frozen=True)
class ParsedDocument:
    raw_bytes: bytes
    normalized_text: str
    lines: tuple[str, ...]
    raw_sha256: str
    normalized_sha256: str
    risk_flags: tuple[str, ...]


def resolve_bounded(root: Path, relative_path: str) -> Path:
    root = root.resolve()
    target = (root / relative_path).resolve()
    if target != root and root not in target.parents:
        raise ValueError("source path escapes the approved root")
    return target


def parse_document(root: Path, relative_path: str, max_bytes: int = 1_000_000) -> ParsedDocument:
    path = resolve_bounded(root, relative_path)
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError(f"unsupported source type: {path.suffix}")
    raw = path.read_bytes()
    if not raw:
        raise ValueError("empty source")
    if len(raw) > max_bytes:
        raise ValueError("source exceeds configured byte limit")
    if b"\x00" in raw:
        raise ValueError("NUL bytes are not permitted")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("source is not strict UTF-8") from exc
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = tuple(normalized.splitlines())
    flags = tuple(name for name, pattern in RISK_PATTERNS.items() if pattern.search(normalized))
    return ParsedDocument(
        raw_bytes=raw,
        normalized_text=normalized,
        lines=lines,
        raw_sha256=sha256(raw).hexdigest(),
        normalized_sha256=sha256(normalized.encode("utf-8")).hexdigest(),
        risk_flags=flags,
    )
