# 08 — Risk, Assumption and Issue Register: Stage 10B Overlay

Version: `1.16.0`

## New risks

`RSK-432` retry storm; `RSK-433` duplicated protected effect; `RSK-434` false transient classification; `RSK-435` circuit-breaker oscillation; `RSK-436` bulkhead starvation; `RSK-437` checkpoint corruption; `RSK-438` checkpoint schema incompatibility; `RSK-439` poison-message accumulation; `RSK-440` unauthorized redrive; `RSK-441` stale degraded evidence; `RSK-442` fallback model quality/residency mismatch; `RSK-443` compensation creates further harm; `RSK-444` ambiguous external outcome; `RSK-445` audit outage blocks critical workflow; `RSK-446` policy/control-plane outage; `RSK-447` queue overload; `RSK-448` human-review backlog; `RSK-449` rollback does not reverse external effects; `RSK-450` configuration drift; `RSK-451` release-manifest tampering; `RSK-452` canary metric blindness; `RSK-453` supply-chain compromise; `RSK-454` probe-induced restart loop; `RSK-455` PDB misunderstood as protection from involuntary disruption; `RSK-456` backup exists but restore fails; `RSK-457` RTO/RPO unowned; `RSK-458` regional correlated failure; `RSK-459` chaos test escapes isolation; `RSK-460` incident evidence overexposes sensitive data; `RSK-461` false production-readiness confidence.

## New assumptions

- `ASM-135`: Dependency operations can be classified by effect and idempotency semantics.
- `ASM-136`: `CMP-005` can query external outcome by idempotency reference for protected actions selected for automation.
- `ASM-137`: Local filesystem atomic replace is sufficient for the bounded reference checkpoint store, not enterprise durability.
- `ASM-138`: Non-production operators can provide authenticated approval references for redrive and release.
- `ASM-139`: Fallback models/tools, where configured later, will be separately approved for quality, residency and risk.
- `ASM-140`: Kubernetes examples are illustrative and require platform-specific security review.
- `ASM-141`: Enterprise business owners will define accepted RTO/RPO and data-loss tolerances.
- `ASM-142`: S08D/S09D remain unresolved and production promotion is prohibited.

## New issues

- `ISS-182`: User stage title includes reliability, deployment and AgentOps while the S10A handoff names only reliability and failure engineering; resolved by `ADR-125` with bounded scope.
- `ISS-183`: Full historical source-of-truth registers and Stage 10A repository were not supplied; overlays are not byte-exact.
- `ISS-184`: No production workflow engine or distributed checkpoint backend selected.
- `ISS-185`: No enterprise queue/DLQ product selected.
- `ISS-186`: No approved fallback model/tool catalogue exists.
- `ISS-187`: No production SLO/error budget approved.
- `ISS-188`: No enterprise RTO/RPO or business-impact analysis approved.
- `ISS-189`: No multi-region failover or restore proof exists.
- `ISS-190`: No production secrets, signing, provenance-verification or image registry integration exists.
- `ISS-191`: S08D deployment evaluation gates remain unresolved.
- `ISS-192`: S09D enterprise control-plane implementation remains unresolved.
- `ISS-193`: Production route and production promotion remain disabled.
