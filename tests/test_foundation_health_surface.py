from fastapi.testclient import TestClient

from stark_terminal_api.main import app


HEALTH_ENDPOINTS = [
    "/health",
    "/database/health",
    "/timeseries/health",
    "/research-lake/health",
    "/cache/health",
    "/streams/health",
    "/event-backbone/health",
    "/data-quality/health",
    "/fixtures/health",
    "/instrument-metadata/health",
    "/market-data-batches/health",
    "/workers/health",
    "/instruments/health",
    "/providers/health",
    "/warehouse/health",
    "/features/health",
]

OPTIONAL_SAFE_ENDPOINTS = [
    "/warehouse/contracts",
    "/features/contracts",
    "/event-backbone/topics",
    "/data-quality/contracts",
    "/instruments/sample",
    "/fixtures/catalog",
    "/instrument-metadata/sample",
    "/instrument-metadata/list",
    "/market-data-batches/sample",
    "/market-data-batches/list",
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


def test_all_foundation_health_endpoints_return_200() -> None:
    client = TestClient(app)

    for endpoint in HEALTH_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_health_endpoint_reports_prompt_16_audit_status() -> None:
    client = TestClient(app)

    body = client.get("/health").json()

    assert body["prompt"] == "16"
    assert body["audit_status"] == "milestone-a-b"
    assert body["execution_apis_enabled"] is False


def test_health_surface_does_not_expose_raw_secret_keys() -> None:
    client = TestClient(app)

    for endpoint in [*HEALTH_ENDPOINTS, *OPTIONAL_SAFE_ENDPOINTS, "/config"]:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(response.json()))
