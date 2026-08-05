from governed_release.application.scenarios import MALICIOUS_REQUEST
from governed_release.security.injection import detect_injection


def test_malicious_request_hits_multiple_controls() -> None:
    findings = detect_injection(MALICIOUS_REQUEST)
    assert "RAW_IDENTIFIER_ACCESS" in findings
    assert "RAW_DATA_EXPORT" in findings
    assert "EVALUATOR_BYPASS" in findings
    assert "POLICY_OVERRIDE" in findings
    assert "UNAPPROVED_DESTINATION" in findings
