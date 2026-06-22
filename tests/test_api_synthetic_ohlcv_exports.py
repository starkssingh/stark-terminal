from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


FORBIDDEN_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "kafka_bootstrap_servers",
    "broker_secret",
    "broker_token",
}


def _collect_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for nested in value.values():
            keys.update(_collect_keys(nested))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_collect_keys(item))
        return keys
    return set()


def test_synthetic_ohlcv_exports_health_endpoint_is_safe() -> None:
    client = TestClient(app)

    response = client.get("/synthetic-ohlcv-exports/health")
    body = response.json()

    assert response.status_code == 200
    assert body["service"] == "stark-terminal-synthetic-ohlcv-exports"
    assert body["synthetic_only"] is True
    assert body["real_market_data_allowed"] is False
    assert body["disk_writes_allowed"] is False
    assert FORBIDDEN_KEYS.isdisjoint(_collect_keys(body))


def test_synthetic_ohlcv_exports_contracts_endpoint_is_metadata_only() -> None:
    client = TestClient(app)

    response = client.get("/synthetic-ohlcv-exports/contracts")
    body = response.json()

    assert response.status_code == 200
    assert body["synthetic_only"] is True
    assert body["real_market_data_allowed"] is False
    assert body["manifest_required"] is True
    assert body["validation_required"] is True
    assert body["writes_files"] is False
    assert body["trading_signals"] is False
    assert FORBIDDEN_KEYS.isdisjoint(_collect_keys(body))


def test_synthetic_ohlcv_exports_sample_endpoint_does_not_write_or_return_bars() -> None:
    client = TestClient(app)

    response = client.get("/synthetic-ohlcv-exports/sample")
    body = response.json()

    assert response.status_code == 200
    assert body["synthetic_only"] is True
    assert body["real_market_data_allowed"] is False
    assert body["writes_files"] is False
    assert body["returns_bars"] is False
    assert body["sample_request"]["synthetic"] is True
    assert body["sample_request"]["source_data_reference"] == "synthetic-local-test-only"
    assert FORBIDDEN_KEYS.isdisjoint(_collect_keys(body))
