# 08 - Risk, Assumption and Issue Register

| Field | Value |
|---|---|
| Version | 0.1.0 |
| Baseline date | 2026-07-31 |
| Status | Active |

## 1. Risk register

| ID | Risk | Likelihood | Impact | Owner | Response | Status |
|---|---|---|---|---|---|---|
| RSK-001 | Scope growth causes stages to become unbounded or superficial. | High | High | Priya | Split at natural architecture boundaries; preserve depth and handoff. | Open |
| RSK-002 | Names, IDs, schemas or diagrams drift across stages. | Medium | High | Priya | Source-of-truth artefacts, validator, ADR-controlled changes. | Controlled |
| RSK-003 | Readers mistake an assistant, workflow or model call for a production agent. | High | Medium | Priya/Sofia | Explicit maturity labels and capability definitions. | Open for S01 |
| RSK-004 | AI output is treated as legal or compliance authority. | Medium | Critical | Daniel/Sofia | Human accountability, disclaimers, approval gates and policy. | Open throughout |
| RSK-005 | Hallucinated or weakly grounded findings enter assessments. | High | High | Maya/Sofia | Evidence-first design, retrieval, uncertainty and evaluation. | Open for S01/S02 |
| RSK-006 | Sensitive or cross-case data leaks through prompts, retrieval, memory or telemetry. | Medium | Critical | Marcus | Classification, isolation, scoped access, redaction and security tests. | Open for S02/S05/S09 |
| RSK-007 | Agent or tool authority exceeds user intent or case purpose. | Medium | Critical | Marcus | Deny by default, attenuated delegation, tool policies and approvals. | Open for S03/S09 |
| RSK-008 | Runtime loops create excessive cost, latency or repeated side effects. | Medium | High | Elena/Liam | Budgets, termination, idempotency, checkpoints and monitoring. | Open for S03/S07/S10 |
| RSK-009 | Multi-agent design increases complexity without measurable value. | Medium | High | Priya | Compare one agent, graph nodes and multiple agents using evidence. | Open for S06 |
| RSK-010 | Vendor or library changes break code or invalidate claims. | High | Medium | Elena | Official documentation verification, pinned versions, adapters and compatibility tests. | Open in implementation stages |
| RSK-011 | Evaluation data is unrealistic, biased, contaminated or too small. | Medium | High | Sofia | Dataset governance, edge/adversarial cases, human calibration and versioning. | Open for S08 |
| RSK-012 | LLM judges create false confidence or bias. | High | High | Sofia | Deterministic checks first, calibration, bias tests, multiple judges and human review. | Open for S08 |
| RSK-013 | Reviewer fatigue or automation bias causes rubber-stamp approval. | Medium | High | Daniel/Sofia | Risk-based queues, evidence-first UI, workload metrics and sampling. | Open for S04/S08 |
| RSK-014 | Audit data is incomplete, mutable or contains protected information. | Medium | High | Marcus/Liam | Structured events, append-only design, redaction, integrity and retention controls. | Open for S10 |
| RSK-015 | Performance and cost targets are invented before workload evidence exists. | High | Medium | Elena/Liam | Provisional NFRs, realistic distributions and measured benchmarks. | Controlled |
| RSK-016 | Control plane becomes a bottleneck or single point of failure. | Medium | High | Priya/Liam | Separate administration from cached runtime enforcement; design resilience. | Open for S09/S10 |
| RSK-017 | Tutorial source conflict produces inconsistent stage scope. | Medium | High | Priya | ADR-001 precedence and one canonical roadmap. | Resolved for baseline |
| RSK-018 | Early labs accidentally use production confidential data. | Low | Critical | Marcus/Sofia | Synthetic/approved data only, explicit environment boundary. | Open |

## 2. Assumptions

| ID | Assumption | Owner | Validation point | Status |
|---|---|---|---|---|
| ASM-001 | Early labs run locally on a development machine with modest resources. | Elena | S01 | Accepted for baseline |
| ASM-002 | Synthetic or approved sample regulatory and policy documents are available. | Maya | S01/S02 | To validate |
| ASM-003 | Human review roles and separation-of-duties rules can be represented in test data. | Daniel | S04 | To validate |
| ASM-004 | Enterprise repositories can later expose typed APIs, files, search or adapters. | Aisha/Priya | S02/S03 | To validate |
| ASM-005 | Paid model services are optional for early labs and local/mock alternatives are acceptable. | Elena | S01 | Accepted for baseline |
| ASM-006 | Regulatory and legal specialists remain responsible for authoritative interpretation. | Daniel | All stages | Accepted invariant |
| ASM-007 | Exact SLOs and capacity targets require measured workloads rather than being fixed in Stage 0. | Liam | S07 | Accepted for baseline |
| ASM-008 | A single repository can support the tutorial through the capstone. | Priya | Review each stage | Accepted, ADR-004 |
| ASM-009 | English is the initial implementation language; multilingual requirements are evaluated later. | Maya | S01/S08 | Open assumption |
| ASM-010 | The conceptual component boundaries can initially be implemented within one local process. | Priya | S01-S04 | Accepted, ADR-007 |

## 3. Issues

| ID | Issue | Resolution | Status |
|---|---|---|---|
| ISS-001 | Source documents contain different output sequences: an earlier complete master uses eight stages, the narrative-driven master uses eleven stages, and the controller requires Stage 0 first. | ADR-001 establishes controller precedence and canonical S00-S11 roadmap. | Resolved |
| ISS-002 | No approved real NorthStar documents or enterprise schemas exist because the organization is fictional. | Use synthetic, attributable fixtures and label them as tutorial data. | Open for S01/S02 |
| ISS-003 | Exact production SLOs, volumes, model choices and costs are unknown. | Keep targets provisional until S07 workload and benchmark evidence. | Open |
| ISS-004 | Full Mermaid rendering was not performed in Stage 0. | Structural checks only; add approved Mermaid renderer and render validation in a later stage. | Open, recorded exception |
| ISS-005 | Legal and regulatory framework mappings will change over time. | Verify primary sources at execution time and require qualified review. | Open throughout |
| ISS-006 | Python baseline was previously 3.12 while Stage 0 tests ran on 3.13.5. | Baseline upgraded to Python 3.13 and verified on Python 3.13.5. | Closed |

## 4. Change history

| Date | Change | Related decision |
|---|---|---|
| 2026-07-31 | Initial risk, assumption and issue baseline created. | ADR-001 through ADR-007 |
