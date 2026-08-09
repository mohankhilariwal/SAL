# ADR-115: Separate operational observability from accountability audit

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

Operational telemetry is high-volume and sampled; audit evidence must be complete for material actions.

## Decision

Implement OBS-001 and AUD-001 as distinct logical paths within CMP-009, sharing identifiers but not retention, sampling, failure or access semantics.

## Alternatives

One undifferentiated log stream; audit-only storage; telemetry-only reconstruction.

## Rationale

Prevents sampled traces from being mistaken for complete evidence and avoids forcing all debug data into long-term audit storage.

## Consequences

Cross-link divergence or duplicate records.

## Risks

Cross-link divergence or duplicate records.

## Mitigations

Canonical correlation context, event IDs, reconciliation tests and evidence manifests.

## Review trigger

Material event coverage gaps or storage/operational cost changes.
