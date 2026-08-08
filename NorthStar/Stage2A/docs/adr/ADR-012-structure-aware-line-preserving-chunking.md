# ADR-012 — Deterministic Structure-Aware Line-Preserving Chunking

- **Status:** Accepted
- **Date:** 2026-07-31
- **Decision owners:** Priya Raman, Elena Petrov, Sofia Alvarez

## Context

NorthStar needs chunks small enough for later retrieval while preserving exact evidence coordinates and regulatory structure. Fixed character windows are reproducible but can sever headings, conditions and exceptions. Model-based semantic segmentation is flexible but probabilistic, expensive and harder to reproduce. The S01 evidence contract already uses line-based citations.

## Decision

Use deterministic Markdown-aware segmentation:

1. Normalize strict UTF-8 text while preserving line order.
2. Treat Markdown headings as hard section boundaries.
3. Split each section into bounded contiguous line windows.
4. Apply configurable line overlap within a section.
5. Preserve heading path, one-based start/end lines, exact text and SHA-256 content hash.
6. Version the chunking policy and include it in source-version identity.

Default tutorial policy: maximum 1,200 characters, maximum 24 lines and two-line overlap.

## Alternatives

1. Whole-document chunks.
2. Fixed characters/tokens with no structure.
3. Paragraph or sentence segmentation.
4. Model-based semantic chunking.
5. Structure-aware deterministic line chunks.

## Rationale

The selected design preserves S01 line evidence semantics, supports deterministic replay and is dependency-free. It is not asserted to be universally optimal; retrieval evaluation in S02B will determine whether the policy should change.

## Consequences

- Headings and exact coordinates are available to later ranking/citation layers.
- Overlap creates intentional duplicate context that S02B must deduplicate or account for.
- Character limits are not token-aware.
- Poorly structured source Markdown may yield weaker chunks.

## Risks

- Conditions or definitions can still be separated.
- Excessive overlap can inflate index size and duplicate results.
- A heading-only section can create unhelpful context.

## Mitigations

- Retain heading path and overlap.
- Independently validate full line coverage and exact reconstruction.
- Version the policy and require index rebuild plus regression evaluation after change.
- Add format-specific parsers only through a future ADR.

## Review triggers

- Context recall/precision shows systematic fragmentation.
- Token-aware model limits require different boundaries.
- PDF/HTML/Office structure needs richer element-aware parsing.
- Corpus storage or retrieval cost is materially affected by overlap.
