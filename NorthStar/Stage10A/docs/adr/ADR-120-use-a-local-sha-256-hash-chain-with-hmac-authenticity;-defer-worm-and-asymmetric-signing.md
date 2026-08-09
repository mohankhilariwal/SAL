# ADR-120: Use a local SHA-256 hash chain with HMAC authenticity; defer WORM and asymmetric signing

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

The stage needs runnable tamper detection, but no production KMS/HSM, timestamp authority or WORM service is available.

## Decision

Implement canonical JSON, sequence numbers, previous hashes, payload/record hashes and local HMAC signatures. Declare no non-repudiation, WORM or production signing claim.

## Alternatives

Plain JSON logs; blockchain; local asymmetric key generation presented as production; managed ledger selection.

## Rationale

Demonstrates integrity mechanics locally while preserving the future production boundary.

## Consequences

Shared-key compromise, deletion of whole ledger, weak timestamp assurance and local disk loss.

## Risks

Shared-key compromise, deletion of whole ledger, weak timestamp assurance and local disk loss.

## Mitigations

Signed checkpoints, external anchoring design, production KMS/HSM/WORM requirements and explicit limitations.

## Review trigger

S09D/deployment selects enterprise key and records services.
