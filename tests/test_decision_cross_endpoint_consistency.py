from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)

ENDPOINTS = [
    "/decision-desk-api/health",
    "/decision-desk-api/contracts",
    "/decision-desk-api/unavailable-template",
    "/decision-desk-api/response-placeholder",
    "/decision-readiness-api/health",
    "/decision-readiness-api/contracts",
    "/decision-readiness-api/unavailable-template",
    "/decision-readiness-api/response-placeholder",
    "/decision-display/health",
    "/decision-display/contracts",
    "/decision-display/unavailable-template",
    "/decision-display/placeholder-layout",
    "/decision-boundary/health",
    "/decision-boundary/contracts",
    "/decision-boundary/invariants",
    "/decision-evidence-validation/health",
    "/decision-evidence-validation/contracts",
    "/decision-evidence-validation/template",
    "/decision-human-review/health",
    "/decision-human-review/contracts",
    "/decision-human-review/unavailable-template",
    "/decision-human-review/placeholder-workflow",
]

DANGEROUS_TRUE_SNIPPETS = [
    "recommendations_allowed': true",
    "recommendations_allowed_now': true",
    "action_generation_allowed': true",
    "action_generation_allowed_now': true",
    "confidence_scoring_allowed': true",
    "confidence_scoring_allowed_now': true",
    "decision_object_generation_allowed': true",
    "decision_object_generation_allowed_now': true",
    "execution_allowed': true",
    "execution_allowed_now': true",
    "approval_allowed': true",
    "approval_allowed_now': true",
    "override_allowed': true",
    "override_allowed_now': true",
    "active_ui_allowed': true",
    "active_ui_allowed_now': true",
    "active_workflow_allowed': true",
    "active_workflow_allowed_now': true",
    "readiness_to_trade_allowed': true",
    "readiness_to_trade_allowed_now': true",
    "recommendation_generated': true",
    "action_generated': true",
    "confidence_generated': true",
    "decision_object_generated': true",
    "approval_granted': true",
    "override_granted': true",
    "readiness_to_trade_generated': true",
    "execution_ready': true",
    "workflow_active': true",
]


def test_decision_integration_endpoints_work() -> None:
    for endpoint in ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_decision_integration_endpoints_keep_dangerous_flags_false() -> None:
    for endpoint in ENDPOINTS:
        text = str(client.get(endpoint).json()).lower()
        for snippet in DANGEROUS_TRUE_SNIPPETS:
            assert snippet not in text, f"{endpoint} exposed {snippet}"


def test_decision_integration_endpoints_do_not_expose_secrets_or_live_data_claims() -> None:
    for endpoint in ENDPOINTS:
        text = str(client.get(endpoint).json()).lower()
        for forbidden in [
            "password",
            "api_key",
            "broker_secret",
            "access_token",
            "refresh_token",
            "live market data",
            "real market data allowed",
            "production trading",
        ]:
            assert forbidden not in text, f"{endpoint} exposed {forbidden}"


def test_decision_integration_health_status_is_consistent() -> None:
    health_endpoints = [endpoint for endpoint in ENDPOINTS if endpoint.endswith("/health")]
    for endpoint in health_endpoints:
        body = client.get(endpoint).json()
        assert body["status"] == "healthy"
        assert body["execution_allowed"] is False
