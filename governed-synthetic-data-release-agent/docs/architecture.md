# Architecture

## System context

```mermaid
flowchart LR
    Analyst[Fraud analyst] --> System[Governed release system]
    Owner[Data Owner] --> System
    Privacy[Privacy Officer] --> System
    Operator[Local operator] --> System
    System --> Internal[Internal sandbox]
    System --> Partner[Named external partner simulation]
```

## Containers and components

```mermaid
flowchart TB
    subgraph Presentation
      UI[Streamlit]
      API[FastAPI]
    end
    subgraph Application
      WF[WorkflowService]
      Evidence[EvidenceBuilder]
    end
    subgraph Domain
      Models[Pydantic v2 entities]
      PolicyContract[PolicyDecisionPoint port]
      GatewayContracts[Generator / model / export / audit ports]
    end
    subgraph Adapters
      DB[(SQLite + SQLAlchemy)]
      Files[Controlled local files]
      SDV[GaussianCopulaSynthesizer]
      Eval[Scikit-learn + deterministic metrics]
      PDP[Python PDP]
      OPA[Optional OPA adapter]
      Model[Stub / Ollama]
      Audit[JSONL + SQLite hash chain]
    end
    UI --> API --> WF
    WF --> Models
    WF --> DB
    WF --> Files
    WF --> SDV
    WF --> Eval
    WF --> PDP
    WF -. optional .-> OPA
    WF --> Model
    WF --> Audit
    WF --> Evidence
```

## Workflow state machine

```mermaid
stateDiagram-v2
    [*] --> RECEIVED
    RECEIVED --> IDENTITY_VALIDATED
    IDENTITY_VALIDATED --> AUTHORITY_VALIDATED
    AUTHORITY_VALIDATED --> SUSPENDED: injection / kill / budget
    AUTHORITY_VALIDATED --> DATA_PROFILED
    DATA_PROFILED --> CLASSIFIED
    CLASSIFIED --> PLAN_AUTHORIZED
    PLAN_AUTHORIZED --> GENERATED
    GENERATED --> EVALUATED
    EVALUATED --> RELEASED: ALLOW + gateway
    EVALUATED --> AWAITING_APPROVAL: REQUIRE_APPROVAL
    AWAITING_APPROVAL --> AWAITING_APPROVAL: one approval
    AWAITING_APPROVAL --> APPROVED: both approvals
    APPROVED --> RELEASED: gateway
    AWAITING_APPROVAL --> QUARANTINED: rejection
    EVALUATED --> QUARANTINED: privacy / utility / evidence
    EVALUATED --> SUSPENDED: kill / budget
```

The complete state is stored as typed JSON in SQLite at each checkpoint. A process restart can reload a workflow and call `resume`; approval records are separately persisted and single-use.

## Trust boundaries

```mermaid
flowchart LR
    subgraph Untrusted
      Req[User request text]
      LLM[LLM output]
      Retrieved[Retrieved/user content]
    end
    subgraph ControlledApplication
      Parse[Validation + injection detection]
      Metrics[Deterministic evaluators]
      PDP[Policy engine]
      Approval[Approval checkpoint]
    end
    subgraph RestrictedData
      Source[Restricted fictional source]
      Candidate[Candidate area]
      Quarantine[Quarantine]
    end
    subgraph ReleaseBoundary
      Gateway[Export gateway]
      Released[Released area + receipt]
    end
    Req --> Parse
    LLM --> Parse
    Retrieved --> Parse
    Parse --> Source
    Source --> Candidate
    Candidate --> Metrics --> PDP
    PDP --> Approval --> Gateway
    PDP --> Gateway
    PDP --> Quarantine
    Gateway --> Released
```

## Decision authority

```mermaid
flowchart TD
    LLM[LLM: interpret and explain] --> Facts[Proposed interpretation]
    Code[Code: calculate metrics] --> Facts
    Facts --> PDP[Policy engine: authorize]
    PDP -->|residual external risk| Humans[Data Owner + Privacy Officer]
    PDP -->|ALLOW| Export[Export gateway]
    Humans -->|both approve| Export
    Humans -->|reject| Q[Quarantine]
    Export --> Receipt[Receipt + expiry + hash]
```

## Approval sequence

```mermaid
sequenceDiagram
    participant W as Workflow
    participant P as Policy engine
    participant D as Data Owner
    participant O as Privacy Officer
    participant E as Export gateway
    W->>P: Normalized policy input
    P-->>W: REQUIRE_APPROVAL
    W-->>D: Evidence-bound approval card
    W-->>O: Evidence-bound approval card
    D->>W: Single-use decision
    O->>W: Single-use decision
    W->>P: Re-evaluate with both roles
    P-->>W: ALLOW
    W->>E: Candidate + evidence + authorization
    E-->>W: Export receipt
```

## Export sequence

```mermaid
sequenceDiagram
    participant W as Workflow
    participant G as Export gateway
    participant M as Evidence manifest
    participant C as Candidate area
    participant R as Released area
    W->>G: ExportAuthorization
    G->>M: Verify SHA-256 manifest
    G->>C: Verify candidate ID, state, columns, hash
    G->>G: Check approvals, destination, kill switch, idempotency
    G->>R: Atomic copy
    G->>R: Write receipt and expiry
    G-->>W: ExportReceipt
```

## Evidence lineage

```mermaid
flowchart LR
    Request --> Identity --> Authority --> Profile --> Classification --> Plan --> Candidate --> Utility --> Privacy --> Recipient --> Policy --> Approvals --> Export
    Request --> Bundle[Evidence bundle]
    Identity --> Bundle
    Authority --> Bundle
    Profile --> Bundle
    Classification --> Bundle
    Plan --> Bundle
    Candidate --> Bundle
    Utility --> Bundle
    Privacy --> Bundle
    Recipient --> Bundle
    Policy --> Bundle
    Approvals --> Bundle
    Export --> Bundle
    Bundle --> Manifest[SHA-256 manifest]
    Bundle --> Zip[ZIP]
```

## Scenario 4 attack and denial

```mermaid
sequenceDiagram
    actor A as Malicious requester content
    participant W as Workload agent
    participant C as Control Plane
    participant T as Tool gateway intent
    participant Audit as Audit ledger
    A->>W: copy IDs; upload raw file; skip evaluation
    W->>C: interpreted requested actions
    C->>C: deterministic injection rules
    C--xT: deny raw read / evaluator bypass / arbitrary URL
    C->>Audit: record full redacted security trace
    C-->>W: DENY + SUSPEND
```

## Local-to-production migration

```mermaid
flowchart LR
    SQLite --> PostgreSQL[Managed PostgreSQL]
    LocalFiles --> ObjectStorage[Governed object storage]
    LocalProcess --> ManagedRuntime[Containers / managed agent runtime]
    StubOllama --> ManagedModels[Managed model endpoint]
    PythonPDP --> HostedPDP[OPA / managed policy service]
    SeedIdentity --> EnterpriseIdP[Enterprise identity]
    LocalApproval --> DurableWorkflow[Durable callback workflow]
    JSONL --> CentralTelemetry[OTel + centralized logs]
    LocalExport --> GovernedDelivery[Object-store delivery + immutability]
```
