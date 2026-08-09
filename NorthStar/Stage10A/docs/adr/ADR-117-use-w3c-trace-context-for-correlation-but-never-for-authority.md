# ADR-117: Use W3C Trace Context for correlation but never for authority

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

Distributed traces need a portable context format, but trace headers are user-influenced and unauthenticated.

## Decision

Propagate traceparent/tracestate only for correlation. Tenant, case, principal, grant and approval context come from authenticated envelopes and receiver-side checks.

## Alternatives

Use trace IDs or baggage as authorization attributes; reject all external context; create custom headers only.

## Rationale

Interoperable tracing without creating a confused-deputy path.

## Consequences

Spoofed trace trees, cardinality attacks or data leakage through baggage.

## Risks

Spoofed trace trees, cardinality attacks or data leakage through baggage.

## Mitigations

Strict parser, new root on invalid input, baggage allowlist and no sensitive identifiers in baggage.

## Review trigger

Protocol activation, external trust federation or trace-context specification change.
