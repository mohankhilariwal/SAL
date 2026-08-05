import importlib.util

import pandas as pd
import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    importlib.util.find_spec("sdmetrics") is None,
    reason="SDMetrics optional dependency not installed",
)
def test_sdmetrics_quality_report_smoke() -> None:
    from sdmetrics.reports.single_table import QualityReport

    real = pd.DataFrame({"amount": [10.0, 12.0, 14.0, 20.0], "category": ["a", "a", "b", "b"]})
    synthetic = pd.DataFrame({"amount": [9.5, 12.5, 15.0, 19.0], "category": ["a", "b", "b", "b"]})
    metadata = {
        "columns": {"amount": {"sdtype": "numerical"}, "category": {"sdtype": "categorical"}}
    }
    report = QualityReport()
    report.generate(real, synthetic, metadata, verbose=False)
    assert 0 <= report.get_score() <= 1
