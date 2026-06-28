from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


DANGEROUS_FLAGS = [
    "live_data_enabled",
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


def test_retail_decision_console_demo_state_endpoint_is_safe() -> None:
    response = client.get("/retail-decision-console/demo-state")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-retail-decision-console"
    assert body["demo_static_state_only"] is True
    assert body["demo_only"] is True
    assert body["unavailable"] is True
    assert body["read_only"] is True
    assert body["no_live_data"] is True
    assert body["no_recommendations"] is True
    assert body["no_action_generation"] is True
    assert body["no_confidence_scoring"] is True
    assert body["no_active_decision_object_generation"] is True
    assert body["no_broker_controls"] is True
    assert body["no_order_buttons"] is True
    assert body["no_execution"] is True
    assert body["demo_state"]["stage"] == "demo_static_state"
    assert body["demo_state"]["demo_only"] is True
    assert body["demo_state"]["unavailable"] is True
    assert body["demo_state"]["provenance"]["demo_only"] is True
    assert body["demo_state"]["provenance"]["static_only"] is True
    assert body["demo_state"]["provenance"]["unavailable"] is True
    assert body["demo_state"]["sections"]
    _assert_no_secrets_or_enabled_dangerous_flags(body)


def test_retail_decision_console_demo_state_route_family_is_get_only() -> None:
    routes = [
        route
        for route in _iter_routes(app.routes)
        if getattr(route, "path", "").startswith("/retail-decision-console")
    ]
    discovered = {getattr(route, "path", "") for route in routes}
    assert "/retail-decision-console/demo-state" in discovered
    for route in routes:
        assert getattr(route, "methods", set()) <= {"GET"}


def test_retail_decision_console_demo_state_adds_no_unsafe_routes() -> None:
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
