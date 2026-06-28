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
    "/synthetic-ohlcv-storage/health",
    "/synthetic-ohlcv-exports/health",
    "/provider-guardrails/health",
    "/provider-readiness/health",
    "/local-sample-provider/health",
    "/local-file-provider/health",
    "/analytics-foundation/health",
    "/numerical-analytics/health",
    "/returns-analytics/health",
    "/risk-analytics/health",
    "/relationship-analytics/health",
    "/time-series-diagnostics/health",
    "/regime-analytics/health",
    "/regime-features/health",
    "/decision-desk/health",
    "/decision-evidence/health",
    "/decision-safety/health",
    "/decision-desk-api/health",
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
    "/synthetic-ohlcv-storage/sample",
    "/synthetic-ohlcv-storage/contracts",
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
    "/analytics-foundation/contracts",
    "/analytics-foundation/dependencies",
    "/numerical-analytics/contracts",
    "/numerical-analytics/dependency-gate",
    "/returns-analytics/contracts",
    "/risk-analytics/contracts",
    "/relationship-analytics/contracts",
    "/time-series-diagnostics/contracts",
    "/regime-analytics/contracts",
    "/regime-analytics/readiness-template",
    "/regime-analytics/dependency-gate",
    "/regime-features/contracts",
    "/regime-features/readiness-template",
    "/regime-features/dependency-gate",
    "/decision-desk/contracts",
    "/decision-desk/readiness-template",
    "/decision-desk/display-boundary",
    "/decision-evidence/contracts",
    "/decision-evidence/readiness-template",
    "/decision-evidence/human-review-template",
    "/decision-safety/contracts",
    "/decision-safety/readiness-template",
    "/decision-safety/human-review-template",
    "/decision-desk-api/contracts",
    "/decision-desk-api/unavailable-template",
    "/decision-desk-api/response-placeholder",
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


def test_health_endpoint_reports_prompt_34_audit_status() -> None:
    client = TestClient(app)

    body = client.get("/health").json()

    assert body["prompt"] == "107"
    assert body["audit_status"] == "retail-decision-console-internal-preview-milestone-closure"
    assert body["execution_apis_enabled"] is False


def test_health_surface_does_not_expose_raw_secret_keys() -> None:
    client = TestClient(app)

    for endpoint in [*HEALTH_ENDPOINTS, *OPTIONAL_SAFE_ENDPOINTS, "/config"]:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(response.json()))
