#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from northstar_compliance.workload.io import load_profile, load_service_model, write_json
from northstar_compliance.workload.models import BenchmarkScenario
from northstar_compliance.workload.simulation import derive_capacity_envelope


def main() -> int:
    parser = argparse.ArgumentParser(description="Derive a simulated, advisory Stage 7B capacity envelope")
    parser.add_argument("--profile", default="config/workloads/WP-001.json")
    parser.add_argument("--service-model", default="config/workloads/service-model-local.json")
    parser.add_argument("--requests", type=int, default=500)
    parser.add_argument("--rates", default="0.1,0.2,0.4,0.6,0.8,1.0,1.2")
    parser.add_argument("--output", default="reports/stage7b-capacity-envelope.json")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    if profile.arrival.request_rate_per_s is None:
        raise SystemExit("capacity rate sweep requires an open-loop profile")
    service = load_service_model(args.service_model)
    scenario = BenchmarkScenario("SC-S07B-CAPACITY", profile, service, args.requests, seed=703, warmup_requests=10)
    rates = [float(item) for item in args.rates.split(",") if item.strip()]
    envelope = derive_capacity_envelope(scenario, rates)
    write_json(args.output, envelope)
    print(json.dumps({**envelope.__dict__} if hasattr(envelope, "__dict__") else {
        field: getattr(envelope, field) for field in envelope.__dataclass_fields__
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
