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


def test_synthetic_ohlcv_storage_health_endpoint_is_safe() -> None:
    client = TestClient(app)

    response = client.get("/synthetic-ohlcv-storage/health")
    body = response.json()

    assert response.status_code == 200
    assert body["service"] == "stark-terminal-synthetic-ohlcv-storage"
    assert body["stores_real_data"] is False
    assert body["timescale_required_for_tests"] is False
    assert FORBIDDEN_KEYS.isdisjoint(_collect_keys(body))


def test_synthetic_ohlcv_storage_sample_endpoint_is_synthetic_only() -> None:
    client = TestClient(app)

    response = client.get("/synthetic-ohlcv-storage/sample")
    body = response.json()

    assert response.status_code == 200
    assert body["synthetic"] is True
    assert body["real_market_data"] is False
    assert body["stores_real_data"] is False
    assert body["timescale_required_for_tests"] is False
    assert body["sample_result"]["stored"] is False
    assert body["sample_result"]["bar_count"] == 3
    assert FORBIDDEN_KEYS.isdisjoint(_collect_keys(body))


def test_synthetic_ohlcv_storage_contracts_endpoint_does_not_connect_externally() -> None:
    client = TestClient(app)

    response = client.get("/synthetic-ohlcv-storage/contracts")
    body = response.json()

    assert response.status_code == 200
    assert body["schema_version"] == "v1"
    assert body["idempotency_key_description"] == "instrument_id + timeframe + timestamp + provider_id"
    assert body["real_market_data"] is False
    assert body["stores_real_data"] is False
    assert body["timescale_required_for_tests"] is False
    assert FORBIDDEN_KEYS.isdisjoint(_collect_keys(body))
