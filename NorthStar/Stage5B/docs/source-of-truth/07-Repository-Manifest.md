# 07 — Repository Manifest

**Repository:** `northstar-agentic-compliance`  
**Version:** `1.2.0`

## 1. Important tree

```text
northstar-agentic-compliance/
├── config/
│   ├── agents/AGT-001.spec.json
│   ├── evaluation/stage5b.json
│   ├── harness/manifest.json
│   └── memory/policy.json
├── docs/
│   ├── adr/ADR-040...ADR-043*.md
│   ├── architecture/diagrams/stage-5b-*.mmd
│   ├── baseline/Stage-5A-Handoff-Pack-supplied.md
│   ├── references/Stage-5B-Technical-Sources.md
│   ├── source-of-truth/00...09*.md
│   └── stages/Stage-5B-Context-Lifecycle-Compaction-and-Memory-Boundaries.md
├── schemas/DATA-079...DATA-086*.schema.json
├── scripts/
│   ├── run_stage5b_demo.py
│   ├── run_stage5b_evaluation.py
│   ├── benchmark_stage5b.py
│   ├── validate_stage5b.py
│   └── consistency_audit_stage5b.py
├── src/northstar_compliance/memory/
│   ├── canonical.py
│   ├── models.py
│   ├── policy.py
│   ├── regeneration.py
│   ├── compaction.py
│   ├── store.py
│   ├── service.py
│   ├── lifecycle.py
│   └── __init__.py
├── tests/
│   ├── unit/test_regeneration_and_compaction.py
│   ├── integration/test_memory_lifecycle.py
│   ├── security/test_memory_security.py
│   └── evaluation/test_stage5b_evaluations.py
├── README.md
└── pyproject.toml
```

## 2. Entry points

```bash
python scripts/run_stage5b_demo.py
python scripts/run_stage5b_evaluation.py
python scripts/benchmark_stage5b.py
pytest -q
python scripts/validate_stage5b.py
python scripts/consistency_audit_stage5b.py
```

## 3. Compatibility

- Python `>=3.11,<3.15`; tested on `3.13.5`.
- Standard-library runtime; pytest `9.0.2` for tests.
- `GRAPH-001` and `DATA-009` remain `1.1.0`.
- `AGT-001-spec` is `1.1.0`; harness manifest is `1.2.0`.
- No requirement for network, paid model or external database.
- The repository is a compatible reconstruction overlay because the byte-exact S05A repository and ten detailed registers were not mounted.

## 4. Files added

Memory config, eight schemas, nine memory package files, five scripts, four test files, four ADRs, six Mermaid diagrams, source references, stage chapter and ten updated source-of-truth artefacts.

## 5. Files modified

`README.md`, `pyproject.toml`, `AGT-001.spec.json`, harness manifest and all ten cumulative artefacts.

## 6. Files retired

None. S05A artefacts are retained conceptually; the supplied handoff is copied into `docs/baseline/`.

## 7. Production migration notes

Replace `LocalCaseMemoryStore` through the service boundary; preserve data contracts, idempotency and fail-closed semantics. Add authenticated IAM/PDP evidence, encryption/KMS, distributed storage, retention/deletion orchestration, legal holds, audit/WORM evidence, tenant keys, observability redaction and disaster recovery before production.
