# 01 — Business and User Story Baseline

**Version:** `0.3.0`  
**Current narrative point:** S02A complete; prepared corpus exists, retrieval does not.

## 1. Organization and business process

NorthStar Financial Services operates in Canada, the United States and selected European markets across banking, payments, lending and insurance-related services. Regulatory analysts must monitor publications, identify obligations, determine affected jurisdictions and business units, map obligations to policies/processes/controls, assess gaps and risk, obtain human approvals, create executive summaries and preserve evidence.

The business accountability remains human. AI may prepare evidence and recommendations but may not make a final legal conclusion, approve a control change or close a compliance case.

## 2. Personas

| ID | Persona | Responsibility relevant to S02A |
|---|---|---|
| `PER-001` | Maya Chen — Regulatory Compliance Analyst | Needs evidence-backed internal knowledge for candidate impact analysis. |
| `PER-002` | Daniel Brooks — Chief Compliance Officer | Requires explainable evidence and retains final accountability. |
| `PER-003` | Priya Raman — Enterprise Agentic AI Architect | Defines stage boundaries and selected architecture. |
| `PER-004` | Elena Petrov — AI Platform Engineer | Implements and operates the local preparation pipeline. |
| `PER-005` | Marcus Green — Cybersecurity Architect | Requires fail-closed access metadata and untrusted-data handling. |
| `PER-006` | Sofia Alvarez — AI Governance and Model Risk Lead | Requires source authority, versioning, evaluation and non-agentic truthfulness. |
| `PER-007` | Liam O’Connor — Site Reliability and AgentOps Engineer | Requires idempotent replay, atomic publication and operational evidence. |
| `PER-008` | Aisha Rahman — Business Process and Controls Owner | Supplies ownership, process/control metadata and validates authority/effective dates. |

## 3. Main user story

`US-001`: As a regulatory compliance analyst, Maya wants an AI-assisted system to analyze a new regulatory publication, identify its obligations, determine which business units, policies and controls may be affected, generate an evidence-backed impact assessment and route high-risk findings for human approval, so NorthStar can respond faster without transferring accountability to autonomous AI.

## 4. Supporting user stories

`US-002` through `US-012` remain accepted with their S01 meanings. Their detailed text was not contained in the supplied S01 handoff, so S02A does not restate or alter it. S02A traces only the following derived needs, which do not redefine those IDs:

- analysts need authorized policy/control/process evidence;
- source owners need authority, version and effective-date preservation;
- cybersecurity needs access scope before later retrieval;
- governance needs reproducible transformations and tests;
- operations needs idempotent replay and atomic corpus publication;
- approvers must continue seeing candidate evidence rather than system-owned conclusions.

## 5. Stage progression

### At the end of S01

Maya could obtain a disciplined first reading of one uploaded publication. Candidate lending, payments and customer-data labels remained hypotheses because the assistant had no internal knowledge.

### S02A narrative requirement

Before adding retrieval, NorthStar must prepare approved internal policies, controls, processes, taxonomy and prior assessments without losing ownership, authority, access, effective dates or exact citations.

### S02A outcome

Five synthetic knowledge sources are converted into 21 immutable, line-exact, access-labelled chunks. A prior-assessment fixture containing an instruction-like sentence is flagged as untrusted content. No model or retrieval query consumes the corpus.

### Next unresolved user need

Maya still cannot ask which prepared passages support a candidate impact. S02B must retrieve and rank only authorized, current evidence and return exact citations.

## 6. Business success measures for this substage

- 100% exact source-line reconstruction for generated chunks in the sample corpus.
- 100% coverage of source lines.
- 0 prepared chunks missing or differing from the source access scope.
- Stable version/chunk IDs on identical replay.
- New technical version when content or transformation changes.
- 0 model/tool/action executions from ingested document text.

These are preparation measures, not final business-outcome measures.
