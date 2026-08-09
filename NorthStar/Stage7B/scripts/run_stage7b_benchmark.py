#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from northstar_compliance.workload.adapters import build_aiperf_plan, build_vllm_plan, export_sample_trace
from northstar_compliance.workload.io import load_profile
from northstar_compliance.workload.sampling import WorkloadSampler


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Stage 7B benchmark traces and external command plans")
    parser.add_argument("--profile", default="config/workloads/WP-005.json")
    parser.add_argument("--requests", type=int, default=200)
    parser.add_argument("--seed", type=int, default=702)
    parser.add_argument("--endpoint", default="http://localhost:8000")
    parser.add_argument("--model", default="replace-with-served-model")
    parser.add_argument("--output-dir", default="reports/benchmark-plan")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    sampled = WorkloadSampler(profile, args.seed).sample(args.requests)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    export_sample_trace(profile, sampled, output_dir / "sample-trace.json")

    plans = [
        build_aiperf_plan(profile, endpoint=args.endpoint, model=args.model, request_count=args.requests),
        build_vllm_plan(profile, endpoint=args.endpoint, model=args.model, request_count=args.requests),
    ]
    payload = {
        "profile_id": profile.profile_id,
        "profile_digest": profile.digest,
        "warning": "Commands are generated, not executed. Fixed-length CLI parameters are smoke-tests only.",
        "plans": [
            {"tool": plan.tool, "command": list(plan.command), "notes": list(plan.notes)} for plan in plans
        ],
    }
    (output_dir / "external-plans.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
