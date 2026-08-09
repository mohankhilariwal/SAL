# 06 — ADR Register: Stage 10B Overlay

Version: `1.16.0`

Preserve `ADR-001`–`124`. Add:

- `ADR-125`: Resolve the scope conflict by implementing reliability plus bounded deployment/AgentOps reference controls, while excluding production activation and FinOps.
- `ADR-126`: Use a provider-neutral failure taxonomy based on permanence, ambiguity, effect class and control domain.
- `ADR-127`: Retry only explicitly transient, idempotent operations within an operation-specific attempt and total-time budget.
- `ADR-128`: Use exponential backoff with full jitter and deadline propagation; avoid retries at multiple stack layers.
- `ADR-129`: Isolate dependencies with per-dependency circuit breakers and bounded bulkheads; overload is rejected or degraded rather than queued without limit.
- `ADR-130`: Use atomic digest-verified workflow checkpoints for resumption; prohibit checkpoint or audit replay into `DATA-106`.
- `ADR-131`: Quarantine permanent/poison messages in a metadata-minimized dead-letter queue; require authenticated manual redrive.
- `ADR-132`: Reconcile ambiguous protected outcomes by idempotency reference before retry; compensation executes only through `CMP-005` under current authority and approval.
- `ADR-133`: Fail closed for authorization, policy, audit, security and integrity failures; permit only labelled read-only degradation when evidence freshness and purpose allow it.
- `ADR-134`: Use local containers and illustrative Kubernetes rolling deployment artefacts for this stage; do not claim a production deployment.
- `ADR-135`: Bind source, configuration, graph, agent specification and test evidence in an immutable release manifest.
- `ADR-136`: Require quality, security, recovery, compatibility and human gates; deny production promotion while S08D/S09D and production routing remain unresolved.
- `ADR-137`: Define DR boundaries and restore tests now, but defer enterprise RTO/RPO, multi-region topology and failover claims to accountable owners.
