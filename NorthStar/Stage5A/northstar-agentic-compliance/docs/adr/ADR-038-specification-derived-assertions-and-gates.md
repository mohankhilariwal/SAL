# ADR-038 — Derive Runtime Assertions, Evaluations and Deployment Gates from the Specification

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

A specification that is not checked against runtime composition can become stale documentation. Conversely, interpreting the specification as a runtime policy engine would duplicate or bypass existing control owners.

## Decision

Bind the `DATA-071` digest into the S04C manifest as `DATA-072`, execute deterministic `DATA-073` assertions at pre-start and post-result phases, map required tests/evaluations into `DATA-075`, and require a deny-by-default `DATA-076` deployment gate.

Assertions verify composition and outcomes, including one agent, graph/version compatibility, exact tools, no memory/concurrency/multiple agents, context-policy compliance, preliminary dispositions, timeout behavior, one `TOOL-006` effect and secret exclusion. They do not select graph routes, grant permissions or consume human decisions.

## Alternatives

- Documentation review only.
- CI schema validation only.
- Runtime prompt self-check.
- Model-based evaluator as the only gate.
- Full policy-engine replacement of existing controls.

## Rationale

The selected design keeps enforcement deterministic and testable while preserving the existing graph/gateway/approval boundaries.

## Consequences

- Incompatible specifications fail before a new run.
- Missing test/evaluation/security evidence blocks the local deployment gate.
- False positives can reduce availability; compatibility failures require controlled correction or a migration ADR.
- This is not production release attestation, signing or continuous evaluation infrastructure.

## Review triggers

Production CI/CD, signed artefact attestations, remote registries, canary releases, in-flight migration or continuous evaluation.
