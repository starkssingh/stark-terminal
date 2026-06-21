from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_timeseries_health_endpoint_returns_expected_keys() -> None:
    client = TestClient(app)

    response = client.get("/timeseries/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-timeseries"
    assert set(body) == {
        "service",
        "configured",
        "enabled",
        "reachable",
        "extension_available",
        "hypertables_enabled",
        "dialect",
        "error",
    }
    assert body["enabled"] is False
    assert body["reachable"] is False


def test_timeseries_health_endpoint_does_not_expose_raw_url() -> None:
    client = TestClient(app)

    body = client.get("/timeseries/health").json()

    assert "timescale_database_url" not in body
    assert "postgresql" not in str(body).lower()
