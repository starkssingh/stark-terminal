from __future__ import annotations

import json
from typing import Any

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


DATA_FOUNDATION_ENDPOINTS = [
    "/fixtures/health",
    "/fixtures/catalog",
    "/instrument-metadata/health",
    "/instrument-metadata/sample",
    "/market-data-batches/health",
    "/market-data-batches/sample",
]

FORBIDDEN_RESPONSE_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_user",
    "clickhouse_password",
    "kafka_bootstrap_servers",
    "kafka_sasl_username",
    "kafka_sasl_password",
    "broker_secret",
    "broker_token",
    "api_key",
    "token",
}

FORBIDDEN_RESPONSE_CLAIMS = [
    '"real_market_data": true',
    '"live_data": true',
    '"live_market_data": true',
    "trade_signal",
    "trading_signal",
    "recommendation",
    "order_placement",
    "execution",
]


def _collect_keys(value: Any) -> set[str]:
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


def test_data_foundation_api_endpoints_are_available() -> None:
    client = TestClient(app)

    for endpoint in DATA_FOUNDATION_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_data_foundation_api_responses_do_not_expose_secrets_or_live_claims() -> None:
    client = TestClient(app)

    for endpoint in DATA_FOUNDATION_ENDPOINTS:
        response = client.get(endpoint)
        body = response.json()
        body_text = json.dumps(body, sort_keys=True).lower()

        assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(body)), endpoint
        for claim in FORBIDDEN_RESPONSE_CLAIMS:
            assert claim not in body_text, endpoint


def test_fixture_catalog_and_samples_are_synthetic_only() -> None:
    client = TestClient(app)

    fixture_catalog = client.get("/fixtures/catalog").json()
    instrument_sample = client.get("/instrument-metadata/sample").json()
    batch_sample = client.get("/market-data-batches/sample").json()

    assert fixture_catalog["synthetic"] is True
    assert fixture_catalog["real_market_data"] is False
    assert instrument_sample["synthetic"] is True
    assert instrument_sample["real_market_data"] is False
    assert batch_sample["synthetic"] is True
    assert batch_sample["real_market_data"] is False
    assert batch_sample["stores_full_bars"] is False
    assert "bars" not in batch_sample["metadata"]
