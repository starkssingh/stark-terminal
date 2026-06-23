from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


ENDPOINTS = [
    "/retail-dashboard/health",
    "/retail-dashboard/contracts",
    "/retail-dashboard/placeholder-layout",
    "/retail-dashboard/readiness-template",
    "/retail-dashboard-api/health",
    "/retail-dashboard-api/contracts",
    "/retail-dashboard-api/unavailable-template",
    "/retail-dashboard-api/response-placeholder",
    "/retail-dashboard-display/health",
    "/retail-dashboard-display/contracts",
    "/retail-dashboard-display/unavailable-template",
    "/retail-dashboard-display/placeholder-layout",
]


def test_retail_dashboard_health_endpoints_work() -> None:
    for endpoint in [
        "/retail-dashboard/health",
        "/retail-dashboard-api/health",
        "/retail-dashboard-display/health",
    ]:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


def test_retail_dashboard_contract_and_template_endpoints_work() -> None:
    for endpoint in ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200


def test_retail_dashboard_responses_do_not_expose_secrets_or_live_data_claims() -> None:
    for endpoint in ENDPOINTS:
        text = str(client.get(endpoint).json()).lower()
        assert "password" not in text
        assert "secret" not in text
        assert "api_key" not in text
        assert "token" not in text
        assert "'live_data': true" not in text
        assert "'real_market_data': true" not in text


def test_retail_dashboard_responses_do_not_generate_trading_outputs() -> None:
    for endpoint in ENDPOINTS:
        body = client.get(endpoint).json()
        text = str(body).lower()
        assert "trading signal" not in text
        assert body.get("recommendation_generated", False) is False
        assert body.get("action_generated", False) is False
        assert body.get("confidence_generated", False) is False
        assert body.get("decision_object_generated", False) is False
        assert body.get("readiness_to_trade_generated", False) is False
        assert body.get("broker_control_generated", False) is False
        assert body.get("execution_ready", False) is False
        assert body.get("approval_granted", False) is False
        assert body.get("override_granted", False) is False


def test_retail_dashboard_openapi_has_no_mutating_dashboard_endpoints() -> None:
    for path, operations in app.openapi()["paths"].items():
        if path.startswith(("/retail-dashboard", "/retail-dashboard-api", "/retail-dashboard-display")):
            assert "post" not in operations
            assert "put" not in operations
            assert "patch" not in operations
            assert "delete" not in operations
