from __future__ import annotations

import json

from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_core.retail_trader_experience_api.contracts import (
    default_retail_trader_experience_api_contract_metadata,
)
from stark_terminal_core.retail_trader_experience_api.responses import (
    default_retail_trader_experience_api_response_placeholder,
)


client = TestClient(app)

API_ENDPOINTS = [
    "/retail-trader-experience-api/health",
    "/retail-trader-experience-api/contracts",
    "/retail-trader-experience-api/unavailable-template",
    "/retail-trader-experience-api/response-placeholder",
]


def test_retail_trader_experience_api_remains_contract_skeleton_only() -> None:
    metadata = default_retail_trader_experience_api_contract_metadata()
    assert metadata.returns_unavailable_by_default is True
    assert metadata.stage.value == "API_CONTRACT_SKELETON"

    for flag in [
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
        "suitability_profiling_allowed",
    ]:
        assert getattr(metadata, flag) is False


def test_retail_trader_experience_api_endpoints_are_read_only_placeholders() -> None:
    for path in API_ENDPOINTS:
        response = client.get(path)
        assert response.status_code == 200, path
        assert client.post(path).status_code in {404, 405}, path

    response_placeholder = default_retail_trader_experience_api_response_placeholder()
    assert response_placeholder.api_contract_skeleton_only is True
    assert response_placeholder.unavailable_response.unavailable is True
    assert response_placeholder.active_ui_generated is False
    assert response_placeholder.recommendation_generated is False
    assert response_placeholder.decision_object_generated is False
    assert response_placeholder.suitability_profile_generated is False
    assert response_placeholder.execution_ready is False


def test_retail_trader_experience_api_has_no_active_trade_endpoint_names() -> None:
    route_paths = {
        getattr(route, "path", "")
        for route in app.routes
        if getattr(route, "path", "").startswith("/retail-trader-experience-api")
    }
    serialized_paths = " ".join(sorted(route_paths)).lower()

    for forbidden in [
        "market-data",
        "recommendation",
        "decisionobject",
        "suitability",
        "broker",
        "execution",
        "order",
        "approval",
        "override",
        "readiness-to-trade",
    ]:
        assert forbidden not in serialized_paths


def test_retail_trader_experience_api_payloads_do_not_generate_outputs() -> None:
    for path in API_ENDPOINTS:
        payload = client.get(path).json()
        serialized = json.dumps(payload).lower()
        for snippet in [
            '"recommendation_generated": true',
            '"action_generated": true',
            '"confidence_generated": true',
            '"decision_object_generated": true',
            '"readiness_to_trade_generated": true',
            '"suitability_profile_generated": true',
            '"execution_ready": true',
            '"approval_granted": true',
            '"override_granted": true',
        ]:
            assert snippet not in serialized, (path, snippet)
