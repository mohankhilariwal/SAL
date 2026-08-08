# ADR-037 — JSON, JSON Schema 2020-12, Semantic Validation and Canonical Digest

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

A syntax-valid document can still contradict accepted architecture. NorthStar needs a portable representation, structural validation and cross-contract semantic checks.

## Decision

Use JSON as the canonical local representation, publish `DATA-071` as a JSON Schema Draft 2020-12 artefact, supplement schema validation with an application-owned semantic validator, and compute SHA-256 over canonical sorted compact JSON.

## Alternatives

- YAML without a canonicalization profile.
- Prose-only Markdown.
- Framework-native Python objects.
- A general-purpose policy/constraint language.
- A database record without repository-controlled source.

## Rationale

JSON is deterministic and tool-neutral for the local stage. JSON Schema expresses structural constraints; semantic code checks stable IDs, versions, exact allowlists, external-control ownership and no-memory/no-concurrency boundaries. A canonical digest binds the accepted content to the harness manifest.

## Consequences

- Human readability is lower than prose, so the stage chapter and catalogue remain explanatory companions.
- SHA-256 proves content equality in this local package, not authorship, signing or deployment attestation.
- Schema and semantic validator versions must evolve together.

## Risks and mitigations

- **Risk:** schema-valid but unsafe spec. **Mitigation:** semantic validator and runtime assertions.
- **Risk:** alternate serializer changes the hash. **Mitigation:** one documented canonicalization function.
- **Risk:** unsigned local files. **Mitigation:** production signing/KMS/attestation remains an explicit gap.

## Review triggers

Need for signed registry distribution, multi-language validation, remote control-plane management, schema federation or standards-based agent-card interoperability.
