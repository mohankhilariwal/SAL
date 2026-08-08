from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json

from .chunker import CHUNKER_VERSION, chunk_document
from .parser import PARSER_VERSION, parse_document
from .schemas import KnowledgeDocumentVersion, KnowledgeSourceDescriptor, SCHEMA_VERSION
from .store import atomic_write_json, atomic_write_jsonl, atomic_write_text


def canonical_hash(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def source_version_id(descriptor: KnowledgeSourceDescriptor, normalized_sha256: str) -> tuple[str, str]:
    metadata = descriptor.to_dict()
    metadata_sha = canonical_hash(metadata)
    material = "|".join(
        [descriptor.source_id, descriptor.version_label, normalized_sha256, metadata_sha, PARSER_VERSION, CHUNKER_VERSION]
    )
    return "KSV-" + sha256(material.encode("utf-8")).hexdigest()[:20].upper(), metadata_sha


class KnowledgePreparationService:
    def prepare(self, manifest_path: Path, source_root: Path, output_root: Path) -> dict:
        manifest_raw = json.loads(manifest_path.read_text(encoding="utf-8"))
        items = manifest_raw["sources"] if isinstance(manifest_raw, dict) else manifest_raw
        descriptors = [KnowledgeSourceDescriptor.from_dict(item) for item in items]
        corpus_entries = []
        all_chunks = []
        for descriptor in descriptors:
            descriptor.access.validate()
            parsed = parse_document(source_root, descriptor.relative_path)
            ksv, metadata_sha = source_version_id(descriptor, parsed.normalized_sha256)
            version = KnowledgeDocumentVersion(
                schema_version=SCHEMA_VERSION,
                source_id=descriptor.source_id,
                source_version_id=ksv,
                version_label=descriptor.version_label,
                raw_sha256=parsed.raw_sha256,
                normalized_sha256=parsed.normalized_sha256,
                metadata_sha256=metadata_sha,
                parser_version=PARSER_VERSION,
                chunker_version=CHUNKER_VERSION,
                line_count=len(parsed.lines),
                risk_flags=parsed.risk_flags,
            )
            chunks = chunk_document(
                descriptor=descriptor,
                source_version_id=ksv,
                normalized_sha256=parsed.normalized_sha256,
                lines=parsed.lines,
                risk_flags=parsed.risk_flags,
            )
            pkg = output_root / "corpus" / descriptor.source_id / ksv
            raw_name = Path(descriptor.relative_path).name
            atomic_write_text(pkg / "raw" / raw_name, parsed.raw_bytes.decode("utf-8"))
            atomic_write_text(pkg / "normalized.txt", parsed.normalized_text)
            atomic_write_json(pkg / "descriptor.json", descriptor.to_dict())
            atomic_write_json(pkg / "document-version.json", version.to_dict())
            atomic_write_jsonl(pkg / "chunks.jsonl", [c.to_dict() for c in chunks])
            corpus_entries.append({
                "source_id": descriptor.source_id,
                "active_source_version_id": ksv,
                "historical_source_version_ids": [],
                "chunk_count": len(chunks),
                "package_path": str(pkg.relative_to(output_root)),
            })
            all_chunks.extend(chunks)
        corpus_hash = canonical_hash([c.to_dict() for c in sorted(all_chunks, key=lambda x: x.chunk_id)])
        corpus_manifest = {
            "schema_version": SCHEMA_VERSION,
            "corpus_id": "CORPUS-" + corpus_hash[:20].upper(),
            "corpus_hash": corpus_hash,
            "parser_version": PARSER_VERSION,
            "chunker_version": CHUNKER_VERSION,
            "source_count": len(descriptors),
            "chunk_count": len(all_chunks),
            "entries": corpus_entries,
        }
        atomic_write_json(output_root / "corpus-manifest.json", corpus_manifest)
        run_id = "ING-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        run = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "manifest_sha256": sha256(manifest_path.read_bytes()).hexdigest(),
            "status": "COMPLETED",
            "source_count": len(descriptors),
            "chunk_count": len(all_chunks),
            "corpus_id": corpus_manifest["corpus_id"],
        }
        atomic_write_json(output_root / "runs" / f"{run_id}.json", run)
        return corpus_manifest
