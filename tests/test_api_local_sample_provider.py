from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_local_sample_provider_health_endpoint_is_safe() -> None:
    body = TestClient(app).get("/local-sample-provider/health").json()

    assert body["service"] == "stark-terminal-local-sample-provider"
    assert body["enabled"] is True
    assert body["provider_name"] == "local_sample"
    assert body["provider_type"] == "LOCAL_SAMPLE"
    assert body["synthetic_only"] is True
    assert body["real_data_allowed"] is False
    assert body["network_allowed"] is False
    assert body["credentials_required"] is False
    assert body["guardrail_decision"] == "ALLOW"
    assert body["status"] == "HEALTHY"
    assert "secret" not in str(body).lower()


def test_local_sample_provider_contracts_endpoint_is_fail_closed() -> None:
    body = TestClient(app).get("/local-sample-provider/contracts").json()

    assert body["service"] == "stark-terminal-local-sample-provider"
    assert body["provider_name"] == "local_sample"
    assert body["synthetic_only"] is True
    assert body["real_market_data"] is False
    assert body["network_calls"] is False
    assert body["credentials_required"] is False
    assert "INSTRUMENT_MASTER" in body["supported_capabilities"]
    assert "HISTORICAL_BARS" in body["supported_capabilities"]
    assert "LATEST_BAR" in body["unsupported_capabilities"]


def test_local_sample_provider_instruments_endpoint_returns_synthetic_metadata() -> None:
    body = TestClient(app).get("/local-sample-provider/instruments").json()

    assert body["service"] == "stark-terminal-local-sample-provider"
    assert body["synthetic"] is True
    assert body["real_market_data"] is False
    assert body["count"] >= 5
    assert body["errors"] == []
    assert body["source_data_reference"] == "synthetic-local-test-only"
    assert "live" not in str(body).lower()


def test_local_sample_provider_sample_bars_endpoint_returns_tiny_synthetic_sample() -> None:
    body = TestClient(app).get("/local-sample-provider/sample-bars").json()

    assert body["service"] == "stark-terminal-local-sample-provider"
    assert body["synthetic"] is True
    assert body["real_market_data"] is False
    assert 1 <= body["count"] <= 5
    assert len(body["bars"]) == body["count"]
    assert body["errors"] == []
    assert body["source_data_reference"] == "synthetic-local-test-only"
    assert all(bar["provider"]["provider_type"] == "LOCAL_SAMPLE" for bar in body["bars"])
    assert "signal" in body["note"].lower()
