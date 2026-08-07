# 02 - Requirements Register

| Field | Value |
|---|---|
| Version | 0.1.0 |
| Baseline date | 2026-07-31 |
| Status | Baseline candidate |

## 1. Requirement lifecycle

Statuses: `Proposed`, `Accepted`, `Implemented`, `Verified`, `Deferred`, `Retired`.

Stage 0 accepts business and architecture requirements but does not claim runtime implementation. Numeric service levels are provisional until workload evidence is collected.

## 2. Functional requirements

| ID | Requirement | Priority | Source | Acceptance intent | Status |
|---|---|---:|---|---|---|
| FR-001 | Register a regulatory publication and preserve original content, source, publication date, retrieval time, jurisdiction and provenance. | Must | US-001, US-002 | A case can reproduce the exact source used for analysis. | Accepted |
| FR-002 | Classify publication relevance, regulatory domain, jurisdiction and affected legal entities with uncertainty recorded. | Must | US-001 | Classification is structured and reviewable. | Accepted |
| FR-003 | Extract candidate obligations as discrete, source-linked records rather than only prose summaries. | Must | US-001, US-003 | Each obligation includes text span, source location and confidence. | Accepted |
| FR-004 | Retrieve internal policies, processes, controls, taxonomies, business-unit metadata and prior assessments subject to access controls. | Must | US-001, US-004 | Retrieved evidence is attributable and permission filtered. | Accepted |
| FR-005 | Map obligations to affected jurisdictions, legal entities, business units, policies, processes and controls. | Must | US-001, US-004 | Mappings include evidence, rationale summary, confidence and reviewer state. | Accepted |
| FR-006 | Identify candidate control gaps, conflicts, missing evidence and uncertainty. | Must | US-001 | The system can return `insufficient_evidence` instead of fabricating certainty. | Accepted |
| FR-007 | Produce a structured impact assessment containing findings, evidence, risk, urgency, confidence and recommended next actions. | Must | US-001 | Output validates against a versioned schema. | Accepted |
| FR-008 | Create and maintain a regulatory-change case with status, ownership, history and durable artefacts. | Must | US-001, US-008 | Case state can be resumed and audited. | Accepted |
| FR-009 | Route work for risk-based human review, approval, rejection, override, escalation and rework. | Must | US-005 | High-risk or irreversible decisions cannot complete without required approval. | Accepted |
| FR-010 | Draft remediation actions, assign accountable owners, track due dates and retain closure evidence. | Should | US-011 | Approved gaps become traceable actions. | Accepted |
| FR-011 | Generate executive summaries only from approved findings and evidence. | Should | US-010 | Summary cannot introduce unapproved material conclusions. | Accepted |
| FR-012 | Produce a tamper-evident audit evidence package containing sources, versions, actions, policy decisions, approvals and final disposition. | Must | US-012 | Independent reconstruction is possible without hidden chain-of-thought. | Accepted |
| FR-013 | Enforce identity, authorization, purpose, resource and data scopes for every access and action. | Must | US-007 | Denied operations fail closed and are logged. | Accepted |
| FR-014 | Search, filter and report case status, history, findings, remediation and approvals according to role. | Should | US-001 | Users see only authorized cases and fields. | Accepted |
| FR-015 | Configure workflow, policy, routing, budget and approval rules through versioned controlled artefacts. | Must | US-006, US-009 | Changes are reviewable, testable and auditable. | Accepted |
| FR-016 | Capture evaluation inputs, outputs, traces, labels and outcomes for offline and online assurance. | Must | US-006 | Evaluation evidence links to versions and requirements. | Accepted |
| FR-017 | Support incident containment, cancellation, quarantine, emergency stop and controlled recovery. | Must | US-007, US-008 | Unsafe or failing execution can be halted and reconstructed. | Accepted |
| FR-018 | Integrate external and internal systems through versioned, typed contracts with explicit error semantics. | Must | US-009 | Interfaces can evolve without silent breakage. | Accepted |
| FR-019 | Distinguish source fact, system inference, human decision and unresolved uncertainty in user-visible outputs and audit records. | Must | US-001, US-012 | Every material field has provenance and decision origin. | Accepted |
| FR-020 | Preserve a complete change history for architecture, agent, prompt, model, tool, policy, schema and evaluation versions. | Must | US-006, US-009 | A run can be tied to the exact configuration used. | Accepted |

