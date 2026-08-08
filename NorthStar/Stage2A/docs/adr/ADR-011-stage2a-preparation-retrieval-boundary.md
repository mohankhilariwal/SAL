# ADR-011 — Split Stage 2 at the Preparation and Retrieval Boundary

- **Status:** Accepted
- **Date:** 2026-07-31
- **Decision owners:** Priya Raman, Sofia Alvarez, Marcus Green

## Context

Stage 1 established a bounded preliminary summarizer but no internal knowledge access. The next full capability described by the master prompt includes ingestion, chunking, search, reranking, citations and retrieval evaluation. Implementing all of those at once would combine two materially different trust boundaries: preparing approved knowledge and serving query-time evidence. The uploaded Stage 1 handoff requires authorization to precede model context assembly and explicitly prohibits premature agent behavior.

## Decision

Divide Stage 2 into:

- **S02A — Ingestion, Chunking and Knowledge Preparation:** approved-manifest intake, strict parsing, provenance, deterministic chunking, access metadata, versioning, immutable packages and preparation validation.
- **S02B — Authorized Retrieval and Grounded Evidence:** lexical/semantic candidate generation, deterministic authorization filtering, hybrid fusion, reranking, exact citations and retrieval evaluation.

S02A must not expose a search API, assemble model context or introduce an agent/tool identifier.

## Alternatives

1. Implement all of Stage 2 in one response and repository change.
2. Prepare documents lazily when each query arrives.
3. Begin with long-context prompting over whole repositories.
4. Split at the explicit preparation/retrieval contract boundary.

## Rationale

The split keeps the stage bounded and executable, makes corpus quality independently testable, and prevents query-time authorization from being simulated before access metadata exists. It also creates a stable prepared-corpus contract that can support multiple index technologies.

## Consequences

- Maya cannot yet search the prepared corpus.
- S02B can evaluate search and ranking against a stable input.
- Corpus rebuilds become explicit when parser/chunker versions change.
- Documentation and testing overhead increase because each substage has a complete handoff.

## Risks

- Stakeholders may mistake a prepared corpus for a retrieval service.
- A later index may require schema changes.
- Manual exports may become stale between S02A and S02B.

## Mitigations

- Mark `CMP-004` as partial/preparation-only.
- Do not implement search methods or allocate agent/tool IDs.
- Include corpus and transformation versions in every package.
- Require S02B to consume `INT-010` and preserve exact evidence semantics.

## Review triggers

- The prepared-corpus schema cannot support the selected S02B index.
- Source systems provide native access-aware query APIs that make local preparation unnecessary.
- Corpus scale or freshness requires event-driven ingestion rather than batch preparation.
