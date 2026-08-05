from fastapi.testclient import TestClient

from governed_release.api.app import app


def test_health_and_scenarios() -> None:
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    scenarios = client.get("/scenarios").json()
    assert len(scenarios) == 4