## 3. Non-functional requirements

| ID | Requirement | Initial target or rule | Validation stage | Status |
|---|---|---|---|---|
| NFR-001 | Human accountability | Named human owners retain regulated decision authority; no anonymous approval. | S01 onward | Accepted |
| NFR-002 | Evidence and explainability | 100% of approved material findings link to accessible evidence and concise rationale. | S02, S08 | Accepted |
| NFR-003 | Security and least privilege | Deny by default; permissions scoped by user, agent, purpose, tool, operation, resource, case and time. | S03, S09 | Accepted |
| NFR-004 | Privacy and minimization | Collect and expose only data required for the case; redact protected fields in telemetry. | S02, S09, S10 | Accepted |
| NFR-005 | Case and tenant isolation | No cross-case or cross-user leakage in retrieval, memory, state or traces. | S02, S05, S09 | Accepted |
| NFR-006 | Availability | Production SLO to be evidence-based; critical review and audit data remain accessible during approved degraded modes. | S07, S10 | Accepted |
| NFR-007 | Interactive responsiveness | Non-model UI and status operations target P95 <= 2 seconds under the validated workload; model workflow targets are workload specific. | S07 | Provisional |
| NFR-008 | Throughput and scalability | Capacity must be based on document size, model calls, tool latency and concurrent cases, not a single fixed-token benchmark. | S07 | Accepted |
| NFR-009 | Durability and recovery | Accepted state and approvals survive process failure; recovery avoids duplicate side effects. | S04, S10 | Accepted |
| NFR-010 | Audit integrity | Material audit events are append-only and tamper evident in production architecture. | S09, S10 | Accepted |
| NFR-011 | Observability | Correlated logs, metrics, traces and events cover user, run, task, agent, model, retrieval, tool, policy and approval actions. | S10 | Accepted |
| NFR-012 | Portability | Core domain, data and policy contracts are vendor neutral; integrations are replaceable adapters. | All stages | Accepted |
| NFR-013 | Maintainability | Modules have clear ownership, bounded responsibilities and versioned contracts. | All stages | Accepted |
| NFR-014 | Testability | Every accepted capability traces to executable tests or an explicitly scheduled evaluation. | All stages | Accepted |
| NFR-015 | Cost governance | Measure cost per request, workflow, completed task, failed run and human escalation; enforce budgets when agents are introduced. | S03, S07, S10 | Accepted |
| NFR-016 | Performance reproducibility | Benchmarks record model, hardware, ISL/OSL distributions, concurrency, cache state and tool latency. | S07 | Accepted |
| NFR-017 | Data residency | Data placement and model routing respect approved jurisdiction and contractual restrictions. | S07, S09, S10 | Accepted |
| NFR-018 | Usability and accessibility | Evidence, confidence, uncertainty and approval actions are understandable and accessible to intended personas. | S01, S04 | Accepted |
| NFR-019 | Version and compatibility control | Schemas, APIs, graphs, prompts, tools and models are versioned with migration and rollback paths. | S04 onward | Accepted |
| NFR-020 | Change assurance | Model, prompt, policy, tool and data changes pass defined regression and governance gates before promotion. | S08, S10 | Accepted |
| NFR-021 | Graceful degradation | A dependency failure produces a safe partial result, retry, queue, escalation or stop rather than fabricated completion. | S03, S10 | Accepted |
| NFR-022 | No hidden reasoning retention | Audit stores concise evidence summaries, actions and decisions, not hidden model chain-of-thought. | All stages | Accepted |

## 4. Foundational policies and controls

| ID | Policy | Linked control |
|---|---|---|
| POL-001 | Human Accountability Policy | CTL-001 requires named human approval at defined risk thresholds. |
| POL-002 | Evidence and Provenance Policy | CTL-002 rejects approval of material findings without valid evidence links. |
| POL-003 | Least-Privilege Tool Policy | CTL-003 enforces deny-by-default and scoped tool authorization. |
| POL-004 | Data Minimization and Isolation Policy | CTL-004 filters retrieval, state, memory and telemetry by authorized scope. |
| POL-005 | Change and Version Control Policy | CTL-005 requires versioned artefacts, tests, ADRs and promotion evidence. |
| POL-006 | Safe Failure Policy | CTL-006 stops, degrades or escalates when critical dependencies or controls fail. |
| POL-007 | Audit Evidence Policy | CTL-007 records attributable actions, sources, versions, approvals and disposition. |
| POL-008 | No Hidden Chain-of-Thought Policy | CTL-008 stores concise decision evidence but not private model reasoning. |

