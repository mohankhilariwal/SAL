# 07 — Repository Manifest

**Repository:** `northstar-agentic-compliance`  
**Version:** `0.3.0`

## 1. Important entry points

- Stage chapter: `docs/stages/Stage-2A-Ingestion-Chunking-and-Knowledge-Preparation.md`
- Preparation service: `src/northstar_compliance/knowledge/service.py`
- Schemas: `src/northstar_compliance/knowledge/schemas.py`
- Parser: `src/northstar_compliance/knowledge/parser.py`
- Chunker: `src/northstar_compliance/knowledge/chunker.py`
- Store: `src/northstar_compliance/knowledge/store.py`
- Validator: `src/northstar_compliance/knowledge/validation.py`
- Demo: `scripts/run_stage2a_demo.py`
- Validation CLI: `scripts/validate_stage2a.py`
- Input manifest: `datasets/stage2a/input/manifest.json`
- Handoff: `docs/source-of-truth/09-Stage-Handoff-Pack.md`
- Consistency audit: `scripts/consistency_audit_stage2a.py`

## 2. Repository tree

```text
northstar-agentic-compliance/
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── datasets/stage2a/input/
│   ├── manifest.json
│   └── documents/
│       ├── POL-001-lending-policy.md
│       ├── CTL-001-customer-data-control.md
│       ├── PROC-001-payments-screening.md
│       ├── TAX-001-regulatory-taxonomy.md
│       └── ASMT-001-prior-impact.md
├── docs/
│   ├── adr/ADR-011...ADR-013
│   ├── architecture/diagrams/
│   │   ├── stage-2a-architecture-before.mmd
│   │   ├── cumulative-logical-architecture.mmd
│   │   ├── stage-2a-ingestion-sequence.mmd
│   │   └── stage-2a-trust-boundary.mmd
│   ├── baseline/
│   │   ├── README.md
│   │   └── Stage-1-Handoff-Pack-supplied.md
│   ├── references/Stage-2A-Technical-Sources.md
│   ├── source-of-truth/00...09
│   └── stages/Stage-2A-Ingestion-Chunking-and-Knowledge-Preparation.md
├── examples/stage2a-output/
│   ├── corpus-manifest.json
│   ├── runs/ING-*.json
│   └── corpus/<source>/<version>/...
├── reports/
│   ├── demo-output.json
│   ├── pytest-output.txt
│   ├── validation-output.json
│   ├── consistency-audit.json
│   ├── python-version.txt
│   └── pytest-version.txt
├── scripts/
│   ├── run_stage2a_demo.py
│   ├── validate_stage2a.py
│   └── consistency_audit_stage2a.py
├── src/northstar_compliance/
│   ├── __init__.py
│   └── knowledge/
│       ├── __init__.py
│       ├── schemas.py
│       ├── parser.py
│       ├── chunker.py
│       ├── store.py
│       ├── service.py
│       └── validation.py
└── tests/
    ├── unit/test_parser.py
    ├── unit/test_chunker.py
    ├── integration/test_ingestion.py
    ├── security/test_access_metadata.py
    └── evaluation/test_chunk_quality.py
```

## 3. Retained S01 paths

The supplied S01 handoff identifies these paths as existing in the prior repository and they remain compatibility constraints:

- `src/northstar_compliance/cli.py`
- `src/northstar_compliance/model_gateway.py`
- `src/northstar_compliance/validation.py`
- `scripts/run_stage1_demo.sh`
- `scripts/validate_stage1.py`
- `docs/stages/Stage-1-Manual-Process-and-Basic-LLM-Assistant.md`

They were not attached in this execution and are not silently recreated. The S02A bundle is an overlay/new-stage package designed to be merged into that repository.

## 4. Run and test

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/run_stage2a_demo.py
pytest
python scripts/validate_stage2a.py
python scripts/consistency_audit_stage2a.py
python -m compileall -q src scripts tests
```

## 5. Verified versions and boundaries

- Python executed: `3.13.5`.
- pytest executed: `9.0.2`.
- Runtime dependencies: none outside standard library.
- 12 tests passed.
- Demo: 5 sources, 21 chunks, warning flag on adversarial prior-assessment fixture.
- Mermaid CLI not executed.
- Python 3.12 not directly executed.
