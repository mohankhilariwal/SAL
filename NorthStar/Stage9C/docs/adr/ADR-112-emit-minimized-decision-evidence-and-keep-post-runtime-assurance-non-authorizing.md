# ADR-112: Emit minimized decision evidence and keep post-runtime assurance non-authorizing

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

Stage 9C must close the guardrail and governance gap identified by the S09B handoff while preserving exactly one active `AGT-001`, `AUTH-001/1.0.0`, `BR-001/1.0.0`, all established authority owners, unresolved Stage 8D and inactive future routes.

## Decision

DATA-197 records identifiers, digests, reason codes, obligations, bundle version and exception reference. It excludes secrets, unrestricted tokens, raw sensitive payloads and hidden chain-of-thought. Async assurance has authority_effect none.

## Alternatives

1. Rely on prompt instructions or a single moderation filter.
2. Centralize every runtime decision in a remote control-plane service.
3. Use only model-based classification.
4. Defer all governance until production deployment.

## Rationale

The selected decision is the smallest design that addresses the current NorthStar failure path, remains locally executable and preserves the accepted security and accountability boundaries.

## Consequences

- More explicit policy, evidence and testing work.
- Deterministic runtime latency is added at several PEPs.
- Policy changes become versioned, reviewable and reversible.
- The full distributed enterprise control plane remains future work.

## Risks and mitigations

Policy omission, stale bundles, exception abuse, classifier drift and enforcement bypass remain possible. Mitigations include schema validation, negative tests, independent approval, immutable digests, local fail-closed behavior for high-impact operations and minimized decision evidence.

## Review triggers

Review on any new tool, authority tier, agent, MCP/A2A route, production deployment, policy-engine adapter, legal/regulatory requirement, control failure or Stage 8D resolution.
