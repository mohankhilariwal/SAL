from datetime import datetime, timezone
import pytest
from northstar_compliance.graph.factory import build_runtime

@pytest.fixture
def t0(): return datetime(2026,7,31,18,0,tzinfo=timezone.utc)

@pytest.fixture
def runtime(tmp_path): return build_runtime(tmp_path/'db.sqlite', wait_timeout_seconds=60, lease_seconds=10)
