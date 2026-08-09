# ADR-095

**Status:** Accepted

## Context
See Stage 9B.

## Decision
Execute combined S09B identity/authorization/blast-radius scope; stop before broader guardrails/control plane.

## Alternatives
See the Stage 9B option and decision matrices.

## Consequences
Adds deterministic identity/authorization or containment semantics without changing human accountability or active-agent topology.

## Risks and mitigations
Tracked in `08-Risk-Assumption-and-Issue-Register.md`; deny by default, negative tests and explicit production limitations apply.

## Review trigger
Any material identity, token, policy, tool, tier, protocol, agent, approval or deployment change.
