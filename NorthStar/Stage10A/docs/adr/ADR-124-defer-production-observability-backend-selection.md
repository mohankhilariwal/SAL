# ADR-124: Defer production observability backend selection

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

The stage must remain provider-neutral and no production deployment/control-plane decision exists.

## Decision

Use local JSONL exporters, canonical schemas and adapter contracts. Compare but do not select commercial or open-source backends.

## Alternatives

Select one vendor now; build a bespoke distributed backend; omit export contracts.

## Rationale

Keeps the local implementation runnable and avoids premature lock-in.

## Consequences

No proof of multi-region scale, retention, search, RBAC or cost.

## Risks

No proof of multi-region scale, retention, search, RBAC or cost.

## Mitigations

Document production selection criteria and conformance tests.

## Review trigger

S09D and deployment architecture establish regions, SLOs, data residency and procurement constraints.
