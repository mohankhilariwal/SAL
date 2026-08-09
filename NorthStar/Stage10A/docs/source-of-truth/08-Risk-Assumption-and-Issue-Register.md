# 08 — Risk, Assumption and Issue Register — Version 1.15.0 Overlay

Preserve inherited active items. Add:

## Risks

- `RSK-402` — Trace-context spoofing causes false correlation or confused analysis. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-403` — Sensitive prompt/response/retrieval/tool data leaks through telemetry. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-404` — Redaction misses semantic or encoded secrets. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-405` — Mandatory audit event is omitted by instrumentation bypass. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-406` — Audit storage outage blocks protected work. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-407` — Protected effect succeeds but outcome audit fails. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-408` — Local audit key is compromised. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-409` — Privileged administrator edits/deletes ledger. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-410` — Hash-chain validity is mistaken for truthfulness/legal admissibility. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-411` — Telemetry exporter backlog exhausts memory/disk. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-412` — High-cardinality labels create cost/DoS/privacy exposure. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-413` — Clock skew undermines temporal interpretation. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-414` — Duplicate/replayed events distort evidence. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-415` — Sampling removes diagnostics needed for an incident. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-416` — Evidence package exposes excessive sensitive data. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-417` — Audit query access enables insider surveillance. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-418` — Audit/replay is accidentally wired as authority or state writer. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-419` — Retention period conflicts with privacy/records obligations. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-420` — No legal hold/deletion proof. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-421` — No multi-region durability or DR proof. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-422` — No production collector/backend availability SLO. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-423` — GenAI semantic-convention drift breaks adapters. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-424` — Distributed multi-writer ordering is undefined. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-425` — Incorrect canonicalization causes verification mismatch. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-426` — Evidence checkpoint is not independently preserved. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-427` — Operator suppresses capture/retention configuration. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-428` — Telemetry cost obscures business ROI. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-429` — No S09D registry/config integration leaves version gaps. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-430` — No S08D baselines prevents production anomaly thresholds. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.
- `RSK-431` — Local performance guard is misused as a production benchmark. Status: active; controls in TM-001/1.3.0 and S10A tests; residual risk remains.

## Assumptions

- `ASM-127` — Host filesystem supports flush/fsync semantics sufficient for local demonstration.
- `ASM-128` — Local HMAC key is protected from ordinary application users.
- `ASM-129` — Trusted tenant/case/run context is supplied outside trace headers.
- `ASM-130` — Current single-agent/tool inventory remains unchanged during S10A.
- `ASM-131` — Metadata/digests are sufficient for the local evidence demonstration.
- `ASM-132` — No legal/records period can be selected without jurisdictional review.
- `ASM-133` — Future OpenTelemetry adapters preserve canonical NorthStar semantics.
- `ASM-134` — Protected tools expose idempotency/status mechanisms for ambiguous-outcome recovery.

## Issues

- `ISS-170` — S09C formally handed off to S09D; user explicitly selected S10A. Controlled divergence recorded by ADR-114. Status: open.
- `ISS-171` — Enterprise control-plane registries/config/distribution/deployment instrumentation remains incomplete. Status: open.
- `ISS-172` — No production OpenTelemetry SDK/Collector/backend is deployed. Status: open.
- `ISS-173` — No WORM/object-lock or immutable managed ledger is implemented. Status: open.
- `ISS-174` — No asymmetric KMS/HSM signing or trusted timestamp authority. Status: open.
- `ISS-175` — No approved enterprise retention, legal-hold or deletion schedule. Status: open.
- `ISS-176` — No multi-region ledger replication or disaster-recovery proof. Status: open.
- `ISS-177` — No production SLO, sampling, cardinality, volume or cost baseline. Status: open.
- `ISS-178` — No live model/tool/retrieval/human-review instrumentation. Status: open.
- `ISS-179` — Mermaid sources are checked structurally; external renderer certification is not claimed. Status: open.
- `ISS-180` — Stage package is a compatible overlay, not a byte-exact historical repository merge. Status: open.
- `ISS-181` — No production evidence-access approval and distribution workflow. Status: open.
