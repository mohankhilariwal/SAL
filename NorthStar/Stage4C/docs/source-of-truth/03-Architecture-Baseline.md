# 03 — Architecture Baseline

**Architecture version:** `1.0.0`  
**Graph compatibility:** `GRAPH-001` `1.1.0` unchanged.

## 1. Maturity before S04C

The 0.9.0 system is a bounded single-agent, typed, sequential graph with gateway-only tools, budgets/recovery/reconciliation, durable SQLite workflow state, external human decision events, expiry and lease-protected resume. Cross-cutting assembly and lifecycle responsibilities remain scattered across factories, modules, configuration and tests.

## 2. Architectural change

S04C adds a framework-neutral compositional harness *inside the existing `CMP-003` orchestration and `CMP-010` runtime responsibilities*. It is not a new top-level component. The harness owns bootstrap, version binding, instruction/context assembly, immutable registries, session/workspace lifecycle, cross-cutting validation, observer hooks and trace correlation. It delegates rather than absorbs:

- graph route/state ownership to `CMP-003`/`GRAPH-001`;
- tool authority and effects to `CMP-005`;
- human decision validation to `CMP-006`/`CMP-007`;
- durable state/lease to `CMP-010`;
- evaluation findings to `CMP-008`;
- trace evidence to `CMP-009`.

## 3. Cumulative logical architecture

```mermaid
flowchart TB
  classDef human fill:#fff,stroke:#333
  classDef existing fill:#eef5ff,stroke:#3366aa
  classDef new fill:#fff2cc,stroke:#aa6a00,stroke-width:2px
  classDef external fill:#f6f6f6,stroke:#777,stroke-dasharray:5 5

  subgraph H[Human accountability boundary]
    MAYA[Maya Chen]:::human
    DANIEL[Daniel Brooks]:::human
    AISHA[Aisha Rahman]:::human
  end

  subgraph NS[NorthStar AI-assisted system]
    C1[CMP-001 Analyst Experience Portal]:::existing
    C2[CMP-002 Regulatory Intake Boundary]:::existing
    C3[CMP-003 Case and Workflow Orchestration Boundary]:::existing
    HAR[Stage 4C framework-neutral harness<br/>manifest + instructions + context + registries<br/>sessions/workspace + validators + hooks]:::new
    G[GRAPH-001 v1.1.0<br/>typed sequential graph]:::existing
    C4[CMP-004 Knowledge and Evidence Access Boundary]:::existing
    C5[CMP-005 Enterprise Integration Boundary<br/>TOOL-001..006 gateway]:::existing
    C6[CMP-006 Human Review and Approval Boundary]:::existing
    C7[CMP-007 Identity Authorization and Policy Boundary]:::existing
    C8[CMP-008 Evaluation and Assurance Boundary]:::existing
    C9[CMP-009 Observability and Audit Boundary<br/>local trace evidence only]:::existing
    C10[CMP-010 Runtime and Deployment Boundary<br/>SQLite + workspace + lease]:::existing
    C11[CMP-011 Source-of-Truth Governance Pack]:::existing
  end

  EXT[Regulatory and enterprise sources]:::external

  MAYA --> C1 --> C2 --> HAR
  EXT --> C2
  HAR --> C4
  HAR --> C7
  HAR --> G
  G --> C5
  G --> C6
  DANIEL --> C6
  AISHA -. future risk-based approval .-> C6
  HAR --> C8
  HAR --> C9
  HAR --> C10
  G --> C10
  C6 --> C10
  C11 -. constrains versions and contracts .-> HAR
```

The new yellow boundary packages existing runtime responsibilities. It does not add a new agent, graph branch or authority path.

## 4. Harness lifecycle

```mermaid
sequenceDiagram
  participant Maya
  participant Harness
  participant Context as CMP-004/CMP-007
  participant Graph as GRAPH-001 1.1.0
  participant Gateway as CMP-005
  participant Approval as CMP-006
  participant Store as CMP-010
  participant Trace as CMP-009

  Maya->>Harness: start(request)
  Harness->>Harness: verify manifest + instruction hash
  Harness->>Context: authorize before source loader
  Context-->>Harness: DATA-065 bounded context
  Harness->>Store: create DATA-066/067 session workspace
  Harness->>Trace: harness.start
  Harness->>Graph: start(digests, session, run)
  Graph->>Gateway: TOOL-006 via INT-017
  Gateway-->>Graph: idempotent review request
  Graph->>Approval: persist wait/token digest
  Graph->>Store: DATA-058/059 checkpoint
  Graph-->>Harness: waiting at N80
  Harness-->>Maya: DATA-070 + transient callback token
  Note over Harness,Store: raw token is not persisted in workspace/DB
  Approval-->>Store: validated DATA-007 decision event
  Maya->>Harness: resume(session, run)
  Harness->>Harness: verify manifest/session binding
  Harness->>Graph: resume with lease
  Graph-->>Harness: approved/rejected/expired preliminary outcome
  Harness->>Trace: completion event + observer hook findings
```

## 5. Trust boundaries

- Instruction and model output are untrusted for authority.
- Context content is data, not executable instruction; authorization precedes loading.
- Registries and manifest are trusted configuration only after integrity validation.
- Approval token is transient; only digest/nonce/correlation are durable.
- Workspace and trace are local operational artefacts, not records or audit.
- Hooks receive summaries and return findings; they are outside control flow.

## 6. Deployment boundary

One Python process composes the harness and sequential graph. SQLite and local files remain the only persistence. Enterprise production mapping may replace adapters with managed registries, policy engines, secret stores, durable workflow engines, sandboxed workspace services and OpenTelemetry exporters while preserving `INT-041`–`046`.
