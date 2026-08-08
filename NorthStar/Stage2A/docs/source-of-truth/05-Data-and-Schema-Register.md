# 05 — Data and Schema Register

**Version:** `0.3.0`  
**Schema version for S02A objects:** `1.0.0`

## 1. Preserved data objects

`DATA-001` through `DATA-014` remain accepted. The supplied S01 handoff explicitly identifies:

- `DATA-001` regulatory publication as executable in S01;
- `DATA-002 RegulatoryCase` as not instantiated;
- line-based specialization of `DATA-004` as executable in S01;
- `DATA-007 ReviewDecision`, `DATA-009 AgentRunState` and `DATA-010 AuthorizationGrant` as not instantiated;
- `DATA-015 PreliminaryRegulatorySummary`;
- `DATA-016 SummaryClaim`;
- `DATA-017 ModelInvocationRecord`;
- `DATA-018 PublicationMetadata`.

S02A does not alter those definitions or schemas.

## 2. New S02A objects

### `DATA-019 KnowledgeSourceDescriptor`

Fields: schema version, source ID, title, source type, owner, relative path, business version, effective dates, jurisdictions, business domains, `DATA-020`, retention class, authority flag.

### `DATA-020 AccessScope`

Fields: classification (`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`), non-empty allowed groups, residency and purpose. Public content must use `['*']`; non-public content may not.

### `DATA-021 KnowledgeDocumentVersion`

Fields: source ID, `KSV-*`, business version, raw/normalized/metadata hashes, byte/line count, parser/chunker versions, ingestion time, status, risk flags and optional superseded version.

### `DATA-022 KnowledgeChunk`

Fields: `CHK-*`, source/version IDs, ordinal, heading path, line coordinates, character count, content hash, exact text, inherited access, jurisdictions/domains/effective dates and risk flags.

### `DATA-023 KnowledgeCorpusManifest`

Fields: schema/corpus/parser/chunker versions, chunking policy, active versions, all historical versions, counts, input manifest hash and update time.

### `DATA-024 IngestionRunRecord`

Fields: `ING-*`, start/completion time, status, input manifest hash, item actions/counts/warnings and errors.

### `DATA-025 KnowledgePreparationReport`

Logical evaluation result containing source/chunk/warning counts and integrity findings. The current CLI returns a dictionary; a stricter schema may be introduced if promoted to a service API.

## 3. Identity and immutability

- `KSV-*` is SHA-256-derived from source, version label, normalized content hash, metadata hash, parser and chunker versions.
- `CHK-*` is SHA-256-derived from source-version ID, exact coordinates and text.
- Version directories are immutable. Active pointers change only in the corpus manifest.
- Raw and normalized hashes are both retained.

## 4. Persistence layout

```text
examples/stage2a-output/
├── corpus-manifest.json
├── runs/ING-*.json
└── corpus/<SOURCE-ID>/<KSV-ID>/
    ├── raw/<original-file>
    ├── normalized.txt
    ├── descriptor.json
    ├── document-version.json
    └── chunks.jsonl
```

This is a local tutorial artifact layout, not a case store, records repository or audit ledger.

## 5. Interfaces

| ID | Contract | Authorization/control | Status |
|---|---|---|---|
| `INT-001` | S01 publication intake | bounded local validation | retained |
| `INT-002` | S01 preliminary summary | fixed preliminary/human-review semantics | retained |
| `INT-007` | S01 local evaluation | local tests | retained |
| `INT-008` | S01 partial process/invocation evidence | provider types behind contract | retained |
| `INT-009` | Authorized Knowledge Ingestion Contract | approved manifest; bounded path; valid access metadata; enterprise auth pending | implemented locally |
| `INT-010` | Prepared Corpus Export Contract | immutable version packages and manifest; consumer must not bypass | implemented |
| `INT-011` | Knowledge Preparation Evaluation Contract | independent hash/coordinate/access/coverage validation | implemented locally |

## 6. Compatibility constraints

- S02B must consume `DATA-022` through `INT-010`; it may not create incompatible chunks from raw sources.
- Access scope must be applied before any future candidate text is exposed.
- Indexes must rebuild when parser/chunker/schema or relevant metadata changes.
- S01 `DATA-015` remains schema `1.0.0` and `stage1-summary-v1`.
