from pathlib import Path

from governed_release.adapters.local_files.source_data import generate_maplebridge_source
from governed_release.adapters.sdv.generator import FallbackStatisticalGenerator
from governed_release.adapters.sklearn.evaluators import evaluate_privacy
from governed_release.config.settings import Settings


def test_attack_mode_fails_privacy(tmp_path: Path) -> None:
    settings = Settings(
        data_dir=tmp_path / "data",
        database_url=f"sqlite:///{tmp_path / 'x.db'}",
        generator="fallback",
    )
    source = generate_maplebridge_source(tmp_path / "source.csv", rows=500)
    permitted = source.drop(columns=["transaction_id", "customer_id", "account_number"])
    generator = FallbackStatisticalGenerator()
    safe = generator.generate(permitted, 1000, 7, unsafe_mode=False)
    unsafe = generator.generate(permitted, 1000, 7, unsafe_mode=True)
    safe_report = evaluate_privacy(permitted, safe, settings, 7)
    unsafe_report = evaluate_privacy(permitted, unsafe, settings, 7)
    assert unsafe_report.exact_match_rate >= 0.09
    assert not unsafe_report.passed
    assert unsafe_report.quasi_identifier_risk >= safe_report.quasi_identifier_risk
