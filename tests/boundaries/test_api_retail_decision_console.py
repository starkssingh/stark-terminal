from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


RETAIL_DECISION_CONSOLE_ENDPOINTS = [
    "/retail-decision-console/health",
    "/retail-decision-console/productization-plan",
    "/retail-decision-console/ui-boundary",
    "/retail-decision-console/readiness",
    "/retail-decision-console/unavailable-state",
    "/retail-decision-console/navigation-placeholder",
    "/retail-decision-console/section-placeholder",
    "/retail-decision-console/card-placeholder",
    "/retail-decision-console/demo-state",
    "/retail-decision-console/static-state-view-model",
]

DANGEROUS_FLAGS = [
    "live_decisions_enabled",
    "recommendations_enabled",
    "action_generation_enabled",
    "confidence_scoring_enabled",
    "decision_object_generation_enabled",
    "live_market_data_enabled",
    "broker_controls_enabled",
    "order_buttons_enabled",
    "execution_enabled",
]


def _iter_routes(routes):
    for route in routes:
        yield route
        original_router = getattr(route, "original_router", None)
        if original_router is not None:
            yield from _iter_routes(getattr(original_router, "routes", []))


def _assert_no_secrets_or_enabled_dangerous_flags(value) -> None:
    serialized = str(value).lower()
    for secret_term in ["api_key", "token", "password", "secret", "credential"]:
        assert secret_term not in serialized
    if isinstance(value, dict):
        for key, item in value.items():
            if key in DANGEROUS_FLAGS:
                assert item is False
            _assert_no_secrets_or_enabled_dangerous_flags(item)
    elif isinstance(value, list):
        for item in value:
            _assert_no_secrets_or_enabled_dangerous_flags(item)


def test_retail_decision_console_get_endpoints_work() -> None:
    for endpoint in RETAIL_DECISION_CONSOLE_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        assert body["service"] == "stark-terminal-retail-decision-console"
        assert body["productization_plan_only"] is True
        assert body["read_only"] is True
        assert body["unavailable_by_default"] is True
        assert body["live_decisions_enabled"] is False
        assert body["recommendations_enabled"] is False
        assert body["action_generation_enabled"] is False
        assert body["confidence_scoring_enabled"] is False
        assert body["decision_object_generation_enabled"] is False
        assert body["live_market_data_enabled"] is False
        assert body["broker_controls_enabled"] is False
        assert body["order_buttons_enabled"] is False
        assert body["execution_enabled"] is False
        _assert_no_secrets_or_enabled_dangerous_flags(body)


def test_retail_decision_console_routes_are_get_only() -> None:
    routes = [
        route
        for route in _iter_routes(app.routes)
        if getattr(route, "path", "").startswith("/retail-decision-console")
    ]
    discovered = {getattr(route, "path", "") for route in routes}
    assert set(RETAIL_DECISION_CONSOLE_ENDPOINTS) <= discovered
    for route in routes:
        assert getattr(route, "methods", set()) <= {"GET"}


def test_retail_decision_console_routes_have_no_unsafe_paths() -> None:
    forbidden_segments = [
        "broker",
        "order",
        "execution",
        "trade",
        "recommendation",
        "recommendations",
        "confidence",
        "decisionobject",
        "live-market-data",
    ]
    bad: list[str] = []
    for route in _iter_routes(app.routes):
        path = getattr(route, "path", "")
        if not path.startswith("/retail-decision-console"):
            continue
        segments = {segment for segment in path.lower().split("/") if segment}
        for term in forbidden_segments:
            if term in segments:
                bad.append(f"{path}:{term}")

    assert bad == []
