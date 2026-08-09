# 06 — ADR Register

**Version:** 1.14.0

`ADR-001`–`103` remain accepted. Add:

| ADR | Decision |
|---|---|
| ADR-104 | Complete guardrail/governance scope plus bounded local CP-001 slice; stop before full production control plane. |
| ADR-105 | Use stage-specific local PEPs, not one universal filter. |
| ADR-106 | Deterministic-first; model-assisted controls advisory only. |
| ADR-107 | Hard controls synchronous before the protected effect. |
| ADR-108 | Immutable version-pinned bundles and local verified caches. |
| ADR-109 | Exceptions only for soft controls with scope, expiry and compensation. |
| ADR-110 | Human accountability remains external and digest-bound. |
| ADR-111 | Extend existing CMP-001–011; add no new authority owner or agent. |
| ADR-112 | Minimized evidence; async assurance non-authorizing. |
| ADR-113 | Local JSON executable reference; future OPA/Cedar adapters require semantic conformance. |

Full ADR files are under `docs/adr/`.
