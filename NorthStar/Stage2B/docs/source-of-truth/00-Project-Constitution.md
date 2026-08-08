# 00 — Project Constitution

## Current governed baseline

- Organization: **NorthStar Financial Services**.
- Playbook branch: the S02A handoff supplied with this execution is the immediate authoritative baseline.
- Architecture, repository and handoff version after this stage: `0.4.0`.
- Current stage: `S02B — Retrieval, Reranking, Citations and RAG Evaluation`.
- Execution date: 2026-07-31.

## Unchanged constitutional principles

1. Introduce the simplest capability that resolves the demonstrated limitation.
2. Preserve named human accountability for regulated conclusions and approvals.
3. Enforce critical access and disposition controls outside probabilistic model reasoning.
4. Keep evidence facts, system inferences, human decisions and unresolved uncertainty distinguishable.
5. Preserve stable identifiers and require ADR-controlled change.
6. Maintain one cumulative architecture and one evolving repository.
7. Treat retrieved content as untrusted evidence data, never as application instruction.
8. Store concise evidence and decisions, not hidden chain-of-thought.
9. Do not claim production readiness from a local synthetic demonstration.

## S02B constitutional boundary

S02B is a deterministic retrieval application capability inside `CMP-004`. It may accept a typed query and a locally asserted principal context, filter chunks, generate lexical and latent-semantic candidates, fuse and rerank them, validate exact citations, assemble bounded evidence context and calculate retrieval metrics.

It may not:

- authenticate a human or workload identity;
- grant or expand authority;
- generate an accepted legal or compliance conclusion;
- create a case, persist a mapping or issue a review decision;
- expose model-selectable tools;
- allocate an agent identifier;
- add graph, memory, multi-agent or workflow state;
- claim that local reports are an audit ledger or enterprise record.

## Source precedence and reconstruction

The execution controller governs sequencing; the narrative-driven master prompt governs book scope; the continuation instruction governs the requested substage; the supplied S02A handoff governs the immediate accepted architecture. The other nine S02A registers were not attached as individual files, so this overlay reconstructs them from the handoff and preserves that limitation as `ISS-019`.

## Definition of done for S02B

S02B is done only when the repository proves that authorization is applied before scoring, exact citations reconstruct from immutable source coordinates, hybrid ranking is deterministic, overlapping evidence is controlled, permission-boundary cases show zero forbidden hits, all ten artefacts are updated, the cumulative diagram agrees with code, the consistency audit passes, and no later-stage capability is claimed.
