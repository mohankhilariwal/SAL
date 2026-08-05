import importlib.util

import pytest

from governed_release.adapters.local_files.source_data import generate_maplebridge_source
from governed_release.adapters.sdv.generator import SDVGaussianCopulaGenerator

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    importlib.util.find_spec("sdv") is None, reason="SDV optional dependency not installed"
)
def test_sdv_gaussian_copula_smoke(tmp_path) -> None:
    source = generate_maplebridge_source(tmp_path / "source.csv", rows=150)
    permitted = source.drop(columns=["transaction_id", "customer_id", "account_number"])
    synthetic = SDVGaussianCopulaGenerator().generate(permitted, 50, 42)
    assert len(synthetic) == 50
    assert list(synthetic.columns) == list(permitted.columns)
