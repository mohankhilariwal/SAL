# ADR-013 — Immutable Knowledge Packages and Fail-Closed Access Metadata

- **Status:** Accepted
- **Date:** 2026-07-31
- **Decision owners:** Marcus Green, Sofia Alvarez, Elena Petrov

## Context

A later retrieval system must distinguish current from historical content, reproduce the exact corpus used for an answer, and prevent unauthorized candidates from entering ranking or model context. Overwriting chunks in place would erase transformation history. Treating access labels as optional would create permission-leakage risk.

## Decision

Create immutable, content-addressed knowledge source-version packages:

- derive `KSV-*` from source ID, business version label, normalized content hash, metadata hash, parser version and chunker version;
- derive `CHK-*` from source-version ID, coordinates and exact text;
- require a non-empty access group set and purpose classification before ingestion;
- copy the access scope exactly to every chunk;
- retain historical versions and identify one active version per source in the corpus manifest;
- publish packages through staging and same-filesystem atomic replacement;
- treat identical replay as idempotent and changed content/transformation as a new version.

## Alternatives

1. Mutable “latest only” files.
2. Database rows updated in place.
3. Content-addressed packages without access metadata.
4. Immutable packages with required access metadata and active pointers.

## Rationale

The design supports provenance, reproducibility, rollback and later pre-retrieval authorization without selecting a vector database. It fails closed when security metadata is missing.

## Consequences

- Storage grows with historical versions.
- Deletion/retention requirements need explicit lifecycle handling later.
- Group strings are tutorial claims until connected to `CMP-007`.
- Indexes must be rebuilt or incrementally synchronized when the active corpus changes.

## Risks

- Incorrect source-owner metadata can still authorize the wrong users.
- Immutable local history can conflict with legal deletion requirements.
- Atomic filesystem publication does not provide tamper evidence or distributed transactions.

## Mitigations

- Validate manifest fields and reject empty access groups.
- Record source owner, authority, dates, residency and purpose.
- Keep this store explicitly non-production.
- Require enterprise identity/PDP reconciliation and retention design before production retrieval.

## Review triggers

- Integration with enterprise IAM/PDP or records-retention systems.
- Multi-node/distributed ingestion.
- Required cryptographic signing or WORM storage.
- Tenant-specific partitioning or geographic residency enforcement.
