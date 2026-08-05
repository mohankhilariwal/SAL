import importlib.util

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    importlib.util.find_spec("presidio_analyzer") is None,
    reason="Presidio optional dependency not installed",
)
def test_custom_presidio_pattern_recognizer() -> None:
    from presidio_analyzer import Pattern, PatternRecognizer

    recognizer = PatternRecognizer(
        supported_entity="MAPLEBRIDGE_ACCOUNT",
        patterns=[Pattern("account", r"\b\d{12}\b", 0.8)],
    )
    results = recognizer.analyze("Account 123456789012", entities=["MAPLEBRIDGE_ACCOUNT"])
    assert results
