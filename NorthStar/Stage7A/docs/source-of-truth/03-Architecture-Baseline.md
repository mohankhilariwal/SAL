# 03 — Architecture Baseline (Reconstructed 1.6.0 Overlay)

## Retained baseline

All S06C components, one active `AGT-001`, canonical `DATA-091`–`105`, `INT-063`–`078`, gateway-only `TOOL-001`–`006`, human authority, memory boundaries and protocol restrictions remain.

## Versioned change

- `GRAPH-001` advances from `1.1.0` to `1.2.0` through `ADR-056` and `ADR-057`.
- The graph remains sequential by default and adds one bounded parallel subgraph for independent immutable read-only/pure-compute branches.
- `AGT-001-spec 1.1.0` is unchanged.
- `CMP-003`, `008`, `009`, `010` and `011` gain the responsibilities described in the Stage 7A chapter.

## Invariants

- exactly one active `AGT-001`;
- no concurrent protected-state writes;
- no worker-owned route, approval, finalization, authority or system termination;
- `CMP-003` performs one state transition after deterministic fan-in;
- `CMP-007` validates authority;
- `CMP-005` remains the tool gateway;
- sequential fallback remains available.

## Cumulative architecture

```mermaid
flowchart LR
    classDef existing fill:#eef3f8,stroke:#506070,stroke-width:1px
    classDef changed fill:#fff4cc,stroke:#9a6b00,stroke-width:2px
    classDef new fill:#e9f7ef,stroke:#247a45,stroke-width:2px
    classDef boundary fill:#f7f7f7,stroke:#555,stroke-dasharray:5 3

    U[Maya Chen<br/>Regulatory Compliance Analyst]:::existing

    subgraph TB1[Experience and Intake Trust Boundary]
      C1[CMP-001<br/>Analyst Experience Portal]:::existing
      C2[CMP-002<br/>Regulatory Intake Boundary]:::existing
    end

    subgraph TB2[Application Orchestration Trust Boundary]
      C3[CMP-003<br/>Case and Workflow Orchestration Boundary]:::changed
      G[GRAPH-001/1.2.0<br/>Sequential graph + bounded parallel subgraph]:::new
      A[Admission Controller<br/>global/per-case/queue limits]:::new
      F[Fan-out/Fan-in Controller<br/>ordered aggregation]:::new
      X[Cancellation + Deadline Coordinator]:::new
      D109[DATA-109<br/>Idempotency records]:::new
      D112[DATA-112<br/>Resumption checkpoints]:::new
    end

    subgraph TB3[Knowledge and Integration Trust Boundary]
      C4[CMP-004<br/>Knowledge and Evidence Access Boundary]:::existing
      C5[CMP-005<br/>Enterprise Integration Boundary<br/>TOOL-001..006 gateway only]:::existing
    end

    subgraph TB4[Human and Authority Trust Boundary]
      C6[CMP-006<br/>Human Review and Approval Boundary]:::existing
      C7[CMP-007<br/>Identity, Authorization and Policy Boundary]:::existing
    end

    subgraph TB5[Assurance and Runtime Trust Boundary]
      C8[CMP-008<br/>Evaluation and Assurance Boundary]:::changed
      C9[CMP-009<br/>Observability and Audit Boundary]:::changed
      C10[CMP-010<br/>Runtime and Deployment Boundary]:::changed
      Q[Bounded Async Work Queue<br/>DATA-107 work items]:::new
      W[Worker Pool<br/>read-only / pure-compute only]:::new
      R[Broker-neutral ExecutionTransport contract<br/>loopback reference only]:::new
    end

    C11[CMP-011<br/>Source-of-Truth Governance Pack<br/>version 1.6.0]:::changed
    AGT[AGT-001<br/>Regulatory Impact Assessment Agent<br/>only active agent; spec 1.1.0]:::existing
    CAND[CAND-EVIDENCE-VERIFIER-001<br/>candidate sandbox only; not active]:::existing

    U --> C1
    C1 --> C2
    C2 --> C3
    C3 --> AGT
    C3 --> G
    G --> A
    A -->|INT-079 admission| Q
    Q -->|INT-080 submission| W
    W -->|read-only evidence| C4
    W -->|approved gateway calls only| C5
    C7 -->|policy decision / grant validation| C3
    C7 -->|no authority granted by queue| W
    W -->|INT-081 branch result| F
    F -->|INT-082 deterministic aggregate| G
    X -. cancellation/deadline .-> W
    C3 --> D109
    C3 --> D112
    C3 --> C6
    C6 --> C3
    W --> C9
    F --> C9
    C8 -->|INT-086 evaluations| C3
    C10 --- Q
    C10 --- W
    R -. future transport substitution .-> Q
    C11 --- C3
    C11 --- C8
    CAND -. not scheduled or activated .-> C3

```
