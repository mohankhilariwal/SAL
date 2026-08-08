"""Controlled knowledge ingestion and preparation for Stage 2A."""

from .chunker import ChunkingPolicy, StructureAwareLineChunker
from .schemas import (
    AccessScope,
    IngestionRunRecord,
    KnowledgeChunk,
    KnowledgeDocumentVersion,
    KnowledgeSourceDescriptor,
)
from .service import KnowledgePreparationService

__all__ = [
    "AccessScope",
    "ChunkingPolicy",
    "IngestionRunRecord",
    "KnowledgeChunk",
    "KnowledgeDocumentVersion",
    "KnowledgePreparationService",
    "KnowledgeSourceDescriptor",
    "StructureAwareLineChunker",
]
