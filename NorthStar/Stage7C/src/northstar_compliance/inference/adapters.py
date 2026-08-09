from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .models import InferenceBenchmarkScenario


def capability_plan(scenario: InferenceBenchmarkScenario) -> dict[str, Any]:
    """Return a version-neutral plan for translation by an external endpoint adapter."""
    return {
        "scenario_id": scenario.scenario_id,
        "scenario_digest": scenario.digest(),
        "profile_id": scenario.workload.profile_id,
        "deployment_id": scenario.deployment.deployment_id,
        "deployment_digest": scenario.deployment.digest(),
        "policy_id": scenario.policy.policy_id,
        "policy_digest": scenario.policy.digest(),
        "request_count": scenario.request_count,
        "seed": scenario.seed,
        "cache_state": scenario.cache_state,
        "evidence_kind": str(scenario.evidence_kind),
        "quality_dataset_id": scenario.quality_dataset_id,
        "required_metrics": [
            "ttft_ms", "itl_or_tpot_ms", "end_to_end_ms", "input_tokens", "output_tokens",
            "output_tokens_per_second", "queue_ms", "cache_hit_rate", "kv_cache_memory",
            "acceptance_rate", "mean_accepted_tokens", "success_rejection_timeout_cancellation_counts",
            "quality_parity_record_id",
        ],
        "policy": asdict(scenario.policy),
        "prohibitions": [
            "no raw prompt or response capture",
            "no production write tools",
            "no automatic DATA-106 mutation",
            "no authority grant",
            "no use of WP-008",
        ],
    }
