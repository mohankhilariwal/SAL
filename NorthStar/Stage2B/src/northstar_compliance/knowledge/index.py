from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from .corpus import PreparedCorpus
from .schemas import RetrievalIndexManifest, SCHEMA_VERSION
from .store import atomic_write_json

INDEX_CONFIG = {
    "lexical_algorithm": "BM25(k1=1.5,b=0.75)",
    "semantic_algorithm": "TF-IDF+truncated-SVD-LSA",
    "semantic_dimensions": 8,
    "fusion_algorithm": "weighted-RRF(k=60)",
    "reranker": "deterministic-metadata-aware-v1",
    "overlap_dedup_threshold": 0.50,
}


def canonical_hash(value: object) -> str:
    return sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()


def build_index_manifest(corpus: PreparedCorpus, output_path: Path) -> RetrievalIndexManifest:
    config_hash=canonical_hash(INDEX_CONFIG)
    material=f"{corpus.corpus_hash}|{config_hash}|{'|'.join(corpus.source_versions)}"
    index_id="RIDX-"+sha256(material.encode("utf-8")).hexdigest()[:20].upper()
    manifest=RetrievalIndexManifest(
        schema_version=SCHEMA_VERSION,
        index_id=index_id,
        corpus_hash=corpus.corpus_hash,
        config_hash=config_hash,
        built_at=datetime.now(timezone.utc).isoformat(),
        chunk_count=len(corpus.chunks),
        lexical_algorithm=INDEX_CONFIG["lexical_algorithm"],
        semantic_algorithm=INDEX_CONFIG["semantic_algorithm"],
        semantic_dimensions=INDEX_CONFIG["semantic_dimensions"],
        fusion_algorithm=INDEX_CONFIG["fusion_algorithm"],
        reranker=INDEX_CONFIG["reranker"],
        source_versions=corpus.source_versions,
    )
    atomic_write_json(output_path,manifest.to_dict())
    return manifest


def validate_index_manifest(corpus: PreparedCorpus, manifest: RetrievalIndexManifest) -> None:
    if manifest.corpus_hash != corpus.corpus_hash:
        raise ValueError("index/corpus hash mismatch; rebuild required")
    if manifest.config_hash != canonical_hash(INDEX_CONFIG):
        raise ValueError("retrieval configuration mismatch; rebuild required")
    if tuple(manifest.source_versions) != corpus.source_versions:
        raise ValueError("source-version mismatch; rebuild required")
