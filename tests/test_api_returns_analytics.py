from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def _returns_route_methods() -> dict[str, list[str]]:
    routes: dict[str, list[str]] = {}
    for route in app.routes:
        if hasattr(route, "path") and route.path.startswith("/returns-analytics"):
            routes[route.path] = sorted(route.methods)
        original_router = getattr(route, "original_router", None)
        if original_router is None:
            continue
        for nested in original_router.routes:
            if hasattr(nested, "path") and nested.path.startswith("/returns-analytics"):
                routes[nested.path] = sorted(nested.methods)
    return routes


def test_returns_analytics_health_endpoint_is_safe() -> None:
    response = TestClient(app).get("/returns-analytics/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-returns-analytics"
    assert body["enabled"] is True
    assert body["schema_version"] == "v1"
    assert body["real_data_allowed"] is False
    assert body["trade_signals_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["decision_objects_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["rolling_enabled"] is True
    assert body["rolling_max_window"] == 252
    assert body["status"] == "healthy"


def test_returns_analytics_contracts_endpoint_is_metadata_only() -> None:
    response = TestClient(app).get("/returns-analytics/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["computation_scope"] == "descriptive-returns-and-rolling-windows-v0"
    assert body["real_data_allowed_now"] is False
    assert body["trade_signals_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["decision_objects_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["supported_return_methods"] == ["SIMPLE", "LOG"]
    assert body["supported_rolling_metrics"] == ["MEAN", "MIN", "MAX", "COUNT"]
    assert "volatility" in body["forbidden_analytics"]
    assert "drawdown" in body["forbidden_analytics"]
    assert "correlation_beta" in body["forbidden_analytics"]


def test_returns_analytics_api_does_not_expose_secrets_or_trade_calls() -> None:
    client = TestClient(app)
    text = "\n".join(
        [
            str(client.get("/returns-analytics/health").json()).lower(),
            str(client.get("/returns-analytics/contracts").json()).lower(),
        ]
    )

    assert "password" not in text
    assert "api_key" not in text
    assert "broker_secret" not in text
    assert "trade_signals_allowed_now': true" not in text
    assert "recommendations_allowed_now': true" not in text
    assert "decision_objects_allowed_now': true" not in text


def test_returns_analytics_api_has_no_post_or_user_supplied_compute_route() -> None:
    routes = _returns_route_methods()

    assert routes["/returns-analytics/health"] == ["GET"]
    assert routes["/returns-analytics/contracts"] == ["GET"]
    assert "/returns-analytics/sample" not in routes
    assert all("POST" not in methods for methods in routes.values())
