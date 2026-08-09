# 08 Risk, Assumption and Issue Register - S08C Overlay 1.11.0

Inherited risks/issues remain active, including `ISS-096`, `ISS-114`-`130`.

## New risks
- `RSK-293`: matched variants may not be semantically equivalent.
- `RSK-294`: repeated trials remain correlated.
- `RSK-295`: synthetic prevalence can mislead threshold selection.
- `RSK-296`: multiple comparisons create false discoveries.
- `RSK-297`: small slices create unstable disparity claims.
- `RSK-298`: translation changes pragmatic meaning.
- `RSK-299`: candidate fingerprints reveal generator family.
- `RSK-300`: order counterbalancing does not remove all context effects.
- `RSK-301`: bootstrap intervals understate structural model uncertainty.
- `RSK-302`: adaptive prompt injection defeats static probes.
- `RSK-303`: quarantine labels may be treated as deployment decisions.
- `RSK-304`: replay fixtures create false confidence.
- `RSK-305`: dataset leakage/contamination.
- `RSK-306`: audit payload over-collection.
- `RSK-307`: lab compute/cost growth with factorial combinations.
- `RSK-308`: human reviewers share the same surface biases.
- `RSK-309`: aggregate reporting hides rare critical failures.

## Assumptions
`ASM-097` synthetic rows contain no customer data; `ASM-098` pair IDs identify intended equivalents; `ASM-099` three repetitions test plumbing only; `ASM-100` replay fixtures are deterministic; `ASM-101` locale review will be performed before real multilingual claims; `ASM-102` no live judge route exists; `ASM-103` critical failures remain non-overridable; `ASM-104` future thresholds require production prevalence and human evidence.

## Issues
- `ISS-131`: full ten-file `1.10.0` merged repository was not mounted; S08C is a compatible overlay.
- `ISS-132`: explicit S08C title conflicts with the S08B continuation instruction; resolved by `ADR-083`, with metrics/gates deferred.
- `ISS-133`: no live judge execution.
- `ISS-134`: no independent real human annotation study.
- `ISS-135`: no production-derived or prevalence-weighted sample.
- `ISS-136`: no adaptive optimization red-team.
- `ISS-137`: no approved production thresholds or power analysis.
- `ISS-138`: no enterprise registry/WORM/retention implementation.
- `ISS-139`: Stage 7D routing and CI/CD deployment gates remain unresolved.
