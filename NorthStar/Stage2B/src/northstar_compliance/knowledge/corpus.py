from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import json

from .schemas import KnowledgeChunk


@dataclass(frozen=True)
class PreparedCorpus:
    root: Path
    manifest: dict
    chunks: tuple[KnowledgeChunk, ...]

    @property
    def corpus_hash(self) -> str:
        return self.manifest["corpus_hash"]

    @property
    def source_versions(self) -> tuple[str, ...]:
        return tuple(sorted({c.source_version_id for c in self.chunks}))

    def normalized_source_path(self, chunk: KnowledgeChunk) -> Path:
        return self.root / "corpus" / chunk.source_id / chunk.source_version_id / "normalized.txt"


def load_prepared_corpus(root: Path) -> PreparedCorpus:
    manifest_path = root / "corpus-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    chunks: list[KnowledgeChunk] = []
    for entry in manifest["entries"]:
        path = root / entry["package_path"] / "chunks.jsonl"
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                chunks.append(KnowledgeChunk.from_dict(json.loads(line)))
    canonical = json.dumps([c.to_dict() for c in sorted(chunks, key=lambda x: x.chunk_id)], sort_keys=True, separators=(",", ":"))
    actual_hash = sha256(canonical.encode("utf-8")).hexdigest()
    if actual_hash != manifest["corpus_hash"]:
        raise ValueError("prepared corpus hash mismatch")
    return PreparedCorpus(root=root, manifest=manifest, chunks=tuple(chunks))
