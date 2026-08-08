# 04 — Component and Agent Catalogue

**Version:** `0.3.0`

## 1. Component inventory

| ID | Name | S02A responsibility/status |
|---|---|---|
| `CMP-001` | Analyst Experience Portal | Partial local CLI from S01; unchanged. |
| `CMP-002` | Regulatory Intake Boundary | Implemented for bounded S01 publication input; unchanged. |
| `CMP-003` | Case and Workflow Orchestration Boundary | Partial one-shot flow; no case/workflow state and no S02A corpus query. |
| `CMP-004` | Knowledge and Evidence Access Boundary | **Partial:** approved manifest validation, bounded parsing, provenance, chunking, immutable prepared corpus and local validation. No search/retrieval/reranking/context assembly. |
| `CMP-005` | Enterprise Integration Boundary | Planned; no live source connector or change feed. |
| `CMP-006` | Human Review and Approval Boundary | Planned; S01 status semantics only. |
| `CMP-007` | Identity, Authorization and Policy Boundary | Planned; local access strings are metadata, not authenticated authorization. |
| `CMP-008` | Evaluation and Assurance Boundary | Partial: S01 tests retained conceptually; S02A corpus integrity/evaluation tests implemented. |
| `CMP-009` | Observability and Audit Boundary | Partial: local ingestion run and provenance artifacts; not audit ledger. |
| `CMP-010` | Runtime and Deployment Boundary | Partial local Python runtime. |
| `CMP-011` | Source-of-Truth Governance Pack | Implemented and updated to `0.3.0`. |

## 2. `CMP-004` detailed responsibilities

### Implemented

- validate source descriptors and access scopes;
- constrain paths to approved root;
- parse strict UTF-8 text/Markdown;
- preserve raw and normalized SHA-256;
- record source version, owner, authority, dates, domains and jurisdiction;
- flag limited suspicious instruction/credential patterns;
- create deterministic structure-aware line chunks;
- propagate access and source metadata;
- atomically persist immutable version packages;
- preserve active and historical versions;
- emit run records and support independent validation.

### Prohibited or deferred

- authenticated identity or policy decision;
- query execution;
- search index or embeddings;
- reranking;
- context assembly;
- model invocation;
- tool execution;
- case/state updates;
- final impact or legal conclusions.

## 3. Agent inventory

None. No `AGT-*` identifier is allocated. The preparation service follows a fixed deterministic procedure. It does not choose goals/actions, observe tools, replan, loop semantically, delegate or own authority.

## 4. Tool inventory

None. No `TOOL-*` identifier is allocated. `INT-009`–`INT-011` are application/service interfaces and cannot be selected by a model.
