# 07 — Repository Manifest

## Repository version

- Name: `northstar-agentic-compliance`
- Version: `0.4.0`
- Python contract: `>=3.11,<3.15`
- Direct runtime dependency: `numpy==2.3.5`
- Test dependency: `pytest==9.0.2`
- Optional, unverified production-oriented adapter: `sentence-transformers>=5,<6`
- Verified environment: Python `3.13.5`, NumPy `2.3.5`, pytest `9.0.2`.

## Important entry points

- `src/northstar_compliance/knowledge/retrieval.py`
- `src/northstar_compliance/knowledge/authorization.py`
- `src/northstar_compliance/knowledge/lexical.py`
- `src/northstar_compliance/knowledge/semantic.py`
- `src/northstar_compliance/knowledge/fusion.py`
- `src/northstar_compliance/knowledge/reranker.py`
- `src/northstar_compliance/knowledge/citations.py`
- `src/northstar_compliance/knowledge/evaluation.py`
- `scripts/run_stage2b_demo.py`
- `scripts/validate_stage2b.py`
- `scripts/consistency_audit_stage2b.py`
- `docs/stages/Stage-2B-Retrieval-Reranking-Citations-and-RAG-Evaluation.md`
- `docs/source-of-truth/09-Stage-Handoff-Pack.md`

## Files added

- S02B retrieval/ranking/citation/evaluation modules under `src/northstar_compliance/knowledge/`.
- S02B evaluation cases under `datasets/stage2b/`.
- S02B demo, validation and consistency scripts.
- S02B unit, integration and evaluation tests.
- S02B architecture diagrams, four ADRs, technical references and stage chapter.
- Updated ten source-of-truth artefacts.

## Files modified/reconstructed

- Preparation modules are reconstructed in this overlay to consume the S02A contract and run the synthetic corpus locally.
- `README.md`, `CHANGELOG.md`, `pyproject.toml`, lock and environment examples advance to `0.4.0`.

## Files retired

None.

## Compatibility notes

1. The supplied S02A handoff is preserved at `docs/baseline/Stage-2A-Handoff-Pack-supplied.md`.
2. The nine other S02A registers and byte-exact S02A repository were not attached; this is a compatible overlay, not proof of a byte-for-byte patch.
3. S02B consumes prepared chunks through `INT-010` and preserves `KSV-*`, `CHK-*`, hash and line semantics.
4. Index/config changes require rebuild and re-evaluation.
5. The local LSA implementation is educational, not a production semantic model.
6. Local reports are not enterprise records or an audit ledger.

