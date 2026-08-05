from __future__ import annotations

from pathlib import Path

import pytest

from governed_release.application.workflow import build_service
from governed_release.config.settings import Settings


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        data_dir=tmp_path / "data",
        database_url=f"sqlite:///{tmp_path / 'data' / 'test.db'}",
        generator="fallback",
        model_gateway="stub",
        policy_engine="python",
    )


@pytest.fixture
def service(settings: Settings):
    return build_service(settings)
