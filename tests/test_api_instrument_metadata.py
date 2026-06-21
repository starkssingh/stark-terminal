from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


FORBIDDEN_RESPONSE_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_user",
    "clickhouse_password",
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


def test_instrument_metadata_health_returns_safe_status() -> None:
    response = TestClient(app).get("/instrument-metadata/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-instrument-metadata"
    assert body["enabled"] is True
    assert body["validation_required"] is True
    assert body["synthetic_seed_allowed"] is True
    assert "repository_reachable" in body
    assert "instrument_count" in body
    assert body["status"] in {"healthy", "disabled", "unavailable"}
    assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(body))


def test_instrument_metadata_sample_is_synthetic_only() -> None:
    response = TestClient(app).get("/instrument-metadata/sample")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-instrument-metadata"
    assert body["synthetic"] is True
    assert body["real_market_data"] is False
    assert body["count"] >= 5
    assert all(item["metadata"]["fixture"] == "synthetic" for item in body["instruments"])
    assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(body))


def test_instrument_metadata_list_fails_safely_without_external_calls() -> None:
    response = TestClient(app).get("/instrument-metadata/list")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-instrument-metadata"
    assert body["status"] in {"ok", "unavailable"}
    assert body["real_market_data"] is False
    assert body["synthetic_seeded"] is False
    assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(body))
