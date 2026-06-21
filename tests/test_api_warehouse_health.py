from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_warehouse_health_endpoint_returns_expected_keys() -> None:
    body = TestClient(app).get("/warehouse/health").json()

    assert body["service"] == "stark-terminal-warehouse"
    assert body["configured"] is False
    assert body["enabled"] is False
    assert body["reachable"] is True
    assert body["backend"] == "memory"
    assert body["memory_fallback_enabled"] is True
    assert body["clickhouse_url_present"] is False
    assert body["database"] == "stark_terminal"
    assert body["schema_version"] == "v1"
    assert body["table_contract_count"] == 6
    assert "password" not in str(body).lower()


def test_warehouse_contracts_endpoint_returns_contracts_without_connecting() -> None:
    body = TestClient(app).get("/warehouse/contracts").json()

    assert body["service"] == "stark-terminal-warehouse"
    assert body["schema_version"] == "v1"
    assert body["count"] == 6
    assert body["contracts"][0]["table_name"] == "analytical_ohlcv_bars"
    assert "CREATE TABLE" not in str(body)
