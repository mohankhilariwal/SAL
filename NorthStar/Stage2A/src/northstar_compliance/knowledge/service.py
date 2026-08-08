from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .chunker import CHUNKER_VERSION, ChunkingPolicy, StructureAwareLineChunker
from .parser import PARSER_VERSION, parse_text_document, resolve_bounded_path, sha256_hex
from .schemas import (
    AccessScope,
    Classification,
    IngestionItemResult,
    IngestionRunRecord,
    KnowledgeDocumentVersion,
    KnowledgeError,
    KnowledgeSourceDescriptor,
    SourceType,
)
from .store import LocalKnowledgeStore


def _canonical_bytes(data: Any) -> bytes:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _descriptor_from_dict(item: dict[str, Any]) -> KnowledgeSourceDescriptor:
    try:
        access_raw = item["access"]
        access = AccessScope(
            classification=Classification(access_raw["classification"]),
            allowed_groups=tuple(access_raw["allowed_groups"]),
            residency=access_raw.get("residency", "CA"),
            purpose=access_raw.get("purpose", "REGULATORY_CHANGE_ANALYSIS"),
        )
        return KnowledgeSourceDescriptor(
            source_id=item["source_id"],
            title=item["title"],
            source_type=SourceType(item["source_type"]),
            owner=item["owner"],
            relative_path=item["relative_path"],
            version_label=item["version_label"],
            effective_from=item["effective_from"],
            effective_to=item.get("effective_to"),
            jurisdictions=tuple(item["jurisdictions"]),
            business_domains=tuple(item["business_domains"]),
            access=access,
            retention_class=item["retention_class"],
            authoritative=bool(item.get("authoritative", True)),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise KnowledgeError(f"invalid source descriptor: {exc}") from exc


class KnowledgePreparationService:
    def __init__(
        self,
        *,
        input_root: Path,
        output_root: Path,
        policy: ChunkingPolicy | None = None,
        max_bytes: int = 2_000_000,
    ) -> None:
        self.input_root = input_root.resolve()
        self.store = LocalKnowledgeStore(output_root.resolve())
        self.chunker = StructureAwareLineChunker(policy)
        self.max_bytes = max_bytes

    def prepare(self, manifest_path: Path) -> IngestionRunRecord:
        raw_manifest = manifest_path.read_bytes()
        manifest_hash = sha256_hex(raw_manifest)
        run_id = f"ING-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}"
        run = IngestionRunRecord.start(run_id)
        run.manifest_sha256 = manifest_hash

        try:
            manifest_data = json.loads(raw_manifest.decode("utf-8", errors="strict"))
            items = manifest_data.get("sources")
            if not isinstance(items, list) or not items:
                raise KnowledgeError("manifest.sources must be a non-empty list")

            descriptors = [_descriptor_from_dict(item) for item in items]
            ids = [descriptor.source_id for descriptor in descriptors]
            if len(ids) != len(set(ids)):
                raise KnowledgeError("duplicate source_id in manifest")

            corpus_manifest = self.store.load_manifest()
            versions = corpus_manifest.setdefault("versions", {})
            active = corpus_manifest.setdefault("active_versions", {})
            corpus_manifest["chunking_policy"] = self.chunker.policy_dict()
            corpus_manifest["parser_version"] = PARSER_VERSION

            for descriptor in descriptors:
                source_path = resolve_bounded_path(self.input_root, descriptor.relative_path)
                parsed = parse_text_document(source_path, max_bytes=self.max_bytes)
                descriptor_dict = descriptor.to_dict()
                metadata_sha = hashlib.sha256(_canonical_bytes(descriptor_dict)).hexdigest()
                identity_payload = (
                    f"{descriptor.source_id}|{descriptor.version_label}|{parsed.normalized_sha256}|"
                    f"{metadata_sha}|{PARSER_VERSION}|{CHUNKER_VERSION}"
                ).encode("utf-8")
                source_version_id = f"KSV-{hashlib.sha256(identity_payload).hexdigest()[:20].upper()}"
                previous = active.get(descriptor.source_id)
                status = "PREPARED_WITH_WARNINGS" if parsed.risk_flags else "PREPARED"
                document_version = KnowledgeDocumentVersion(
                    source_id=descriptor.source_id,
                    source_version_id=source_version_id,
                    version_label=descriptor.version_label,
                    raw_sha256=parsed.raw_sha256,
                    normalized_sha256=parsed.normalized_sha256,
                    metadata_sha256=metadata_sha,
                    byte_count=len(parsed.raw_bytes),
                    line_count=len(parsed.lines),
                    parser_version=PARSER_VERSION,
                    chunker_version=CHUNKER_VERSION,
                    ingested_at=datetime.now(timezone.utc).isoformat(),
                    status=status,
                    risk_flags=parsed.risk_flags,
                    supersedes=previous if previous and previous != source_version_id else None,
                )
                chunks = self.chunker.chunk(
                    descriptor=descriptor,
                    source_version_id=source_version_id,
                    lines=parsed.lines,
                    document_risk_flags=parsed.risk_flags,
                )
                if not chunks:
                    raise KnowledgeError(f"{descriptor.source_id} produced zero chunks")
                action = self.store.write_version(
                    descriptor=descriptor,
                    document_version=document_version,
                    raw_bytes=parsed.raw_bytes,
                    normalized_text=parsed.normalized_text,
                    chunks=chunks,
                )
                versions[source_version_id] = document_version.to_dict()
                active[descriptor.source_id] = source_version_id
                run.items.append(
                    IngestionItemResult(
                        source_id=descriptor.source_id,
                        source_version_id=source_version_id,
                        action=action,
                        chunk_count=len(chunks),
                        status=status,
                        risk_flags=parsed.risk_flags,
                    )
                )

            corpus_manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
            corpus_manifest["source_count"] = len(active)
            corpus_manifest["version_count"] = len(versions)
            corpus_manifest["active_chunk_count"] = sum(item.chunk_count for item in run.items)
            corpus_manifest["manifest_input_sha256"] = manifest_hash
            self.store.write_manifest(corpus_manifest)
            run.complete(status="COMPLETED_WITH_WARNINGS" if any(item.risk_flags for item in run.items) else "COMPLETED")
        except Exception as exc:
            run.errors.append(f"{type(exc).__name__}: {exc}")
            run.complete(status="FAILED")
            self.store.write_run(run.run_id, run.to_dict())
            raise

        self.store.write_run(run.run_id, run.to_dict())
        return run
