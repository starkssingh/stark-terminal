from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ANALYTICS_ENDPOINTS = [
    "/analytics-foundation/health",
    "/analytics-foundation/contracts",
    "/analytics-foundation/dependencies",
    "/numerical-analytics/health",
    "/numerical-analytics/contracts",
    "/numerical-analytics/dependency-gate",
    "/returns-analytics/health",
    "/returns-analytics/contracts",
    "/risk-analytics/health",
    "/risk-analytics/contracts",
    "/relationship-analytics/health",
    "/relationship-analytics/contracts",
    "/time-series-diagnostics/health",
    "/time-series-diagnostics/contracts",
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
    "password",
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


def test_analytics_milestone_api_endpoints_are_safe() -> None:
    client = TestClient(app)

    for endpoint in ANALYTICS_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        assert FORBIDDEN_RESPONSE_KEYS.isdisjoint(_collect_keys(response.json())), endpoint


def test_analytics_milestone_api_responses_do_not_claim_live_data_or_decisions() -> None:
    client = TestClient(app)

    for endpoint in ANALYTICS_ENDPOINTS:
        body = client.get(endpoint).json()
        text = str(body).lower()
        assert "real_data_allowed': true" not in text
        assert "real_data_allowed_now': true" not in text
        assert "real_market_data': true" not in text
        assert "trade_signals_allowed': true" not in text
        assert "trade_signals_allowed_now': true" not in text
        assert "recommendations_allowed': true" not in text
        assert "recommendations_allowed_now': true" not in text
        assert "decision_objects_allowed': true" not in text
        assert "decision_objects_allowed_now': true" not in text
        assert "execution_allowed': true" not in text
        assert "execution_allowed_now': true" not in text


def test_analytics_milestone_api_has_no_user_supplied_compute_post_routes() -> None:
    analytics_routes = {
        route.path: sorted(route.methods)
        for route in app.routes
        if hasattr(route, "path")
        and (
            route.path.startswith("/analytics-foundation")
            or route.path.startswith("/numerical-analytics")
            or route.path.startswith("/returns-analytics")
            or route.path.startswith("/risk-analytics")
            or route.path.startswith("/relationship-analytics")
            or route.path.startswith("/time-series-diagnostics")
        )
    }

    assert "/returns-analytics/sample" not in analytics_routes
    assert "/risk-analytics/sample" not in analytics_routes
    assert "/relationship-analytics/sample" not in analytics_routes
    assert "/time-series-diagnostics/sample" not in analytics_routes
    assert all("POST" not in methods for methods in analytics_routes.values())


def test_core_health_reports_analytics_milestone_status() -> None:
    body = TestClient(app).get("/health").json()

    assert body["prompt"] == "67"
    assert body["audit_status"] == "strategy-research-workspace-milestone"
    assert body["execution_apis_enabled"] is False
