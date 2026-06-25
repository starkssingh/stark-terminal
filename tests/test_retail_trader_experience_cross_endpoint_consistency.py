from __future__ import annotations

from collections.abc import Iterator

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)

EXPERIENCE_ENDPOINTS = [
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
    "/retail-trader-experience-boundary/health",
    "/retail-trader-experience-boundary/contracts",
    "/retail-trader-experience-boundary/invariants",
]

DANGEROUS_FALSE_KEYS = {
    "active_ui_allowed",
    "active_ui_allowed_now",
    "active_ui_generated",
    "active_ui",
    "rendered_now",
    "frontend_components_allowed",
    "frontend_components_allowed_now",
    "frontend_component_generated",
    "desktop_components_allowed",
    "desktop_components_allowed_now",
    "desktop_component_generated",
    "recommendations_allowed",
    "recommendations_allowed_now",
    "recommendation_generated",
    "recommendation_available",
    "recommendation_widget",
    "recommendation",
    "action_generation_allowed",
    "action_generation_allowed_now",
    "action_generated",
    "action_available",
    "action_widget",
    "action_signal",
    "confidence_scoring_allowed",
    "confidence_scoring_allowed_now",
    "confidence_generated",
    "confidence_available",
    "confidence_widget",
    "confidence_signal",
    "decision_object_generation_allowed",
    "decision_object_generation_allowed_now",
    "decision_object_generated",
    "decision_object_widget",
    "decision_object_signal",
    "active_decision_object",
    "readiness_to_trade_allowed",
    "readiness_to_trade_allowed_now",
    "readiness_to_trade_generated",
    "readiness_to_trade_available",
    "readiness_to_trade_widget",
    "readiness_to_trade",
    "broker_controls_allowed",
    "broker_controls_allowed_now",
    "broker_control_generated",
    "broker_control_enabled",
    "broker_control_widget",
    "broker_control",
    "exposes_broker_controls",
    "execution_allowed",
    "execution_allowed_now",
    "execution_ready",
    "execution_widget",
    "executes_trade",
    "approval_allowed",
    "approval_allowed_now",
    "approval_granted",
    "approval_widget",
    "override_allowed",
    "override_allowed_now",
    "override_granted",
    "override_widget",
    "accepts_market_data_for_trader_decision",
    "generates_recommendation",
    "generates_active_ui",
    "generates_decision_object",
    "generates_suitability_profile",
    "suitability_profiling_allowed",
    "suitability_profiling_allowed_now",
    "suitability_profile",
    "suitability_profile_generated",
    "suitability_profile_widget",
    "suitability_profile_generated",
    "trading_permission_profile",
    "real_market_data",
    "live_data",
    "display_ready",
    "safety_passed",
}

FORBIDDEN_SECRET_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_password",
    "kafka_bootstrap_servers",
    "sasl_password",
    "api_key",
    "token",
    "broker_token",
    "broker_secret",
    "password",
}


def _walk(value: object) -> Iterator[tuple[str | None, object]]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key, nested
            yield from _walk(nested)
    elif isinstance(value, list):
        for nested in value:
            yield None, nested
            yield from _walk(nested)


def test_retail_trader_experience_endpoint_families_are_safe_and_consistent() -> None:
    for endpoint in EXPERIENCE_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        for key, value in _walk(body):
            if key in DANGEROUS_FALSE_KEYS:
                assert value is False, f"{endpoint}:{key}"
            if key is not None:
                assert key.lower() not in FORBIDDEN_SECRET_KEYS, f"{endpoint}:{key}"
        lowered = repr(body).lower()
        assert "trusted real market data" not in lowered
        assert "trading decision" not in lowered


def test_retail_trader_experience_endpoint_families_have_no_post_methods() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/retail-trader-experience"):
            assert "POST" not in methods, path

