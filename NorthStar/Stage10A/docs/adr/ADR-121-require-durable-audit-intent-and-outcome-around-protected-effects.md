# ADR-121: Require durable audit intent and outcome around protected effects

- **Status:** Accepted
- **Stage:** S10A
- **Architecture version:** 1.15.0

## Context

An audit record written only after an external or protected action can be missing when the action succeeds but logging fails.

## Decision

CMP-005 and CMP-003 append a required intent before protected effects and an outcome/reconciliation event after. Mandatory append failure blocks the effect.

## Alternatives

Best-effort post-action logging; log every low-risk read synchronously; transactional coupling to a remote global service.

## Rationale

Supports ambiguous-outcome investigation and fail-closed accountability without centralizing all telemetry.

## Consequences

Added latency and availability dependency on the local durable ledger.

## Risks

Added latency and availability dependency on the local durable ledger.

## Mitigations

Local append path, fsync, bulkheads, performance guard, recovery runbook and future durable replicated service.

## Review trigger

Measured overhead exceeds SLOs or transaction boundaries change.
