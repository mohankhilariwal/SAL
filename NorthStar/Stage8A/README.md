# NorthStar Stage 8A — Evaluation Architecture and Datasets

This repository is a compatible `1.9.0` overlay reconstructed from the supplied
Stage 7C handoff. It implements a local, standard-library-only evaluation
registry, immutable JSONL datasets, deterministic graders, split-isolation and
contamination checks, an isolated evaluation harness, human-review sampling,
and evidence export.

It does **not** implement Stage 7D model selection/routing, LLM-as-a-Judge,
online evaluation, production datasets, or production deployment gates.

## Run

```bash
python -m pip install -e '.[test]'
python scripts/validate_stage8a.py
python scripts/run_stage8a_demo.py
python scripts/run_stage8a_evaluation.py
pytest
python scripts/consistency_audit_stage8a.py
```

Python baseline: `>=3.11,<3.15`; verified on Python `3.13.5` with pytest `9.0.2`.
