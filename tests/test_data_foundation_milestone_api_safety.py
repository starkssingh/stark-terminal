from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def _assert_no_secret_or_decision_keys(value: object) -> None:
    text = str(value).lower()
    forbidden = [
        "database_url",
        "redis_url",
        "clickhouse_url",
        "kafka_bootstrap",
        "api_key",
        "token",
        "password",
        "broker_secret",
        "buy bias",
        "sell bias",
        "order placement",
        "broker execution",
    ]
    for term in forbidden:
        assert term not in text


def test_prompt_22_health_marker() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["prompt"] == "54"
    assert body["audit_status"] == "retail-dashboard-boundary-hardening"
    assert body["execution_apis_enabled"] is False


def test_synthetic_storage_export_provider_health_endpoints_are_safe() -> None:
    endpoints = [
        "/synthetic-ohlcv-storage/health",
        "/synthetic-ohlcv-exports/health",
        "/provider-guardrails/health",
        "/provider-readiness/health",
        "/local-sample-provider/health",
        "/local-file-provider/health",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        _assert_no_secret_or_decision_keys(body)


def test_prompt_18_to_21_contract_and_sample_endpoints_are_safe() -> None:
    endpoints = [
        "/synthetic-ohlcv-storage/contracts",
        "/synthetic-ohlcv-storage/sample",
        "/synthetic-ohlcv-exports/contracts",
        "/synthetic-ohlcv-exports/sample",
        "/provider-guardrails/contracts",
        "/provider-guardrails/readiness-template",
        "/provider-readiness/contracts",
        "/provider-readiness/template",
        "/provider-readiness/example-score",
        "/local-sample-provider/contracts",
        "/local-sample-provider/instruments",
        "/local-sample-provider/sample-bars",
        "/local-file-provider/contracts",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        _assert_no_secret_or_decision_keys(body)
        if endpoint.startswith("/local-sample-provider") and endpoint not in {"/local-sample-provider/health"}:
            assert body.get("real_market_data", False) is False
        if endpoint.startswith("/synthetic-ohlcv-exports"):
            assert body.get("real_market_data_allowed", False) is False
        if endpoint.startswith("/provider-guardrails"):
            assert body.get("execution_allowed", False) is False
        if endpoint.startswith("/local-file-provider"):
            assert body.get("real_market_data", False) is False


def test_local_sample_sample_bars_are_labelled_synthetic_not_live() -> None:
    response = client.get("/local-sample-provider/sample-bars")
    assert response.status_code == 200
    body = response.json()
    assert body["synthetic"] is True
    assert body["real_market_data"] is False
    assert body["source_data_reference"] == "synthetic-local-test-only"
    assert body["count"] <= 5
    assert body["bars"]
    _assert_no_secret_or_decision_keys(body)
