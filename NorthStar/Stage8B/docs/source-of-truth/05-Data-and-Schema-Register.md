# 05 - Data and Schema Register - S08B Overlay 1.10.0

New data objects:
- `DATA-143 JudgePolicy`
- `DATA-144 JudgePromptTemplate`
- `DATA-145 JudgeEvaluationEnvelope`
- `DATA-146 CriterionFinding`
- `DATA-147 JudgeVerdict`
- `DATA-148 JudgeCalibrationCase`
- `DATA-149 JudgeCalibrationDataset`
- `DATA-150 JudgeBiasProbe`
- `DATA-151 JudgeBiasMeasurement`
- `DATA-152 JudgeCalibrationReport`
- `DATA-153 JudgePanelResult`
- `DATA-154 JudgeAuditEvidence`

New interfaces:
- `INT-112 Judge Policy Resolution`
- `INT-113 Judge Envelope Construction`
- `INT-114 Judge Adapter Invocation`
- `INT-115 Judge Output Validation`
- `INT-116 Bias Probe Execution`
- `INT-117 Human-Judge Calibration`
- `INT-118 Qualified Judge Panel Aggregation`
- `INT-119 Judge Evidence Export`
- `INT-120 Judge Eligibility or Quarantine`

All objects and interfaces are advisory and have `authority_effect: none`. Existing `DATA-001`-`142`, `INT-001`-`111` and `TOOL-001`-`006` remain unchanged.
