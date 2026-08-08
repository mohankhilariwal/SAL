# NorthStar Agentic Compliance — Stage 2A

This package implements only **Stage 2A — Ingestion, Chunking and Knowledge Preparation**.
It extends the Stage 1 non-agentic assistant with a deterministic, local knowledge-preparation pipeline.
It does **not** implement search, embeddings, reranking, model-context assembly, tools, agent loops, memory or workflow state.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/run_stage2a_demo.py
pytest
python scripts/validate_stage2a.py
```

The demo writes an immutable prepared corpus under `examples/stage2a-output/`.
