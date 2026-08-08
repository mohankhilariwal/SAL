# 03 — Architecture Baseline

## Version and maturity

- Architecture version: `0.4.0`.
- Maturity: bounded local RAG **retrieval/context layer**, not a generated-answer service and not an agent.
- `CMP-004` advances from preparation-only to preparation plus authorized retrieval, ranking, citation and context assembly.
- `CMP-008` advances with retrieval evaluation and permission-boundary regression.
- `CMP-007` remains planned; principal attributes are local test claims.

## Architecture before S02B

```mermaid
flowchart LR
    classDef implemented fill:#e8f5e9,stroke:#2e7d32;
    classDef partial fill:#fff8e1,stroke:#f57f17;
    classDef planned fill:#f3f4f6,stroke:#6b7280,stroke-dasharray:5 5;
    MAYA["Maya Chen"] --> C1["CMP-001 Analyst Experience Portal"]:::partial
    C1 --> C3["CMP-003 One-shot application flow"]:::partial
    C3 -. cannot query .-> C4["CMP-004 Knowledge and Evidence Access Boundary"]:::partial
    C4 --> PREP["Prepared corpus\nDATA-019 to DATA-025"]:::implemented
    C7["CMP-007 Identity, Authorization and Policy Boundary"]:::planned -. access strings only .-> PREP
    PREP --> C8["CMP-008 preparation validation"]:::partial
```

## New requirement

Maya needs the best authorized evidence without opening every chunk. Exact terms, paraphrases, overlapping passages and restricted sources make a single search method or post-filtering unsafe.

## Selected architecture

```mermaid
flowchart TB
    classDef implemented fill:#e8f5e9,stroke:#2e7d32,stroke-width:1.5px;
    classDef partial fill:#fff8e1,stroke:#f57f17,stroke-width:1.5px;
    classDef planned fill:#f3f4f6,stroke:#6b7280,stroke-dasharray:5 5;
    classDef new fill:#fce4ec,stroke:#ad1457,stroke-width:2px;
    classDef external fill:#ede7f6,stroke:#5e35b1;

    MAYA["Maya Chen\nRegulatory Compliance Analyst"]:::external --> C1["CMP-001 Analyst Experience Portal\nlocal CLI / evidence view"]:::partial
    PUB["Regulatory publication"]:::external --> C2["CMP-002 Regulatory Intake Boundary\nStage 1 bounded input"]:::implemented
    C1 --> C2 --> C3["CMP-003 Case and Workflow Orchestration Boundary\none-shot application flow"]:::partial
    C3 --> S1["Stage 1 provider-neutral summary contract"]:::partial

    SRCS["Approved policy, control, process, taxonomy\nand prior-assessment exports"]:::external --> C4["CMP-004 Knowledge and Evidence Access Boundary"]:::new
    subgraph K["CMP-004 implemented through S02B"]
        PREP["S02A parser, provenance, chunker, immutable corpus"]:::implemented
        AUTH["Deterministic query authorization\nbefore candidate scoring"]:::new
        LEX["BM25 lexical candidates"]:::new
        SEM["TF-IDF + SVD latent semantic candidates"]:::new
        FUS["Weighted reciprocal-rank fusion"]:::new
        RER["Metadata-aware reranking\nand overlap suppression"]:::new
        CITE["Exact line citation builder\nand context assembly"]:::new
        PREP --> AUTH
        AUTH --> LEX
        AUTH --> SEM
        LEX --> FUS
        SEM --> FUS
        FUS --> RER --> CITE
    end
    SRCS --> PREP
    C3 --> AUTH
    CITE --> C3

    C7["CMP-007 Identity, Authorization and Policy Boundary\nenterprise identity/PDP planned"]:::planned -. locally asserted principal context .-> AUTH
    C8["CMP-008 Evaluation and Assurance Boundary\nretrieval regression and permission tests"]:::new --> K
    C9["CMP-009 Observability and Audit Boundary\nlocal manifests/reports; not audit ledger"]:::partial <-->|"local evidence"| K
    C10["CMP-010 Runtime and Deployment Boundary\nlocal Python runtime"]:::partial --> K
    C11["CMP-011 Source-of-Truth Governance Pack\nversion 0.4.0"]:::implemented --> K

    C5["CMP-005 Enterprise Integration Boundary"]:::planned
    C6["CMP-006 Human Review and Approval Boundary"]:::planned
    C4 -. no live connectors .-> C5
    C3 -. no approval workflow .-> C6
```

## Retrieval flow

```mermaid
flowchart LR
    Q["DATA-027 RetrievalQuery"] --> PEP["Authorization filter\nprincipal + purpose + clearance + groups + residency + date"]
    P["DATA-026 RetrievalPrincipalContext"] --> PEP
    CORPUS["INT-010 Prepared Corpus Export"] --> PEP
    PEP --> AUTHSET["Authorized chunk subset"]
    AUTHSET --> BM25["BM25 lexical ranking"]
    AUTHSET --> LSA["TF-IDF + truncated-SVD semantic ranking"]
    BM25 --> RRF["Weighted reciprocal-rank fusion"]
    LSA --> RRF
    RRF --> RERANK["Deterministic metadata-aware reranker"]
    RERANK --> DEDUP["Overlapping-span suppression"]
    DEDUP --> CIT["Exact citation construction + independent validation"]
    CIT --> CTX["DATA-032 RetrievalContext"]
```

## Trust boundary

```mermaid
flowchart TB
    classDef trusted fill:#e8f5e9,stroke:#2e7d32;
    classDef untrusted fill:#ffebee,stroke:#c62828;
    classDef planned fill:#f3f4f6,stroke:#6b7280,stroke-dasharray:5 5;

    USER["Locally asserted principal attributes\nnot enterprise-authenticated"]:::untrusted --> PEP["Deterministic retrieval PEP"]:::trusted
    DOCS["Prepared document text\nuntrusted evidence data"]:::untrusted --> PEP
    META["Approved manifest metadata"]:::trusted --> PEP
    PDP["CMP-007 enterprise identity/PDP"]:::planned -. future signed decision .-> PEP
    PEP --> AUTH["Authorized candidate IDs"]:::trusted
    AUTH --> SCORE["Lexical and semantic scorers"]:::trusted
    SCORE --> CITE["Citation and context assembler"]:::trusted
    CITE --> MODEL["Future grounded generation boundary"]:::planned
    DOCS -. never becomes instruction .-> CITE
```

## Architecture invariants

1. `INT-010` is the only S02B input for prepared chunks; raw documents are not independently rechunked.
2. Authorization and metadata filtering precede lexical/semantic scorer construction.
3. Index identity binds corpus hash, source versions and retrieval configuration.
4. Fusion and reranking never widen the authorized candidate set.
5. Citations are application-built from immutable coordinates, not model-authored.
6. Retrieval context remains untrusted evidence and cannot alter application authority or disposition.
7. `CMP-008` evaluates retrieval independently from any future generator.
8. No agent, model-selectable tool, graph, memory, case state, approval or production audit capability exists.

## Deployment boundary

All components run in one local Python process over synthetic files. Logical boundaries are not claimed as microservices. Production decomposition requires an ADR based on identity, scaling, resilience, tenancy, ownership and data-residency needs.
