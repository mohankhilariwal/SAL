# 07 - Repository Manifest

**Repository:** `northstar-agentic-compliance`  
**Version:** 0.2.0

```text
northstar-agentic-compliance/
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── requirements.lock
├── Stage-1-Handoff-Pack.md
├── Stage-1-Validation-Report.txt
├── .env.example
├── datasets/stage1/
│   ├── sample-publication.txt
│   └── adversarial-publication.txt
├── docs/
│   ├── source-of-truth/00-... through 09-...
│   ├── stages/Stage-1-Manual-Process-and-Basic-LLM-Assistant.md
│   ├── adr/ADR-008...ADR-010...
│   ├── architecture/diagrams/
│   │   ├── cumulative-logical-architecture.mmd
│   │   ├── stage-1-architecture-before.mmd
│   │   ├── stage-1-sequence.mmd
│   │   └── stage-1-trust-boundaries.mmd
│   └── references/Stage-1-Technical-Sources.md
├── src/northstar_compliance/
│   ├── __init__.py
│   ├── schemas.py
│   ├── intake.py
│   ├── prompts.py
│   ├── model_gateway.py
│   ├── mock_model.py
│   ├── openai_http.py
│   ├── validation.py
│   ├── artifact_store.py
│   ├── service.py
│   └── cli.py
├── tests/test_stage1.py
├── scripts/
│   ├── run_stage1_demo.sh
│   ├── validate_source_of_truth.py
│   └── validate_stage1.py
└── examples/stage1-output/PUB-.../
```

## Entry points

- CLI: `src/northstar_compliance/cli.py`
- Model boundary: `model_gateway.py`
- Deterministic offline adapter: `mock_model.py`
- Optional managed-provider adapter: `openai_http.py`
- Schema/evidence validation: `validation.py`
- Stage acceptance: `scripts/validate_stage1.py`
- Current chapter: `docs/stages/Stage-1-Manual-Process-and-Basic-LLM-Assistant.md`
- Validation report: `Stage-1-Validation-Report.txt`
- Exported handoff: `Stage-1-Handoff-Pack.md`

## Compatibility baseline

- Accepted Python: 3.12; supported/tested package metadata allows 3.12 and 3.13.
- Executed environment: Python 3.13.5.
- Runtime dependencies: standard library only.
- Managed provider: optional and not live-called in acceptance.
- Schema versions: `1.0.0`.
- Prompt version: `stage1-summary-v1`.
- No package or API from a later stage is introduced.
