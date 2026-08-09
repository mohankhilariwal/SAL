# Final Certification-Style Architecture Assignment

> Educational assessment only. Completion does not confer an accredited certification or prove production readiness.

## Scenario

NorthStar proposes adding a new cross-border regulatory research capability that retrieves multilingual publications and may send a controlled external notification after human approval. A vendor proposes replacing the current single-agent design with a supervisor and four specialist agents.

## Candidate deliverables

1. Business and non-functional requirement delta.
2. Updated cumulative architecture and trust-boundary diagrams.
3. Single-agent versus multi-agent decision with representative evidence plan.
4. Agent/tool/data/interface changes using stable identifiers.
5. Authority and blast-radius model for the new external action.
6. Threat model and misuse cases.
7. Evaluation dataset, metrics, judge-bias and hard-gate plan.
8. Workload, capacity, cost and SLO assumptions.
9. Failure, reconciliation, audit and recovery design.
10. RACI, runbook update and production-readiness decision.
11. At least three ADRs.
12. Explicit limitations and non-certification statement.

## Grading rubric — 100 points

| Dimension | Points | Excellent evidence |
|---|---:|---|
| Problem framing and requirements | 10 | Clear goals, non-goals, risk and success criteria. |
| Architecture coherence and diagrams | 15 | Components, flows, state and trust boundaries agree. |
| Agent/topology decision | 10 | Least complexity; measured triggers; no fashion-driven agents. |
| Identity, authorization and blast radius | 15 | Attenuated authority, receiver checks, approvals and effect limits. |
| Data, retrieval, memory and privacy | 10 | Provenance, access, retention, deletion and isolation. |
| Evaluation and assurance | 15 | Denominators, slices, hard gates, uncertainty and human calibration. |
| Reliability, observability and audit | 10 | Reconciliation, checkpoints, incidents and forensic evidence. |
| Performance, capacity and FinOps | 5 | Representative workload and cost per successful outcome. |
| Governance, RACI and readiness | 5 | Human accountability and honest blocker decision. |
| ADRs, traceability and communication | 5 | Decisions and consequences are explicit and consistent. |

### Performance levels

- **90–100:** Enterprise Agentic AI Architect readiness for supervised real-world architecture work.
- **75–89:** Senior practitioner; minor gaps in evidence or cross-domain integration.
- **60–74:** Practitioner; coherent design but material assurance or operating gaps.
- **Below 60:** Foundational understanding; redesign required before production-oriented work.

The assessor must grade evidence summaries and artefacts, not hidden chain-of-thought.
