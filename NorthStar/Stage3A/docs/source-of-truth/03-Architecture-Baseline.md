# 03 — Architecture Baseline

**Architecture version:** `0.5.0`

## Before S03A

S02B is a bounded retrieval/context application. `CMP-003` can initiate a fixed one-shot flow and `CMP-004` can return authorized cited evidence, but `CMP-005` has no implemented capability boundary. No `TOOL-*` or `AGT-*` exists.

See `docs/architecture/diagrams/stage-3a-architecture-before.mmd`.

## S03A architectural change

`CMP-005 Enterprise Integration Boundary` becomes partial through an application-owned tool gateway and six local adapters. The gateway is a policy-enforcement point, not an agent. It implements `INT-016`–`INT-020` and accepts `DATA-034`–`DATA-040`.

The call order is invariant:

```text
resolve exact tool/version
  -> validate input
  -> idempotency pre-check
  -> deterministic policy decision
  -> rate/circuit controls
  -> dry-run or bounded adapter invocation
  -> validate output and size
  -> idempotency commit for successful writes
  -> redacted execution event
  -> typed result envelope
```

## Cumulative architecture

```mermaid
flowchart TB
    classDef implemented fill:#e8f5e9,stroke:#2e7d32,stroke-width:1.5px;
    classDef partial fill:#fff8e1,stroke:#f57f17,stroke-width:1.5px;
    classDef planned fill:#f3f4f6,stroke:#6b7280,stroke-dasharray:5 5;
    classDef new fill:#fce4ec,stroke:#ad1457,stroke-width:2px;
    classDef external fill:#ede7f6,stroke:#5e35b1;
    MAYA["Maya Chen"]:::external --> C1["CMP-001 Analyst Experience Portal"]:::partial
    C1 --> C3["CMP-003 deterministic orchestration caller\nno agent loop"]:::partial
    C3 --> GW["CMP-005 Tool Gateway"]:::new
    GW --> REG["INT-016 registry + TOOL-001..006"]:::new
    REG --> VAL["strict input/output validation"]:::new
    VAL --> PDP["INT-018 local deterministic policy"]:::new
    PDP --> CTRL["idempotency, timeout, rate, circuit, retry, dry-run"]:::new
    CTRL --> ADP["INT-019 adapters"]:::new
    ADP --> C4["CMP-004 authorized retrieval"]:::implemented
    ADP --> LOCAL["synthetic catalogues and reversible local store"]:::new
    GW --> C9["CMP-009 local execution evidence\nnot audit ledger"]:::partial
    C7["CMP-007 enterprise IAM/PDP planned"]:::planned -. local claims .-> PDP
    C6["CMP-006 approval service planned"]:::planned
    LOCAL -. queued record only .-> C6
    C8["CMP-008 tool evaluation"]:::new --> GW
    C10["CMP-010 local Python runtime"]:::partial --> GW
    C11["CMP-011 governance pack 0.5.0"]:::implemented --> REG
    AGT["No AGT-*; S03B deferred"]:::planned -. no direct call .-> GW
```

## Trust and deployment boundaries

- Descriptors are trusted change-controlled configuration for the local stage.
- Caller principal attributes are constrained but unauthenticated.
- Evidence returned by `TOOL-003` remains untrusted data and retains S02B filtering.
- Adapters are inside the local process; no remote server authentication, network policy or service identity is proven.
- Local store and event log are tutorial artefacts, not enterprise systems of record or audit.

## Deferred architecture

`DATA-009 AgentRunState`, `DATA-010 AuthorizationGrant`, accepted `DATA-002 RegulatoryCase`, human approval processing, durable checkpoints, model action selection, graph execution, MCP/A2A, memory and multi-agent behavior remain unimplemented.
