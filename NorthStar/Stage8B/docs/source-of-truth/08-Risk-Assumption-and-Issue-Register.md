# 08 - Risk, Assumption and Issue Register - S08B Overlay 1.10.0

Inherited items, including `ISS-096` and `ISS-114`-`122`, remain.

## New risks

| ID | Description | Status |
|---|---|---|
| `RSK-275` | Judge silently follows prompt injection embedded in candidate text | active |
| `RSK-276` | Judge rewards style, verbosity or fluency over factual correctness | active |
| `RSK-277` | Position or framing changes reverse preferences | active |
| `RSK-278` | Central tendency hides very good and very bad outputs | active |
| `RSK-279` | Self-preference or familiarity distorts model comparison | active |
| `RSK-280` | Acquiescence or sycophancy rewards agreement with false framing | active |
| `RSK-281` | Authority, bandwagon or confidence signals displace evidence | active |
| `RSK-282` | Language/cultural disparities create unequal evaluation quality | active |
| `RSK-283` | Reference answer anchors the judge to a flawed or stale interpretation | active |
| `RSK-284` | Premature score commitment produces post-hoc rationalization | active |
| `RSK-285` | Panel judges share correlated training and failure modes | active |
| `RSK-286` | Human calibration labels are inconsistent, fatigued or biased | active |
| `RSK-287` | Synthetic calibration data fails to represent production language | active |
| `RSK-288` | Model/provider update invalidates calibration | active |
| `RSK-289` | Raw candidate/reference text leaks through judge telemetry | active |
| `RSK-290` | Judge scores are mistaken for regulatory or deployment authority | active |
| `RSK-291` | Overuse of judges increases latency and cost | active |
| `RSK-292` | Listwise/pairwise evaluation scales poorly or amplifies superficial bias | active |

## New assumptions

| ID | Description |
|---|---|
| `ASM-088` | Future human calibration will use independent qualified reviewers |
| `ASM-089` | A future provider adapter can return schema-constrained JSON |
| `ASM-090` | Judge candidate identity can be hidden in ordinary evaluations |
| `ASM-091` | Authorized evidence references can be supplied without raw protected data |
| `ASM-092` | Production thresholds will be set using real prevalence and risk |
| `ASM-093` | Cross-family judge panels will be considered after model selection |
| `ASM-094` | Stage 8A deterministic hard gates remain available after merge |
| `ASM-095` | Human review capacity exists for disputed or abstained cases |
| `ASM-096` | Replay fixtures are sufficient only to validate plumbing |

## New issues

| ID | Description | Status |
|---|---|---|
| `ISS-123` | User-requested S08B title conflicts with the S08A exact continuation instruction; resolved by ADR-077 | recorded |
| `ISS-124` | No live judge model/provider/version is selected | open |
| `ISS-125` | No independent human calibration study has been executed | open |
| `ISS-126` | No production-derived judge calibration cases exist | open |
| `ISS-127` | No provider token-probability distribution is available for distributional scoring | open |
| `ISS-128` | No multilingual/cultural expert study has been executed | open |
| `ISS-129` | Metrics/regression/deployment gates remain unimplemented | open |
| `ISS-130` | No independent adversarial red-team of the judge has been executed | open |
