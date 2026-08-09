from __future__ import annotations

from dataclasses import replace

from .models import (
    BatchingPolicy,
    CachePolicy,
    DeploymentKind,
    InferenceDeploymentProfile,
    InferenceOptimizationPolicy,
    OptimizationRecommendation,
    OptimizationTechnique,
    SpeculativeDecodingPlan,
    TechniqueAssessment,
    WorkloadSignal,
)


def _assessment(technique: OptimizationTechnique, score: int, decision: str, rationale: str, *gates: str) -> TechniqueAssessment:
    return TechniqueAssessment(technique, score, decision, rationale, tuple(gates))


def recommend_techniques(workload: WorkloadSignal, deployment: InferenceDeploymentProfile) -> tuple[TechniqueAssessment, ...]:
    if workload.status != "active":
        raise ValueError("inactive workload profile cannot receive an optimization recommendation")
    long_context = workload.median_isl_tokens >= 8_000 or workload.p95_isl_tokens >= 48_000
    long_output = workload.median_osl_tokens >= 700 or workload.p95_osl_tokens >= 3_000
    short_output = workload.p95_osl_tokens <= 1_500
    high_concurrency = workload.expected_concurrency >= 16 or workload.batch
    tool_dominated = workload.external_latency_fraction >= 0.45
    cacheable_prefix = workload.repeated_prefix_ratio >= 0.35
    input_grounded = workload.input_output_overlap >= 0.35
    results: list[TechniqueAssessment] = []
    results.append(_assessment(OptimizationTechnique.CONTEXT_REDUCTION, 5 if long_context or workload.context_growth else 2, "select" if long_context or workload.context_growth else "benchmark", "Reduce duplicated or low-value context before buying inference capacity; authoritative evidence and required state cannot be removed.", "citation-coverage parity", "required-state retention", "task-success non-regression"))
    results.append(_assessment(OptimizationTechnique.OUTPUT_LENGTH_CONTROL, 4 if long_output else 3, "select", "Bounded structured outputs reduce decode work, but truncation must fail closed rather than appear complete.", "schema completeness", "no truncation of required findings"))
    results.append(_assessment(OptimizationTechnique.STREAMING, 5 if workload.interactive else 1, "select" if workload.interactive and deployment.supports_streaming else "not_applicable", "Streaming improves perceived responsiveness but does not reduce total compute or authorize partial output.", "partial-output labelling", "final-schema validation"))
    if cacheable_prefix and deployment.supports_prefix_cache:
        cache_decision, cache_score = "select", 5 if long_context else 4
    elif cacheable_prefix:
        cache_decision, cache_score = "benchmark", 3
    else:
        cache_decision, cache_score = "defer", 1
    results.append(_assessment(OptimizationTechnique.PREFIX_CACHING, cache_score, cache_decision, "Reuse only exact immutable prompt prefixes bound to tenant, authorization scope, model, tokenizer and prompt version.", "representative cache-hit rate", "tenant isolation", "cache invalidation"))
    results.append(_assessment(OptimizationTechnique.EXACT_RESPONSE_CACHING, 1, "defer", "Only immutable deterministic metadata may be cached; regulatory assessments and approval-sensitive outputs remain uncached.", "content classification", "freshness and authorization binding"))
    results.append(_assessment(OptimizationTechnique.SEMANTIC_RESPONSE_CACHING, 0, "prohibit", "Semantic similarity is not sufficient to reuse a regulatory conclusion across documents, jurisdictions, users or evidence versions.", "not permitted"))
    if deployment.kind == DeploymentKind.SELF_HOSTED and deployment.supports_continuous_batching:
        batching_decision, batching_score = ("select", 5) if high_concurrency else ("benchmark", 3)
    elif deployment.kind == DeploymentKind.MANAGED_API:
        batching_decision, batching_score = "not_applicable", 1
    else:
        batching_decision, batching_score = "defer", 1
    results.append(_assessment(OptimizationTechnique.CONTINUOUS_BATCHING, batching_score, batching_decision, "Continuous batching is a serving-runtime concern; it is valuable for throughput but can increase queueing and TTFT if poorly tuned.", "p95 TTFT", "success and rejection rate", "fairness by workload class"))
    results.append(_assessment(OptimizationTechnique.CHUNKED_PREFILL, 5 if long_context and deployment.supports_chunked_prefill else 2, "benchmark" if long_context else "defer", "Chunked prefill can improve scheduler fairness for long prompts but must be measured with interactive and long-document traffic together.", "TTFT fairness", "prefill throughput", "no starvation"))
    if deployment.kind == DeploymentKind.SELF_HOSTED and deployment.supports_quantization:
        quant_decision, quant_score = "benchmark", 4 if high_concurrency or long_context else 3
    elif deployment.kind == DeploymentKind.MANAGED_API:
        quant_decision, quant_score = "not_applicable", 1
    else:
        quant_decision, quant_score = "defer", 1
    results.append(_assessment(OptimizationTechnique.QUANTIZATION, quant_score, quant_decision, "Quantization can reduce weight or KV-cache memory and change throughput, but NorthStar requires quality and numerical-stability evidence.", "structured-output validity", "groundedness parity", "memory and throughput measurement"))
    parallel_score = 4 if deployment.kind == DeploymentKind.SELF_HOSTED and long_context else 1
    results.append(_assessment(OptimizationTechnique.TENSOR_PARALLELISM, parallel_score, "benchmark" if parallel_score >= 4 and deployment.supports_parallelism else "defer", "Tensor parallelism is a model-fit and latency trade-off, not a default. Communication overhead must be included.", "hardware topology", "collective-communication profile", "latency/throughput crossover"))
    results.append(_assessment(OptimizationTechnique.PIPELINE_PARALLELISM, 2 if deployment.kind == DeploymentKind.SELF_HOSTED else 0, "defer", "Pipeline parallelism is mainly a model-fit option and may add bubbles and complexity for online latency-sensitive work.", "model-fit necessity", "pipeline-bubble measurement"))
    results.append(_assessment(OptimizationTechnique.DATA_PARALLELISM, 4 if deployment.kind == DeploymentKind.SELF_HOSTED and high_concurrency else 1, "benchmark" if deployment.kind == DeploymentKind.SELF_HOSTED and high_concurrency else "defer", "Data-parallel replicas can scale independent requests but require routing, cache locality and failure-domain design.", "load balancing", "cache locality", "replica failure test"))
    if input_grounded and long_output and not tool_dominated:
        prompt_lookup_score, prompt_lookup_decision = 4, "benchmark"
    elif input_grounded and not short_output:
        prompt_lookup_score, prompt_lookup_decision = 3, "benchmark"
    else:
        prompt_lookup_score, prompt_lookup_decision = 0, "defer"
    results.append(_assessment(OptimizationTechnique.SPECULATIVE_PROMPT_LOOKUP, prompt_lookup_score, prompt_lookup_decision, "Prompt-lookup speculation is most plausible for input-grounded outputs with repeated phrases; it is not assumed beneficial for short or tool-dominated workflows.", "lossless parity", "acceptance rate", "decode and end-to-end improvement", "memory overhead"))
    if deployment.supports_speculative_decoding and long_output and not high_concurrency and not tool_dominated:
        draft_score, draft_decision = 4, "benchmark"
    elif deployment.supports_speculative_decoding and long_output:
        draft_score, draft_decision = 2, "benchmark"
    else:
        draft_score, draft_decision = 0, "defer"
    results.append(_assessment(OptimizationTechnique.SPECULATIVE_DRAFT_MODEL, draft_score, draft_decision, "A draft model adds compute and memory. It is a profile-specific experiment, especially at low-to-moderate concurrency and sufficiently long decode.", "draft-target tokenizer compatibility", "lossless sampling verification", "acceptance distribution", "high-concurrency regression test"))
    results.append(_assessment(OptimizationTechnique.SELF_SPECULATIVE, 2 if deployment.supports_speculative_decoding and long_output else 0, "defer", "Self-speculative methods depend on model/runtime support and are not selected without a compatible model and endpoint.", "runtime support", "quality parity"))
    results.append(_assessment(OptimizationTechnique.MULTI_TOKEN_PREDICTION, 2 if deployment.supports_speculative_decoding and long_output else 0, "defer", "MTP is available only for models with native support; NorthStar has not selected such a model.", "native model support", "quality and latency benchmark"))
    results.append(_assessment(OptimizationTechnique.MODEL_ROUTING, 2, "defer", "Model routing is architecturally relevant but belongs to the next explicit model-selection stage; no automatic route changes are introduced here.", "model catalogue", "risk and residency policy", "cross-model quality evaluation"))
    return tuple(results)


