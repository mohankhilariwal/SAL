# 01 — Business and User Story Baseline

**Version:** `0.8.0`

## Context carried forward

Maya Chen can run the one-agent regulatory impact assessment with authorized evidence, six gateway capabilities, deterministic completion, bounded budgets, typed recovery, cancellation and local checkpoint/resume. The output remains a preliminary, evidence-backed, unapproved package queued for human review.

## S04A narrative state

Liam can explain retries and resume, but he cannot review the imperative loop as a set of separately owned control states. Priya therefore introduces `GRAPH-001` so deterministic prerequisites, `AGT-001` decisions, policy preflight, gateway calls, recovery, observation and termination have explicit nodes and routes.

## Business acceptance criteria

- Maya receives the same six milestones and linked unapproved artifacts as S03C.
- Marcus can prove that policy and gateway nodes precede every action and that model output cannot mutate authority.
- Sofia can evaluate graph path coverage, forbidden transitions, termination and recovery routes independently.
- Liam can inspect and resume a graph-version-bound local checkpoint without replaying completed work.
- No new agent, memory, approval decision or production durability claim is introduced.
