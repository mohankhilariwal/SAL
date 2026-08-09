import pytest

from northstar_compliance.observability import TelemetryRedactor


@pytest.mark.parametrize(
    "key",
    ["password", "secret", "api_key", "access_token", "raw_prompt", "raw_response"],
)
def test_893_to_898_secret_keys_are_redacted(key):
    result = TelemetryRedactor().redact({key: "sensitive-value"})
    assert result.sanitized[key] == "[REDACTED]"
    assert key in result.redacted_paths
    assert result.digests[key]


@pytest.mark.parametrize(
    "value,marker",
    [
        ("Bearer abc.def.ghi", "[REDACTED:bearer]"),
        ("contact user@example.com", "[REDACTED:email]"),
        ("4111 1111 1111 1111", "[REDACTED:credit_card_like]"),
        ("-----BEGIN PRIVATE KEY-----", "[REDACTED:private_key]"),
    ],
)
def test_899_to_902_sensitive_patterns_are_redacted(value, marker):
    result = TelemetryRedactor().redact({"message": value})
    assert marker in result.sanitized["message"]
    assert "message" in result.redacted_paths


def test_903_nested_redaction_tracks_paths():
    result = TelemetryRedactor().redact({"outer": {"authorization": "Bearer xyz"}})
    assert result.sanitized["outer"]["authorization"] == "[REDACTED]"
    assert "outer.authorization" in result.redacted_paths


def test_904_redaction_preserves_safe_fields():
    result = TelemetryRedactor().redact({"tool_id": "TOOL-004", "count": 3})
    assert result.sanitized == {"tool_id": "TOOL-004", "count": 3}
    assert result.redacted_paths == []
