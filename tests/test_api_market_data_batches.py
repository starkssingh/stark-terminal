from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


FORBIDDEN_RESPONSE_KEYS = {
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


def test_market_data_batches_health_returns_safe_status() -> None:
    response = TestClient(app).get("/market-data-batches/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-market-data-batches"
    assert body["enabled"] is True
    assert body["validation_required"] is True
    assert body["synthetic_allowed"] is True
    assert body["stores_full_bars"] is False
    assert body["status"] in {"healthy", "disabled", "unavailable"}
    assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(body))


def test_market_data_batches_sample_is_synthetic_metadata_only() -> None:
    response = TestClient(app).get("/market-data-batches/sample")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-market-data-batches"
    assert body["synthetic"] is True
    assert body["real_market_data"] is False
    assert body["stores_full_bars"] is False
    assert body["metadata"]["synthetic"] is True
    assert body["metadata"]["row_count"] == 5
    assert "bars" not in body["metadata"]
    assert "synthetic metadata only" in body["note"]
    assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(body))


def test_market_data_batches_list_fails_safely_without_table() -> None:
    response = TestClient(app).get("/market-data-batches/list")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-market-data-batches"
    assert body["status"] in {"ok", "unavailable"}
    assert body["stores_full_bars"] is False
    assert body["real_market_data"] is False
    assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(body))
