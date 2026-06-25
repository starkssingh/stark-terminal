from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)

API_PATHS = [
    "/retail-trader-experience-api/health",
    "/retail-trader-experience-api/contracts",
    "/retail-trader-experience-api/unavailable-template",
    "/retail-trader-experience-api/response-placeholder",
]


def _package_text() -> str:
    package_root = ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api"
    return "\n".join(path.read_text(encoding="utf-8") for path in package_root.glob("*.py"))


def _walk(payload: object):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield key, value
            yield from _walk(value)
    elif isinstance(payload, list):
        for item in payload:
            yield from _walk(item)


def test_retail_trader_experience_api_package_remains_contract_skeleton_only() -> None:
    text = _package_text().lower()

    assert "api_contract_skeleton_only" in text
    assert "unavailable" in text
    for forbidden in [
        "def generate_trader_recommendation",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def build_suitability_profile",
        "def execute_trade",
        "def place_order",
        "decisionobject(",
    ]:
        assert forbidden not in text


def test_retail_trader_experience_api_endpoints_are_read_only_and_safe() -> None:
    for path in API_PATHS:
        response = client.get(path)
        assert response.status_code == 200
        payload = response.json()
        serialized = json.dumps(payload).lower()
        assert "password" not in serialized
        assert "secret" not in serialized
        assert "api_key" not in serialized
        assert "token" not in serialized
        assert '"live_market_data": true' not in serialized
        assert '"real_market_data": true' not in serialized
        assert '"live_data_available": true' not in serialized
        assert "trusted real market data" not in serialized
        assert response.request.method == "GET"
        assert client.post(path).status_code in {404, 405}


def test_retail_trader_experience_api_has_no_forbidden_endpoint_paths() -> None:
    forbidden_path_terms = [
        "market-data",
        "recommendation",
        "decisionobject",
        "suitability",
        "broker",
        "execution",
        "order",
        "approval",
        "override",
    ]

    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-trader-experience-api"):
            assert "POST" not in getattr(route, "methods", set())
            for term in forbidden_path_terms:
                assert term not in path


def test_retail_trader_experience_api_responses_do_not_enable_dangerous_flags() -> None:
    dangerous_keys = {
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
        "active_ui_allowed_now",
        "frontend_components_allowed_now",
        "desktop_components_allowed_now",
        "recommendations_allowed_now",
        "action_generation_allowed_now",
        "confidence_scoring_allowed_now",
        "decision_object_generation_allowed_now",
        "readiness_to_trade_allowed_now",
        "broker_controls_allowed_now",
        "execution_allowed_now",
        "approval_allowed_now",
        "override_allowed_now",
        "suitability_profiling_allowed_now",
        "active_ui_generated",
        "frontend_component_generated",
        "desktop_component_generated",
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "broker_control_generated",
        "suitability_profile_generated",
        "execution_ready",
        "approval_granted",
        "override_granted",
        "active_profile",
        "suitability_profile",
        "trading_permission_profile",
        "active_journey",
        "trading_advice_journey",
        "readiness_to_trade_journey",
        "broker_control_journey",
        "execution_journey",
        "active_dashboard",
        "active_decision_object",
        "recommendation_available",
        "action_available",
        "confidence_available",
        "readiness_to_trade_available",
        "broker_controls_available",
        "execution_available",
        "display_ready",
        "safety_passed",
    }

    for path in API_PATHS:
        payload = client.get(path).json()
        for key, value in _walk(payload):
            if key in dangerous_keys:
                assert value is False, (path, key)
