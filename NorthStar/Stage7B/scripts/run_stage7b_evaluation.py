#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import replace

from northstar_compliance.workload.evaluation import evaluate_profile
from northstar_compliance.workload.io import load_profile, load_service_model, write_json
from northstar_compliance.workload.models import BenchmarkScenario
from northstar_compliance.workload.simulation import CapacitySimulator


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Stage 7B workload evaluation")
    parser.add_argument("--profile", default="config/workloads/WP-001.json")
    parser.add_argument("--service-model", default="config/workloads/service-model-local.json")
    parser.add_argument("--output", default="reports/stage7b-evaluation.json")
    parser.add_argument("--request-rate", type=float, default=None, help="Override an open-loop profile rate for envelope validation")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    if args.request_rate is not None:
        if profile.arrival.request_rate_per_s is None:
            raise SystemExit("--request-rate requires an open-loop profile")
        profile = replace(profile, arrival=replace(profile.arrival, request_rate_per_s=args.request_rate))
    service = load_service_model(args.service_model)
    scenario = BenchmarkScenario("SC-S07B-EVAL", profile, service, 120, seed=704, warmup_requests=5)
    results = evaluate_profile(profile, CapacitySimulator(scenario).run())
    report = {
        "profile_id": profile.profile_id,
        "request_rate_per_s": profile.arrival.request_rate_per_s,
        "results": [
            {"evaluation_id": r.evaluation_id, "passed": r.passed, "detail": r.detail} for r in results
        ],
        "passed": all(r.passed for r in results),
    }
    write_json(args.output, report)
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
