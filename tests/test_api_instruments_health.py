from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_instruments_health_endpoint_returns_expected_keys() -> None:
    body = TestClient(app).get("/instruments/health").json()

    assert body["service"] == "stark-terminal-instruments"
    assert body["configured"] is True
    assert body["mode"] == "local"
    assert body["source"] == "synthetic"
    assert body["instrument_count"] == 6
    assert body["external_calls_allowed"] is False
    assert body["provider_network_calls_allowed"] is False
    assert body["status"] == "HEALTHY"
    assert "secret" not in str(body).lower()


def test_providers_health_endpoint_returns_expected_keys() -> None:
    body = TestClient(app).get("/providers/health").json()

    assert body["service"] == "stark-terminal-providers"
    assert body["provider_count"] == 1
    assert body["default_provider"] == "local_sample"
    assert body["external_calls_allowed"] is False
    assert body["network_calls_allowed"] is False
    assert body["providers"] == ["local_sample"]
    assert body["status"] == "HEALTHY"
    assert "secret" not in str(body).lower()


def test_sample_instruments_endpoint_is_synthetic_only() -> None:
    body = TestClient(app).get("/instruments/sample").json()

    assert body["service"] == "stark-terminal-instruments"
    assert body["source"] == "synthetic"
    assert body["count"] == 6
    assert body["live_data"] is False
    assert body["instruments"][0]["metadata"]["fixture"] == "synthetic"
    assert "live" not in body["source"].lower()
