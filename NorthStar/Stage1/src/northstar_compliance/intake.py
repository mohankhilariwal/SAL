from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .schemas import PublicationMetadata


class IntakeError(ValueError):
    pass


@dataclass(frozen=True)
class Publication:
    metadata: PublicationMetadata
    text: str
    lines: tuple[str, ...]


def _publication_id(digest: str) -> str:
    return f"PUB-{digest[:16].upper()}"


def ingest_publication(
    path: Path,
    *,
    title: str,
    source_uri: str,
    jurisdiction: str,
    max_bytes: int = 250_000,
) -> Publication:
    if path.suffix.lower() not in {".txt", ".md"}:
        raise IntakeError("Stage 1 accepts only .txt and .md files")
    if not path.is_file():
        raise IntakeError(f"Input file does not exist: {path}")
    raw = path.read_bytes()
    if not raw:
        raise IntakeError("Input publication is empty")
    if len(raw) > max_bytes:
        raise IntakeError(f"Input exceeds configured byte limit: {len(raw)} > {max_bytes}")
    if b"\x00" in raw:
        raise IntakeError("Binary/NUL-containing input is not accepted")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IntakeError("Input must be valid UTF-8") from exc
    if not text.strip():
        raise IntakeError("Input publication contains no non-whitespace text")
    digest = hashlib.sha256(raw).hexdigest()
    lines = tuple(text.splitlines())
    metadata = PublicationMetadata(
        publication_id=_publication_id(digest),
        title=title.strip(),
        source_uri=source_uri.strip(),
        jurisdiction=jurisdiction.strip(),
        received_at=datetime.now(timezone.utc).isoformat(),
        file_name=path.name,
        sha256=digest,
        line_count=len(lines),
        byte_count=len(raw),
    )
    if not metadata.title or not metadata.source_uri or not metadata.jurisdiction:
        raise IntakeError("title, source_uri and jurisdiction are required")
    return Publication(metadata=metadata, text=text, lines=lines)
