# NorthStar Agentic Compliance

This is the cumulative implementation repository for the **NorthStar Agentic AI Architecture Playbook**.

Current state: **Stage 0 - Playbook Foundation and Architecture Constitution**.

## What exists

- Ten authoritative source-of-truth artefacts in `docs/source-of-truth/`.
- The complete Stage 0 chapter in `docs/stages/`.
- A dependency-free structural validator.
- Standard-library unit tests.

## What does not exist yet

No LLM assistant, RAG, agent, tool integration, graph, memory, control plane or production deployment is implemented.

## Validate

```bash
python3 scripts/validate_source_of_truth.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Architecture version: `0.1.0`  
Repository version: `0.1.0`