## Execution commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python scripts/run_stage2b_demo.py
python -m pytest -q
python scripts/validate_stage2b.py
python scripts/consistency_audit_stage2b.py
```

## Complete current file inventory

```text
.env.example
.gitignore
CHANGELOG.md
README.md
datasets/stage2a/input/documents/ASMT-001-prior-impact.md
datasets/stage2a/input/documents/CTL-001-customer-data-control.md
datasets/stage2a/input/documents/POL-001-lending-policy.md
datasets/stage2a/input/documents/PROC-001-payments-screening.md
datasets/stage2a/input/documents/TAX-001-regulatory-taxonomy.md
datasets/stage2a/input/manifest.json
datasets/stage2b/evaluation-cases.json
docs/adr/ADR-014-authorize-before-retrieval-scoring.md
docs/adr/ADR-015-hybrid-retrieval-and-rrf.md
docs/adr/ADR-016-deterministic-reranking-and-deduplication.md
docs/adr/ADR-017-exact-citations-and-retrieval-first-evaluation.md
docs/adr/README.md
docs/architecture/diagrams/cumulative-logical-architecture.mmd
docs/architecture/diagrams/stage-2b-architecture-after.mmd
docs/architecture/diagrams/stage-2b-architecture-before.mmd
docs/architecture/diagrams/stage-2b-evaluation-architecture.mmd
docs/architecture/diagrams/stage-2b-ranking-pipeline.mmd
docs/architecture/diagrams/stage-2b-retrieval-sequence.mmd
docs/architecture/diagrams/stage-2b-trust-boundary.mmd
docs/baseline/Stage-2A-Handoff-Pack-supplied.md
docs/references/Stage-2B-Technical-Sources.md
docs/source-of-truth/00-Project-Constitution.md
docs/source-of-truth/01-Business-and-User-Story-Baseline.md
docs/source-of-truth/02-Requirements-Register.md
docs/source-of-truth/03-Architecture-Baseline.md
docs/source-of-truth/04-Component-and-Agent-Catalogue.md
docs/source-of-truth/05-Data-and-Schema-Register.md
docs/source-of-truth/06-ADR-Register.md
docs/source-of-truth/07-Repository-Manifest.md
docs/source-of-truth/08-Risk-Assumption-and-Issue-Register.md
docs/source-of-truth/09-Stage-Handoff-Pack.md
docs/stages/Stage-2B-Retrieval-Reranking-Citations-and-RAG-Evaluation.md
examples/stage2b-output/index/retrieval-index-manifest.json
examples/stage2b-output/prepared-corpus/corpus/ASMT-001/KSV-D617CDA60FF9A2BA7206/chunks.jsonl
examples/stage2b-output/prepared-corpus/corpus/ASMT-001/KSV-D617CDA60FF9A2BA7206/descriptor.json
examples/stage2b-output/prepared-corpus/corpus/ASMT-001/KSV-D617CDA60FF9A2BA7206/document-version.json
examples/stage2b-output/prepared-corpus/corpus/ASMT-001/KSV-D617CDA60FF9A2BA7206/normalized.txt
examples/stage2b-output/prepared-corpus/corpus/ASMT-001/KSV-D617CDA60FF9A2BA7206/raw/ASMT-001-prior-impact.md
examples/stage2b-output/prepared-corpus/corpus/CTL-001/KSV-F3EC747F8737F30E2B86/chunks.jsonl
examples/stage2b-output/prepared-corpus/corpus/CTL-001/KSV-F3EC747F8737F30E2B86/descriptor.json
examples/stage2b-output/prepared-corpus/corpus/CTL-001/KSV-F3EC747F8737F30E2B86/document-version.json
examples/stage2b-output/prepared-corpus/corpus/CTL-001/KSV-F3EC747F8737F30E2B86/normalized.txt
examples/stage2b-output/prepared-corpus/corpus/CTL-001/KSV-F3EC747F8737F30E2B86/raw/CTL-001-customer-data-control.md
examples/stage2b-output/prepared-corpus/corpus/POL-001/KSV-0921CE196D63A7CE6773/chunks.jsonl
examples/stage2b-output/prepared-corpus/corpus/POL-001/KSV-0921CE196D63A7CE6773/descriptor.json
examples/stage2b-output/prepared-corpus/corpus/POL-001/KSV-0921CE196D63A7CE6773/document-version.json
examples/stage2b-output/prepared-corpus/corpus/POL-001/KSV-0921CE196D63A7CE6773/normalized.txt
examples/stage2b-output/prepared-corpus/corpus/POL-001/KSV-0921CE196D63A7CE6773/raw/POL-001-lending-policy.md
examples/stage2b-output/prepared-corpus/corpus/PROC-001/KSV-3CD13C57F3A62D76108E/chunks.jsonl
examples/stage2b-output/prepared-corpus/corpus/PROC-001/KSV-3CD13C57F3A62D76108E/descriptor.json
examples/stage2b-output/prepared-corpus/corpus/PROC-001/KSV-3CD13C57F3A62D76108E/document-version.json
examples/stage2b-output/prepared-corpus/corpus/PROC-001/KSV-3CD13C57F3A62D76108E/normalized.txt
examples/stage2b-output/prepared-corpus/corpus/PROC-001/KSV-3CD13C57F3A62D76108E/raw/PROC-001-payments-screening.md
examples/stage2b-output/prepared-corpus/corpus/TAX-001/KSV-8933A97D01785479DFB7/chunks.jsonl
examples/stage2b-output/prepared-corpus/corpus/TAX-001/KSV-8933A97D01785479DFB7/descriptor.json
examples/stage2b-output/prepared-corpus/corpus/TAX-001/KSV-8933A97D01785479DFB7/document-version.json
examples/stage2b-output/prepared-corpus/corpus/TAX-001/KSV-8933A97D01785479DFB7/normalized.txt
examples/stage2b-output/prepared-corpus/corpus/TAX-001/KSV-8933A97D01785479DFB7/raw/TAX-001-regulatory-taxonomy.md
examples/stage2b-output/prepared-corpus/corpus-manifest.json
examples/stage2b-output/prepared-corpus/runs/ING-20260731T210251003168Z.json
examples/stage2b-output/prepared-corpus/runs/ING-20260731T210251588862Z.json
pyproject.toml
reports/consistency-audit-console.txt
reports/consistency-audit.json
reports/demo-console.txt
reports/demo-output.json
reports/dependency-versions.txt
reports/editable-install-output.txt
reports/pytest-output.txt
reports/python-version.txt
reports/retrieval-evaluation.json
reports/validation-console.txt
reports/validation-output.json
requirements.lock
scripts/consistency_audit_stage2b.py
scripts/run_stage2b_demo.py
scripts/validate_stage2b.py
src/northstar_compliance/__init__.py
src/northstar_compliance/knowledge/__init__.py
src/northstar_compliance/knowledge/authorization.py
src/northstar_compliance/knowledge/chunker.py
src/northstar_compliance/knowledge/citations.py
src/northstar_compliance/knowledge/corpus.py
src/northstar_compliance/knowledge/evaluation.py
src/northstar_compliance/knowledge/fusion.py
src/northstar_compliance/knowledge/index.py
src/northstar_compliance/knowledge/lexical.py
src/northstar_compliance/knowledge/parser.py
src/northstar_compliance/knowledge/reranker.py
src/northstar_compliance/knowledge/retrieval.py
src/northstar_compliance/knowledge/schemas.py
src/northstar_compliance/knowledge/semantic.py
src/northstar_compliance/knowledge/sentence_transformers_adapter.py
src/northstar_compliance/knowledge/service.py
src/northstar_compliance/knowledge/store.py
src/northstar_compliance/knowledge/tokenization.py
src/northstar_compliance/knowledge/validation.py
tests/conftest.py
tests/evaluation/test_retrieval_evaluation.py
tests/integration/test_authorized_retrieval.py
tests/unit/test_retrieval_components.py
tests/unit/test_stage2a_compatibility.py
```
