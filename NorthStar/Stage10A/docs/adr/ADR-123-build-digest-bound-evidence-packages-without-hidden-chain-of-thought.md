# ADR-123: Build digest-bound evidence packages without hidden chain-of-thought

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

Auditors need actions, evidence and decisions, not private model reasoning.

## Decision

Package ordered audit events, artefact/source digests, policy/auth/approval/evaluation references, verification report and final disposition. Exclude hidden chain-of-thought and unrestricted secrets.

## Alternatives

Store full reasoning traces; provide only a human summary; export the complete telemetry backend.

## Rationale

Produces portable, minimal and auditable decision evidence.

## Consequences

Concise evidence may omit context needed for review.

## Risks

Concise evidence may omit context needed for review.

## Mitigations

Evidence sufficiency tests, source links, uncertainty fields and controlled supplemental artefacts.

## Review trigger

Audit users identify recurring evidence gaps.
