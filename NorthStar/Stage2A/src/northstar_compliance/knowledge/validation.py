from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .schemas import KnowledgeError


def validate_prepared_corpus(output_root: Path) -> dict[str, int]:
    manifest_path = output_root / "corpus-manifest.json"
    if not manifest_path.is_file():
        raise KnowledgeError("corpus-manifest.json is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    active = manifest.get("active_versions", {})
    if not active:
        raise KnowledgeError("corpus has no active versions")

    source_count = 0
    chunk_count = 0
    warning_count = 0
    for source_id, source_version_id in active.items():
        version_root = output_root / "corpus" / source_id / source_version_id
        descriptor = json.loads((version_root / "descriptor.json").read_text(encoding="utf-8"))
        version = json.loads((version_root / "document-version.json").read_text(encoding="utf-8"))
        normalized = (version_root / "normalized.txt").read_text(encoding="utf-8")
        lines = tuple(normalized.splitlines())
        if hashlib.sha256(normalized.encode("utf-8")).hexdigest() != version["normalized_sha256"]:
            raise KnowledgeError(f"normalized hash mismatch for {source_id}")
        access = descriptor["access"]
        if not access.get("allowed_groups"):
            raise KnowledgeError(f"missing access groups for {source_id}")

        seen_ids: set[str] = set()
        with (version_root / "chunks.jsonl").open(encoding="utf-8") as handle:
            for raw_line in handle:
                chunk = json.loads(raw_line)
                if chunk["chunk_id"] in seen_ids:
                    raise KnowledgeError(f"duplicate chunk_id in {source_id}")
                seen_ids.add(chunk["chunk_id"])
                start = int(chunk["line_start"])
                end = int(chunk["line_end"])
                expected = "\n".join(lines[start - 1 : end])
                if expected != chunk["text"]:
                    raise KnowledgeError(f"line-coordinate mismatch for {chunk['chunk_id']}")
                if hashlib.sha256(expected.encode("utf-8")).hexdigest() != chunk["content_sha256"]:
                    raise KnowledgeError(f"chunk hash mismatch for {chunk['chunk_id']}")
                if chunk["access"] != access:
                    raise KnowledgeError(f"access scope not propagated to {chunk['chunk_id']}")
                warning_count += len(chunk.get("risk_flags", []))
                chunk_count += 1
        source_count += 1

    return {"sources": source_count, "chunks": chunk_count, "warnings": warning_count}
