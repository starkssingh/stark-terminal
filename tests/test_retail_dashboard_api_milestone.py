from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_core.retail_dashboard_api.contracts import (
    default_retail_dashboard_api_contract_metadata,
)
from stark_terminal_core.retail_dashboard_api.responses import (
    default_retail_dashboard_api_response_placeholder,
)


client = TestClient(app)


def test_retail_dashboard_api_remains_contract_skeleton_only() -> None:
    metadata = default_retail_dashboard_api_contract_metadata()

    assert metadata.stage.value.lower() == "api_contract_skeleton"
    assert metadata.returns_unavailable_by_default is True
    assert metadata.active_ui_allowed is False
    assert metadata.recommendations_allowed is False
    assert metadata.action_generation_allowed is False
    assert metadata.confidence_scoring_allowed is False
    assert metadata.decision_object_generation_allowed is False
    assert metadata.readiness_to_trade_allowed is False
    assert metadata.broker_controls_allowed is False
    assert metadata.execution_allowed is False
    assert metadata.approval_allowed is False
    assert metadata.override_allowed is False


def test_retail_dashboard_api_response_has_no_generated_outputs() -> None:
    response = default_retail_dashboard_api_response_placeholder()

    assert response.api_contract_skeleton_only is True
    assert response.active_ui_generated is False
    assert response.recommendation_generated is False
    assert response.action_generated is False
    assert response.confidence_generated is False
    assert response.decision_object_generated is False
    assert response.readiness_to_trade_generated is False
    assert response.broker_control_generated is False
    assert response.execution_ready is False
    assert response.approval_granted is False
    assert response.override_granted is False


def test_retail_dashboard_api_endpoints_remain_read_only_placeholders() -> None:
    for endpoint in [
        "/retail-dashboard-api/health",
        "/retail-dashboard-api/contracts",
        "/retail-dashboard-api/unavailable-template",
        "/retail-dashboard-api/response-placeholder",
    ]:
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        assert body.get("recommendation_generated", False) is False
        assert body.get("decision_object_generated", False) is False
        assert body.get("readiness_to_trade_generated", False) is False
        assert body.get("broker_control_generated", False) is False
        assert body.get("execution_ready", False) is False


def test_retail_dashboard_api_has_no_forbidden_endpoint_paths() -> None:
    for path, operations in app.openapi()["paths"].items():
        if path.startswith("/retail-dashboard-api"):
            lowered = path.lower()
            assert "market-data" not in lowered
            assert "recommendation" not in lowered
            assert "active-dashboard" not in lowered
            assert "decisionobject" not in lowered
            assert "broker" not in lowered
            assert "execution" not in lowered
            assert "order" not in lowered
            assert "approval" not in lowered
            assert "override" not in lowered
            assert "post" not in operations
