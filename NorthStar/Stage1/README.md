# NorthStar Agentic Compliance

Cumulative implementation repository for the **NorthStar Agentic AI Architecture Playbook**.

Current accepted stage: **S01 — Manual Process and Basic LLM Assistant**  
Architecture/repository version: **0.2.0**

Stage 1 adds a bounded, single-turn regulatory-publication summarizer. It is an **assistant application**, not an agent. It has no retrieval, tools, durable workflow state, autonomous loop, memory, or multi-agent capability.

## Local run

```bash
python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m northstar_compliance.cli \
  --provider mock \
  --input datasets/stage1/sample-publication.txt \
  --title "Synthetic Supervisory Notice 2026-NS-17" \
  --source-uri "synthetic://northstar/2026-NS-17" \
  --jurisdiction CA \
  --output-dir examples/stage1-output
```

For an optional managed-model call, set `OPENAI_API_KEY` and `OPENAI_MODEL`, then use `--provider openai`. No managed-model call is required for the tests.

## Important boundary

Every generated summary is marked `preliminary_unapproved`; `human_review_required` is always `true`. The model cannot set approval, final legal interpretation, risk acceptance, or any enterprise action.
