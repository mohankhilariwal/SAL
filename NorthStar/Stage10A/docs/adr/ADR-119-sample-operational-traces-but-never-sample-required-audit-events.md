# ADR-119: Sample operational traces but never sample required audit events

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

Full traces can be expensive; material accountability events cannot be probabilistically omitted.

## Decision

Use policy-based sampling for spans/events and 100% capture for required audit types. Errors, denials, approvals, protected writes, exceptions and final disposition are always traced and audited.

## Alternatives

Always-on telemetry; ratio-sampled audit; error-only tracing.

## Rationale

Controls cost and volume without weakening accountability.

## Consequences

Sampling rules may miss useful context or create biased operational views.

## Risks

Sampling rules may miss useful context or create biased operational views.

## Mitigations

Tail/error sampling candidates, coverage metrics, unsampled audit path and periodic sampling review.

## Review trigger

Incident postmortems show missing diagnostic context or volume economics change.
