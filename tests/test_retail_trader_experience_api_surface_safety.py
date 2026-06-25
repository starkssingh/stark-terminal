from __future__ import annotations

import json

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)

ENDPOINTS = [
    "/retail-trader-experience/health",
    "/retail-trader-experience/contracts",
    "/retail-trader-experience/placeholder-experience",
    "/retail-trader-experience/readiness-template",
    "/retail-trader-experience-api/health",
    "/retail-trader-experience-api/contracts",
    "/retail-trader-experience-api/unavailable-template",
    "/retail-trader-experience-api/response-placeholder",
    "/retail-trader-experience-display/health",
    "/retail-trader-experience-display/contracts",
    "/retail-trader-experience-display/unavailable-template",
    "/retail-trader-experience-display/placeholder-experience",
]

FALSE_FLAGS = {
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
    "readiness_to_trade",
    "broker_control_enabled",
    "approval_granted",
    "override_granted",
    "active_profile",
    "suitability_profile",
    "trading_permission_profile",
    "active_journey",
    "trading_advice_journey",
    "active_dashboard",
    "active_ui",
    "active_decision_object",
    "safety_passed",
    "display_ready",
}


def _walk(payload: object):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield key, value
            yield from _walk(value)
    elif isinstance(payload, list):
        for item in payload:
            yield from _walk(item)


def test_retail_trader_experience_endpoint_families_work() -> None:
    for path in ENDPOINTS:
        response = client.get(path)
        assert response.status_code == 200, path


def test_retail_trader_experience_endpoint_families_are_read_only() -> None:
    for path in ENDPOINTS:
        assert client.post(path).status_code in {404, 405}

    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-trader-experience"):
            methods = getattr(route, "methods", set())
            assert methods <= {"GET", "HEAD", "OPTIONS"}


def test_retail_trader_experience_endpoint_payloads_do_not_expose_secrets_or_live_data() -> None:
    for path in ENDPOINTS:
        payload = client.get(path).json()
        serialized = json.dumps(payload).lower()
        for forbidden in [
            "password",
            "api_key",
            "token",
            "secret",
            "credential",
            '"live_market_data": true',
            '"real_market_data": true',
            '"live_data_available": true',
            "trusted real market data",
        ]:
            assert forbidden not in serialized, (path, forbidden)


def test_retail_trader_experience_endpoint_payloads_keep_dangerous_flags_false() -> None:
    for path in ENDPOINTS:
        payload = client.get(path).json()
        for key, value in _walk(payload):
            if key in FALSE_FLAGS:
                assert value is False, (path, key)


def test_retail_trader_experience_endpoint_payloads_do_not_return_active_trade_outputs() -> None:
    active_output_snippets = [
        '"decision_object_generated": true',
        '"recommendation_generated": true',
        '"action_generated": true',
        '"confidence_generated": true',
        '"readiness_to_trade_generated": true',
        '"suitability_profile_generated": true',
        '"execution_ready": true',
        '"approval_granted": true',
        '"override_granted": true',
    ]

    for path in ENDPOINTS:
        serialized = json.dumps(client.get(path).json()).lower()
        for snippet in active_output_snippets:
            assert snippet not in serialized, (path, snippet)
