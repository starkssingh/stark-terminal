from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_core.retail_dashboard_api.contracts import (
    default_retail_dashboard_api_contract_metadata,
)
from stark_terminal_core.retail_dashboard_api.responses import (
    default_retail_dashboard_api_response_placeholder,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/core/stark_terminal_core/retail_dashboard_api"
ROUTE = ROOT / "apps/api/stark_terminal_api/routes/retail_dashboard_api.py"
client = TestClient(app)


def test_retail_dashboard_api_package_remains_contract_skeleton_only() -> None:
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


def test_retail_dashboard_api_response_placeholder_has_no_generated_outputs() -> None:
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


def test_retail_dashboard_api_has_no_forbidden_endpoint_paths() -> None:
    paths = app.openapi()["paths"]
    for path, operations in paths.items():
        if path.startswith("/retail-dashboard-api"):
            lowered = path.lower()
            assert "market-data" not in lowered
            assert "recommendation" not in lowered
            assert "active-dashboard" not in lowered
            assert "decisionobject" not in lowered
            assert "broker" not in lowered
            assert "execution" not in lowered
            assert "order" not in lowered
            assert "post" not in operations


def test_retail_dashboard_api_endpoints_return_placeholder_metadata_only() -> None:
    for endpoint in [
        "/retail-dashboard-api/health",
        "/retail-dashboard-api/contracts",
        "/retail-dashboard-api/unavailable-template",
        "/retail-dashboard-api/response-placeholder",
    ]:
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        text = str(body).lower()
        assert "password" not in text
        assert "secret" not in text
        assert "live data" not in text
        assert body.get("recommendation_generated", False) is False
        assert body.get("decision_object_generated", False) is False
        assert body.get("readiness_to_trade_generated", False) is False
        assert body.get("broker_control_generated", False) is False
        assert body.get("execution_ready", False) is False


def test_retail_dashboard_api_code_has_no_market_data_to_recommendation_path() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in [*PACKAGE.glob("*.py"), ROUTE])
    for phrase in [
        "def generate_dashboard_recommendation",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def create_order_button",
        "@router.post",
    ]:
        assert phrase not in text
