# 01 — Business and User Story Baseline

**Version:** `0.6.0`

## Carried-forward business objective

As a regulatory compliance analyst, Maya Chen wants an AI-assisted system to analyze a new regulatory publication, identify candidate obligations and affected policies/controls, prepare an evidence-backed impact assessment and route high-risk findings for human approval without transferring accountability to autonomous AI.

`US-001`–`US-012` remain accepted without renaming or renumbering.

## Narrative state after S03A

NorthStar had six safe local capabilities behind `CMP-005 Tool Gateway`, but their invocation order was hard-coded. The system could not receive a goal, choose the next allowed capability from observed state, detect completion or return control when progress failed.

## S03B business increment

Maya may now submit one bounded goal: prepare a preliminary impact package for one accepted publication. `AGT-001` can:

1. find candidate regulatory catalogue records;
2. retrieve only Maya-authorized internal evidence;
3. identify candidate controls;
4. create a reversible `draft_unapproved` case;
5. save a `candidate_unapproved` mapping; and
6. queue a human review request.

The system still cannot make a legal conclusion, approve a finding, change a control, notify external recipients, assign remediation or close a case.

## Persona responsibilities in this stage

| Persona | S03B responsibility |
|---|---|
| Maya Chen | Supplies the goal and remains the analyst who receives the draft or escalation. |
| Daniel Brooks | Retains accountability; no approval decision is simulated. |
| Priya Raman | Defines the bounded loop, agent authority and deterministic completion semantics. |
| Elena Petrov | Implements the provider-neutral decision contract and local runtime. |
| Marcus Green | Requires gateway-only actions, trusted principal injection and negative authority tests. |
| Sofia Alvarez | Requires termination-accuracy evaluation and no false success from model-declared completion. |
| Liam O’Connor | Requires explicit terminal reasons and points out the remaining recovery/checkpoint gap. |
| Aisha Rahman | Remains a future business-control reviewer; no control change is authorized. |

## Business acceptance criteria

- A successful run produces one case, mapping and review request that remain unapproved.
- A premature `complete` decision is escalated, not accepted.
- A denied/failed tool call produces a non-success terminal outcome.
- Every terminal run explains why it stopped and what partial milestones exist.
- Restricted evidence remains absent from Maya's observations.

## Current user-story status

The main story is partially advanced: evidence discovery and preparation of an unapproved review package are locally demonstrated. Human review, accepted mappings, remediation and closure remain unimplemented.

## Next narrative problem

The minimal loop stops safely but does not yet handle multi-dimensional budgets, transient recovery, model/tool fallback, cancellation, ambiguous writes, checkpoint/restart or compensation. Those concerns are reserved for S03C.
