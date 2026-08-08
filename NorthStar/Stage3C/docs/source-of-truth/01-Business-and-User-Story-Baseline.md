# 01 — Business and User Story Baseline

## Context carried forward

Maya Chen can ask `AGT-001` to prepare an evidence-backed, unapproved regulatory impact package using six controlled tools. The S03B loop chooses one action at a time, validates completion outside the decision provider and stops on simple guards. It is safe but operationally weak: a transient catalogue outage, model timeout or ambiguous write ends the investigation immediately, while iteration count alone cannot control variable token use, elapsed time or cost.

## S03C narrative development

Liam O’Connor injects a temporary regulatory-catalogue failure. The first run escalates even though a registered fallback source can answer. Elena Petrov then simulates a draft-case timeout after dispatch. Retrying would risk a duplicate case, but the idempotency store can determine whether the original write committed. Maya also cancels a run and later resumes a checkpoint after a process stop. Priya Raman requires these behaviours to be deterministic and budgeted before the team converts the loop into a graph.

## Business acceptance criteria

1. A transient read failure can recover within a bounded failure/retry budget.
2. A permanent or authorization failure escalates without repeated calls.
3. A write with unknown commit status is reconciled before any retry decision.
4. A budget stop returns useful partial evidence and missing work.
5. Cancellation never reports completion.
6. Resumption does not repeat completed tool work.
7. Every recovery action is visible to Maya and reviewable by Liam/Sofia.
8. The final package remains unapproved and routed to human review.

## Scope boundary

S03C improves one local sequential run. It does not add parallelism, a workflow graph, durable distributed execution, long-term memory, human approval processing or enterprise records.
