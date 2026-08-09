# ADR-092: Use ordinal risk prioritization without false precision

- Status: Accepted
- Date: 2026-08-01

## Context
NorthStar requires Stage 9A threat modelling while preserving the accepted 1.11.0 architecture and its unresolved evaluation/deployment-gate work.

## Decision
Use a NorthStar 1-5 likelihood and impact scale only for prioritization; preserve raw factors and hard invariant failures rather than claiming actuarial probabilities or a universal score.

## Alternatives
1. Defer threat modelling until Stage 8D is complete.
2. Use STRIDE alone.
3. Use only an agentic threat list without architecture-specific data flows.
4. Allow the threat model to update runtime policy automatically.

## Rationale
The selected approach preserves the execution controller's explicit-stage rule while maintaining architectural honesty, systematic coverage, agent-specific depth, reproducibility and human authority.

## Consequences
The repository gains a local threat-model laboratory, schemas, catalogue, attack trees, misuse cases, reports and tests. No runtime authority or production security certification is created.

## Risks
The overlay may be mistaken for a merged historical register or for proof of production security.

## Mitigations
Record `ISS-096`, `ISS-131`, `ISS-140` and the advisory-only scope; require a later identity, authorization, blast-radius and production-control implementation.

## Review triggers
Any new agent, tool, route, model/provider, memory scope, external protocol endpoint, code/browser capability, identity design, deployment topology or material data-flow change.
