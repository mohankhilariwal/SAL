# ADR-043 — Consent, Provenance, Expiry, Deletion and Isolation Controls

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

Persistent memory can retain stale or sensitive data beyond the purpose for which it was created and can leak across tenants, cases or users.

## Decision

Every memory write/read/delete requires `DATA-082 MemoryConsentGrant` bound to tenant, case, user, purpose, operations and expiry. Records require source references, versions and hashes; use a provisional 14-day default and 30-day maximum; stale records are excluded by default; deletion/expiry removes content and leaves a content-free lifecycle tombstone. Storage paths are tenant/case partitioned and validated.

The consent object is a product opt-in acknowledgement, not a legal conclusion about the applicable lawful basis. Production privacy/records review remains mandatory.

## Alternatives

- Implicit consent — rejected.
- Indefinite retention — rejected.
- Soft delete with content retained — rejected for the local tutorial boundary.
- Global memory index — rejected because isolation and deletion would be harder to prove.

## Rationale

These controls align the technical design with purpose limitation, retention, accuracy, safeguards and deletion principles while preserving jurisdiction-specific legal review.

## Consequences

Memory may disappear before a case completes; the system must remain functional through authoritative regeneration. Production stores need stronger erasure propagation, backup handling, KMS, IAM and evidence.

## Risks and mitigations

- **Risk:** local tombstones are not an audit record. **Mitigation:** label them lifecycle evidence only.
- **Risk:** retention values are wrong for a jurisdiction or record class. **Mitigation:** values are provisional and configurable; production approval is an issue.

## Review triggers

Records schedules, litigation hold, data-subject requests, backup replication, production IAM/PDP/KMS, or cross-region deployment.
