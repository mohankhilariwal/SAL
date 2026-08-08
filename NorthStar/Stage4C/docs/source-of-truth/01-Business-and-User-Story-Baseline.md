# 01 — Business and User Story Baseline

**Version:** `1.0.0`

## 1. Context carried forward

Maya's regulatory impact workflow can already produce a complete evidence-backed, reversible, unapproved package; queue a review; persist a durable wait; accept a validated Daniel decision; expire unanswered reviews; and resume without repeating `TOOL-006`. The S04B baseline explicitly leaves the harness unimplemented and identifies scattered cross-cutting runtime wiring as the next problem.

## 2. Narrative development

Priya asks Elena to reproduce yesterday's approved demonstration in a clean process. Elena must manually remember which instruction file to load, which context filters to run, which registries to wire, which validators to call, which workspace files are safe, which trace fields must be redacted and how the approval service joins the graph. The graph is correct, but the application that surrounds it is easy to assemble inconsistently.

Marcus points out that a longer system prompt cannot solve this. A prompt cannot stop a forbidden loader from reading text, freeze a tool registry, enforce a workspace root, verify a checksum, redact credentials or ensure a decision is single-use. Sofia adds that an evaluation callback must observe behavior without becoming another hidden decision-maker. Liam needs one restartable lifecycle with correlated session, run and trace evidence.

Priya therefore introduces a harness only around the existing single-agent graph. It standardizes assembly and lifecycle controls while leaving business reasoning, graph routes, tool authority, durable waits and human decisions with their accepted owners.

## 3. User-story impact

`US-001`–`US-012` remain unchanged. S04C primarily strengthens the quality attributes required to satisfy them consistently:

- Maya receives the same bounded, attributable context and preliminary result across runs.
- Daniel's decision remains external and typed; the harness cannot manufacture it.
- Priya gains a framework-neutral, versioned composition boundary.
- Elena gains a reproducible bootstrap and workspace lifecycle.
- Marcus gains deterministic access-before-context, immutable registries and secret-safe artefacts.
- Sofia gains explicit validators and observer-only evaluation hooks.
- Liam gains session/run/trace correlation and restart checks.
- Aisha's accountability remains outside autonomous completion.

## 4. Acceptance criteria for this stage

1. One manifest binds `AGT-001`, `GRAPH-001` 1.1.0, `TOOL-001`–`006`, instruction, validators and hooks.
2. Instruction drift and future-stage flags fail closed.
3. Unauthorized context loaders are never invoked.
4. The bounded context envelope records provenance, hashes, truncation and omission.
5. Session workspaces are contained, quota-limited and free of raw approval tokens.
6. Harness start reaches the existing durable wait; resume follows existing approved/rejected/expired routes.
7. Tool side effects remain one after resume.
8. Trace evidence is correlated and redacted but not called audit.
9. Exactly one agent exists and no memory/concurrent branch package is introduced.

## 5. Business outcome now enabled

NorthStar can run the same controlled single-agent workflow through one repeatable lifecycle contract rather than bespoke factory wiring. This reduces configuration drift and test gaps; it does not yet prove production SLOs, legal correctness, enterprise identity, memory or multi-agent value.

## 6. Next unresolved business need

The harness can consistently enforce the controls it has been given, but the agent's purpose, goals, non-goals, preconditions, invariants, authority tier, error semantics, SLOs and retirement criteria are still distributed across code, prose and tests. Formal specification is required before adding context/memory behavior that could persist beyond one bounded session.
