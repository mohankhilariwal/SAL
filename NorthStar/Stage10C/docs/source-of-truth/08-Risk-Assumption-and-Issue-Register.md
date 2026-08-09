# 08 — Risk, Assumption and Issue Register, Stage 10C Overlay

Version `1.17.0`. Preserve inherited items.

## Risks

- `RSK-462` incomplete cost capture; `463` stale rate card; `464` currency error; `465` shared-cost misallocation; `466` tag poisoning; `467` token-cost attack; `468` retry amplification; `469` human-review underestimation; `470` observability underfunding; `471` evaluation sampling bias; `472` retention cost growth; `473` regional egress surprise; `474` discount expiry; `475` average-load under-sizing; `476` peak multiplier error; `477` queue instability; `478` protected-write bottleneck; `479` autoscaling lag; `480` load-test non-representativeness; `481` SLO proxy optimization; `482` error-budget misuse; `483` control failure hidden by aggregate SLO; `484` budget interrupts reconciliation; `485` cost optimizer bypasses evaluation; `486` RTO/RPO chosen by technology only; `487` recovery target untested; `488` backup corruption; `489` readiness evidence tampering; `490` checklist theatre; `491` production route accidental activation; `492` unresolved S08D/S09D ignored; `493` false certification/readiness claim.

## Assumptions

- `ASM-143` CAD is the illustrative currency.
- `ASM-144` configured rates are synthetic.
- `ASM-145` workload profiles are planning assumptions.
- `ASM-146` human loaded rates require Finance validation.
- `ASM-147` provider billing can later be reconciled by stable dimensions.
- `ASM-148` Stage 10B authority and reliability invariants remain unchanged.
- `ASM-149` SLO and RTO/RPO proposals have not been approved.
- `ASM-150` production route remains technically disabled.

## Issues

- `ISS-194` byte-exact Stage 10B repository not mounted.
- `ISS-195` no provider billing adapter.
- `ISS-196` no FOCUS conformance test.
- `ISS-197` no calibrated production workload distribution.
- `ISS-198` no production load test.
- `ISS-199` SLO approval missing.
- `ISS-200` RTO/RPO approval missing.
- `ISS-201` recovery exercise missing.
- `ISS-202` production provenance/signing/admission missing.
- `ISS-203` enterprise audit durability/retention approval missing.
- `ISS-204` Stage 8D unresolved.
- `ISS-205` Stage 9D unresolved.