## 5. Baseline traceability matrix

At Stage 0, runtime implementation is intentionally absent. `Planned component` indicates the architectural boundary expected to own the requirement; later stages may refine the component through ADR-controlled change.

| Requirement | User stories | Planned component(s) | Control | Planned verification |
|---|---|---|---|---|
| FR-001 | US-001, US-002 | CMP-002, CMP-003 | CTL-002, CTL-007 | TEST-101, EVAL-101 in S01 |
| FR-002 | US-001 | CMP-003, CMP-004 | CTL-002 | EVAL-102 in S01/S02 |
| FR-003 | US-001, US-003 | CMP-003, CMP-004 | CTL-002 | EVAL-201 in S02 |
| FR-004 | US-001, US-004 | CMP-004, CMP-005, CMP-007 | CTL-003, CTL-004 | TEST-201, EVAL-202 in S02 |
| FR-005 | US-001, US-004 | CMP-003, CMP-004, CMP-005 | CTL-002 | EVAL-203 in S02/S03 |
| FR-006 | US-001 | CMP-003, CMP-008 | CTL-002, CTL-006 | EVAL-204 in S02/S03 |
| FR-007 | US-001 | CMP-003, CMP-001 | CTL-002 | TEST-102 in S01 |
| FR-008 | US-001, US-008 | CMP-003, CMP-010 | CTL-006, CTL-007 | TEST-301 in S03/S04 |
| FR-009 | US-005 | CMP-006, CMP-007 | CTL-001, CTL-003 | TEST-401 in S04 |
| FR-010 | US-011 | CMP-005, CMP-006 | CTL-001, CTL-007 | TEST-402 in S04/S10 |
| FR-011 | US-010 | CMP-003, CMP-001 | CTL-002 | EVAL-301 in S03/S08 |
| FR-012 | US-012 | CMP-009 | CTL-007, CTL-008 | TEST-901 in S09/S10 |
| FR-013 | US-007 | CMP-007 | CTL-003, CTL-004 | TEST-902 in S09 |
| FR-014 | US-001 | CMP-001, CMP-003 | CTL-004 | TEST-103 in S01 |
| FR-015 | US-006, US-009 | CMP-007, CMP-008, CMP-010 | CTL-005 | TEST-801 in S08/S10 |
| FR-016 | US-006 | CMP-008, CMP-009 | CTL-005, CTL-007 | EVAL-801 in S08 |
| FR-017 | US-007, US-008 | CMP-007, CMP-010 | CTL-006 | TEST-1001 in S10 |
| FR-018 | US-009 | CMP-005, CMP-010 | CTL-005 | TEST-302 in S03 onward |
| FR-019 | US-001, US-012 | CMP-001, CMP-003, CMP-009 | CTL-002, CTL-007 | TEST-104, EVAL-802 |
| FR-020 | US-006, US-009 | CMP-008, CMP-009, CMP-010 | CTL-005, CTL-007 | TEST-802, TEST-1002 |

## 6. Stage 0 validation requirements

| ID | Objective | Expected result |
|---|---|---|
| TEST-001 | Verify all ten source-of-truth artefacts exist. | All files present at canonical paths. |
| TEST-002 | Verify required Stage 0 headings and handoff sections exist. | No missing required headings. |
| TEST-003 | Verify stable identifier formats and detect conflicting duplicate definitions. | No invalid or conflicting IDs. |
| TEST-004 | Verify component names in the architecture baseline exist in the catalogue. | All referenced component IDs are catalogued. |
| TEST-005 | Verify no agent is claimed as implemented in Stage 0. | Agent inventory is empty and planned agents are not instantiated. |
| TEST-006 | Verify repository manifest paths exist. | Manifest matches created repository files. |
| TEST-007 | Perform a structural Mermaid audit. | Code fences and basic graph declarations are well formed; renderer validation remains pending. |
