# ADR-039 — Bind a Context Policy Profile Without Adding Memory or Compaction

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

The user requested specification and context engineering, but the accepted S04C handoff requires formal agent specification before context compaction or memory. `DATA-065` already provides authorized, bounded context.

## Decision

Add `DATA-077 ContextPolicyProfile` inside `DATA-071`. It formalizes the existing allowed context kinds, authorization-before-load, provenance/hash requirements, deterministic ordering and item/character budgets. It explicitly prohibits memory kinds, cross-case reuse and compaction/regeneration in S05A.

## Alternatives

- Omit context from the specification.
- Add long-term memory now.
- Add automatic summarization/compaction now.
- Let prompts decide what context to keep.
- Treat every workspace/checkpoint record as memory.

## Rationale

The profile makes current context boundaries testable without introducing the unresolved retention, privacy, deletion, poisoning, temporal-validity and regeneration semantics of memory.

## Consequences

- Context policy drift fails closed.
- Long histories may exceed the current 8-item/12,000-character budget and require escalation or a new run.
- Stage 5B must design context lifecycle, compaction and memory boundaries before enabling any memory flag.

## Review triggers

Need for long-history continuation, context compaction, summarization, semantic/episodic/user memory, cross-session recall, deletion or consent management.
