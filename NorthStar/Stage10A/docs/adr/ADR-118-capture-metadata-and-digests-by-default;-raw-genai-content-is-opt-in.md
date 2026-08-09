# ADR-118: Capture metadata and digests by default; raw GenAI content is opt-in

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

Prompts, completions, retrieval results and tool arguments may contain confidential, regulated or secret data.

## Decision

Default telemetry and audit to metadata, source references, counts, reason codes and cryptographic digests. Raw content requires a separately authorized evidence vault and approved retention policy.

## Alternatives

Capture all content; capture nothing; rely only on downstream redaction.

## Rationale

Reduces privacy exposure while retaining operational and forensic value.

## Consequences

Over-redaction may impede investigation; under-redaction leaks data.

## Risks

Over-redaction may impede investigation; under-redaction leaks data.

## Mitigations

Pre-export redaction, field classification, digest references, tests and controlled evidence access.

## Review trigger

Investigations demonstrate insufficient evidence or legal/records policy changes.