def build_selected_policy(workload: WorkloadSignal, deployment: InferenceDeploymentProfile) -> InferenceOptimizationPolicy:
    if workload.status != "active":
        raise ValueError("inactive workload profile cannot produce a policy")
    long_context = workload.median_isl_tokens >= 8_000 or workload.context_growth
    long_output = workload.median_osl_tokens >= 700 or workload.p95_osl_tokens >= 3_000
    cacheable = workload.repeated_prefix_ratio >= 0.35 and deployment.supports_prefix_cache
    self_hosted = deployment.kind == DeploymentKind.SELF_HOSTED
    high_concurrency = workload.expected_concurrency >= 16 or workload.batch
    prompt_lookup_candidate = deployment.supports_speculative_decoding and workload.input_output_overlap >= 0.35 and long_output and workload.external_latency_fraction < 0.45 and not high_concurrency
    cache_policy = CachePolicy(cacheable, ("provider_prompt" if deployment.kind == DeploymentKind.MANAGED_API else "prefix_kv") if cacheable else "none", "tenant_authorization_model_tokenizer_prompt", True, True, True, True, True, 300 if cacheable else 0, 1024 if cacheable else 0)
    if self_hosted and deployment.supports_continuous_batching:
        batch_mode = "continuous" if high_concurrency else "dynamic"
        max_batch_tokens = 65_536 if long_context else 32_768
    else:
        batch_mode, max_batch_tokens = "none", 0
    batching_policy = BatchingPolicy(batch_mode, max_batch_tokens, max(1, min(workload.expected_concurrency or 1, 32)), 8.0 if workload.interactive else 40.0, bool(self_hosted and deployment.supports_chunked_prefill and long_context), bool(self_hosted and high_concurrency))
    speculative = SpeculativeDecodingPlan("prompt_lookup" if prompt_lookup_candidate else "disabled", prompt_lookup_candidate, None, 4 if prompt_lookup_candidate else 0, 0.55, 0.10, 0.05, 0.20, True, (workload.profile_id,) if prompt_lookup_candidate else tuple())
    output_cap = min(max(workload.median_osl_tokens * 2, 256), max(workload.p95_osl_tokens, 256))
    return InferenceOptimizationPolicy(f"IOP-{workload.profile_id[3:]}-{deployment.deployment_id[4:]}", "1.0.0", 0.15 if long_context else 0.05, output_cap, bool(workload.interactive and deployment.supports_streaming), "none" if self_hosted else "provider_managed", 1, 1, 1, cache_policy, batching_policy, speculative)


def build_recommendation(workload: WorkloadSignal, deployment: InferenceDeploymentProfile, policy: InferenceOptimizationPolicy | None = None) -> OptimizationRecommendation:
    chosen = policy or build_selected_policy(workload, deployment)
    return OptimizationRecommendation(f"IOR-{workload.profile_id[3:]}-{deployment.deployment_id[4:]}", workload.profile_id, deployment.deployment_id, recommend_techniques(workload, deployment), chosen.policy_id, True, False, False)


def disable_speculation(policy: InferenceOptimizationPolicy) -> InferenceOptimizationPolicy:
    return replace(policy, speculative_plan=SpeculativeDecodingPlan("disabled", False, None, 0, policy.speculative_plan.minimum_acceptance_rate, policy.speculative_plan.minimum_decode_improvement, policy.speculative_plan.minimum_e2e_improvement, policy.speculative_plan.maximum_memory_overhead_ratio, policy.speculative_plan.require_lossless_distribution, tuple()))
