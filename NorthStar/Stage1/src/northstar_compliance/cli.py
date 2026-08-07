from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .artifact_store import LocalArtifactStore
from .intake import ingest_publication
from .mock_model import DeterministicMockSummaryModel
from .openai_http import OpenAIResponsesSummaryModel
from .service import run_summary


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="NorthStar Stage 1 bounded regulatory summarizer")
    p.add_argument("--provider", choices=("mock", "openai"), default="mock")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--source-uri", required=True)
    p.add_argument("--jurisdiction", required=True)
    p.add_argument("--output-dir", type=Path, default=Path(os.getenv("NORTHSTAR_OUTPUT_DIR", "examples/stage1-output")))
    p.add_argument("--max-input-bytes", type=int, default=int(os.getenv("NORTHSTAR_MAX_INPUT_BYTES", "250000")))
    return p


def main() -> int:
    args = parser().parse_args()
    publication = ingest_publication(
        args.input,
        title=args.title,
        source_uri=args.source_uri,
        jurisdiction=args.jurisdiction,
        max_bytes=args.max_input_bytes,
    )
    model = DeterministicMockSummaryModel() if args.provider == "mock" else OpenAIResponsesSummaryModel()
    result = run_summary(publication, model=model, store=LocalArtifactStore(args.output_dir))
    print(json.dumps({
        "artifact_path": str(result.artifact_path),
        "publication_id": result.summary.publication_id,
        "disposition": result.summary.disposition,
        "human_review_required": result.summary.human_review_required,
        "source_fact_count": len(result.summary.source_facts),
        "deadline_candidate_count": len(result.summary.deadline_candidates),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
