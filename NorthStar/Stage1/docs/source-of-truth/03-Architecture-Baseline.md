# 03 - Architecture Baseline

**Architecture version:** 0.2.0  
**Maturity:** M1 - bounded single-turn assistant

## Architecture before S01

M0 consisted of the manual regulatory-change process plus `CMP-011 Source-of-Truth Governance Pack`. All runtime boundaries `CMP-001` through `CMP-010` were planned.

## S01 architectural change

- `CMP-001` is partially implemented as a local CLI.
- `CMP-002` is implemented for controlled UTF-8 text/Markdown intake and provenance.
- `CMP-003` is partially implemented as deterministic single-turn application orchestration; it is not an agent loop and does not persist workflow state.
- `CMP-008` is partially implemented through local regression/evaluation tests.
- `CMP-009` is partially implemented through local source, invocation and summary artifacts; it is not a production audit ledger.
- `CMP-010` is partially implemented as a local Python runtime and scripts.
- `CMP-004`, `CMP-005`, `CMP-006` and `CMP-007` remain planned.
- `CMP-011` remains implemented.

## Cumulative logical architecture

```mermaid
flowchart TB
    classDef human fill:#fff,stroke:#333;
    classDef planned fill:#eef5ff,stroke:#3366aa,stroke-dasharray: 5 5;
    classDef implemented fill:#e7f8ef,stroke:#1f7a4d,stroke-width:2px;
    classDef partial fill:#fff7e6,stroke:#a36500,stroke-width:2px;

    subgraph HUM[Human accountability boundary]
        MAYA[Maya Chen]:::human
        DANIEL[Daniel Brooks]:::human
        AISHA[Aisha Rahman]:::human
    end
    subgraph S01[Bounded Stage 1 assistant]
        C1[CMP-001 Analyst Experience Portal - CLI]:::partial
        C2[CMP-002 Regulatory Intake Boundary]:::implemented
        C3[CMP-003 Case and Workflow Orchestration Boundary - one request only]:::partial
        C8[CMP-008 Evaluation and Assurance Boundary - local]:::partial
        C9[CMP-009 Observability and Audit Boundary - local artifacts]:::partial
        C10[CMP-010 Runtime and Deployment Boundary - local Python]:::partial
    end
    subgraph FUT[Planned boundaries]
        C4[CMP-004 Knowledge and Evidence Access Boundary]:::planned
        C5[CMP-005 Enterprise Integration Boundary]:::planned
        C6[CMP-006 Human Review and Approval Boundary]:::planned
        C7[CMP-007 Identity Authorization and Policy Boundary]:::planned
    end
    C11[CMP-011 Source-of-Truth Governance Pack]:::implemented
    MAYA --> C1 --> C2 --> C3 --> C1 --> MAYA
    C3 --> C8
    C3 --> C9
    C10 -. hosts .-> C1
    C11 -. governs .-> S01
    DANIEL -. future approval .-> C6
    AISHA -. future approval .-> C6
    C3 -. unresolved grounding .-> C4
```

## Security boundaries

1. Publication content is untrusted.
2. Model output is untrusted until schema and evidence validation succeed.
3. Disposition and human-review fields are application-owned.
4. No enterprise identity, secrets, retrieval or action capability is exposed to the model.
5. Local artifacts are tutorial evidence, not enterprise records.

## Remaining architectural limitation

The assistant cannot access authorized NorthStar policies, controls, processes or prior assessments. Candidate affected areas are therefore hypotheses. Stage 2 must introduce grounded knowledge access without introducing tool-using agency.
