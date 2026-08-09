# ADR-116: Use a provider-neutral canonical telemetry schema with OpenTelemetry adapters

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

Core OpenTelemetry logs/traces/metrics are stable, while GenAI and agent conventions continue to evolve.

## Decision

Define DATA-217..228 as NorthStar canonical records; map to W3C/OpenTelemetry fields at adapters and require semantic conformance tests.

## Alternatives

Directly persist vendor SDK payloads; invent a proprietary transport; freeze emerging GenAI attributes into core state.

## Rationale

Preserves portability and allows adoption of current conventions without coupling source-of-truth schemas to unstable fields.

## Consequences

Adapter drift and lossy mappings.

## Risks

Adapter drift and lossy mappings.

## Mitigations

Versioned mapping profile, opt-in fields, contract tests and raw-event fixtures.

## Review trigger

OpenTelemetry GenAI conventions reach stable status or NorthStar adopts a managed backend.
