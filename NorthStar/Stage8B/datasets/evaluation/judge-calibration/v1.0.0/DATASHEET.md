# JDS-001/1.0.0 - Synthetic Judge Calibration Dataset

Purpose: validate Stage 8B judge contracts, bias measurements, output validation and advisory calibration logic.

Composition: 24 synthetic NorthStar regulatory-assessment examples, human-label fixtures, three replay-judge streams and paired perturbation observations.

Important limitations:
- no production data;
- no live model calls;
- no real human annotation study;
- replay outputs intentionally include one biased judge and two calibrated fixtures;
- scores do not estimate production quality;
- no sealed Stage 8A test case is included;
- no hidden chain-of-thought is requested or retained.

Corrections require a new immutable dataset version.
