from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_time_series_diagnostics_health_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/time-series-diagnostics/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-time-series-diagnostics"
    assert body["enabled"] is True
    assert body["schema_version"] == "v1"
    assert body["real_data_allowed"] is False
    assert body["trade_signals_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["decision_objects_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["require_timezone_aware"] is True
    assert body["default_expected_interval_seconds"] > 0
    assert body["max_observations"] > 0
    assert body["status"] == "healthy"


def test_time_series_diagnostics_contracts_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/time-series-diagnostics/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-time-series-diagnostics"
    assert body["computation_scope"] == "descriptive-time-series-data-quality-diagnostics-v0"
    assert body["real_data_allowed_now"] is False
    assert body["trade_signals_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["decision_objects_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["supported_diagnostics"] == [
        "MONOTONICITY",
        "DUPLICATES",
        "GAPS",
        "IRREGULAR_INTERVALS",
        "SPACING_SUMMARY",
    ]
    assert "ADF" in body["deferred_diagnostics"]
    assert "REGIME_DETECTION" in body["deferred_diagnostics"]
    assert "execution_apis" in body["forbidden_analytics"]


def test_time_series_diagnostics_api_has_no_user_supplied_computation_endpoint() -> None:
    client = TestClient(app)

    assert client.get("/time-series-diagnostics/sample").status_code == 404
    assert client.post("/time-series-diagnostics/contracts", json={}).status_code == 405


def test_time_series_diagnostics_endpoints_do_not_expose_secrets_or_decisions() -> None:
    client = TestClient(app)

    for endpoint in ["/time-series-diagnostics/health", "/time-series-diagnostics/contracts"]:
        body = client.get(endpoint).json()
        text = str(body).lower()
        assert "database_url" not in text
        assert "broker_secret" not in text
        assert "api_key" not in text
        assert "trading_decision" not in text
        assert "trade_signal': true" not in text
        assert "decisionobject" not in text.replace("decisionobjects", "")

