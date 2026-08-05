from governed_release.security.redaction import redact_value


def test_redacts_sensitive_keys_and_patterns() -> None:
    value = {"account_number": "123456789012", "message": "customer CUST-ABC123 used 123456789012"}
    redacted = redact_value(value)
    assert redacted["account_number"] == "[REDACTED]"
    assert "CUST-ABC123" not in redacted["message"]
    assert "123456789012" not in redacted["message"]
