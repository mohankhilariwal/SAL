# 00 - Project Constitution

**Architecture version:** 0.2.0  
**Repository version:** 0.2.0  
**Last accepted stage:** S01

## Purpose and invariant

The NorthStar Agentic AI Architecture Playbook evolves one regulated-enterprise user story through the simplest sufficient capability. AI output remains advisory; named humans retain accountability. Critical authorization, privacy, legal, financial and irreversible-action controls remain deterministic and external to model instructions.

## Accepted names and personas

NorthStar Financial Services; Maya Chen, Daniel Brooks, Priya Raman, Elena Petrov, Marcus Green, Sofia Alvarez, Liam O'Connor and Aisha Rahman.

## Source precedence and change control

The execution controller governs sequencing; the narrative-driven master governs the story and scope. The ten files in `docs/source-of-truth/` remain authoritative. Existing identifiers are not renamed or renumbered without impact analysis and a superseding ADR.

## Stage 1 constitution update

S01 implements a bounded, single-turn preliminary summarizer using `CMP-001`, `CMP-002`, `CMP-003`, `CMP-008`, `CMP-009` and `CMP-010` in constrained local form. `CMP-011` remains the implemented governance pack. No agent, RAG, tool, graph, memory or production control plane is implemented.

Model-generated fields cannot set approval, final disposition or legal conclusion. The application fixes `preliminary_unapproved`, `human_review_required=true`, `approval_status=not_requested` and `legal_conclusion=not_provided`.

## Technology and verification rule

The runtime is Python-standard-library only. The accepted baseline is Python 3.13; the package is verified on Python 3.13.5. Optional provider adapters are isolated and not counted as live-verified unless a credentialed call is recorded.

## Definition of done for S01

- One controlled publication can be ingested and hashed.
- One structured preliminary summary can be produced through the model contract.
- Exact source-line evidence is validated outside the model.
- Mandatory human-review status cannot be overridden by model output.
- Local artifacts and invocation metadata are persisted.
- Tests and validation execute successfully.
- All ten artefacts and the cumulative architecture are updated.
- The handoff authorizes only Stage 2 retrieval work.
