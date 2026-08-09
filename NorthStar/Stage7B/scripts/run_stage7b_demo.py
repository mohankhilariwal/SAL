#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from northstar_compliance.workload.io import load_profile, load_service_model, write_json
from northstar_compliance.workload.models import BenchmarkScenario
from northstar_compliance.workload.simulation import CapacitySimulator


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Stage 7B local planning demo")
    parser.add_argument("--profile", default="config/workloads/WP-001.json")
    parser.add_argument("--service-model", default="config/workloads/service-model-local.json")
    parser.add_argument("--requests", type=int, default=120)
    parser.add_argument("--seed", type=int, default=701)
    parser.add_argument("--output", default="reports/stage7b-demo.json")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    service = load_service_model(args.service_model)
    scenario = BenchmarkScenario(
        scenario_id="SC-S07B-DEMO",
        profile=profile,
        service_model=service,
        request_count=args.requests,
        seed=args.seed,
        warmup_requests=min(5, max(0, args.requests - 1)),
    )
    summary = CapacitySimulator(scenario).summarize()
    report = {
        "evidence_kind": "simulated",
        "warning": "Planning proxy only; not production endpoint evidence.",
        "profile_id": profile.profile_id,
        "profile_version": profile.version,
        "profile_digest": profile.digest,
        "tokenizer_id": profile.tokenizer_id,
        "service_model": service.model_id,
        "metrics": summary,
    }
    write_json(args.output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
