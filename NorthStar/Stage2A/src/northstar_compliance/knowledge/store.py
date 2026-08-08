from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Iterable

from .schemas import KnowledgeChunk, KnowledgeDocumentVersion, KnowledgeSourceDescriptor


def _canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


class LocalKnowledgeStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.corpus_root = root / "corpus"
        self.runs_root = root / "runs"
        self.manifest_path = root / "corpus-manifest.json"
        self.root.mkdir(parents=True, exist_ok=True)

    def has_version(self, source_id: str, source_version_id: str) -> bool:
        return (self.corpus_root / source_id / source_version_id / "document-version.json").is_file()

    def write_version(
        self,
        *,
        descriptor: KnowledgeSourceDescriptor,
        document_version: KnowledgeDocumentVersion,
        raw_bytes: bytes,
        normalized_text: str,
        chunks: Iterable[KnowledgeChunk],
    ) -> str:
        target = self.corpus_root / descriptor.source_id / document_version.source_version_id
        if target.exists():
            return "REUSED"

        target.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=f".{document_version.source_version_id}.", dir=target.parent))
        try:
            (staging / "raw").mkdir(parents=True)
            (staging / "raw" / Path(descriptor.relative_path).name).write_bytes(raw_bytes)
            atomic_write_text(staging / "normalized.txt", normalized_text)
            atomic_write_json(staging / "descriptor.json", descriptor.to_dict())
            atomic_write_json(staging / "document-version.json", document_version.to_dict())
            chunk_list = list(chunks)
            chunk_lines = "".join(_canonical_json(chunk.to_dict()) + "\n" for chunk in chunk_list)
            atomic_write_text(staging / "chunks.jsonl", chunk_lines)
            os.replace(staging, target)
        except Exception:
            shutil.rmtree(staging, ignore_errors=True)
            raise
        return "CREATED"

    def load_manifest(self) -> dict[str, Any]:
        if not self.manifest_path.exists():
            return {
                "schema_version": "1.0.0",
                "corpus_version": "0.3.0",
                "active_versions": {},
                "versions": {},
                "chunking_policy": {},
            }
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def write_manifest(self, manifest: dict[str, Any]) -> None:
        atomic_write_json(self.manifest_path, manifest)

    def write_run(self, run_id: str, data: dict[str, Any]) -> Path:
        path = self.runs_root / f"{run_id}.json"
        atomic_write_json(path, data)
        return path
