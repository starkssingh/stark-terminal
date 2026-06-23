from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)

ENDPOINTS = [
    "/decision-readiness-api/health",
    "/decision-readiness-api/contracts",
    "/decision-readiness-api/unavailable-template",
    "/decision-readiness-api/response-placeholder",
    "/decision-display/health",
    "/decision-display/contracts",
    "/decision-display/unavailable-template",
    "/decision-display/placeholder-layout",
    "/decision-evidence-validation/health",
    "/decision-evidence-validation/contracts",
    "/decision-evidence-validation/template",
    "/decision-evidence-validation/sample",
    "/decision-human-review/health",
    "/decision-human-review/contracts",
    "/decision-human-review/unavailable-template",
    "/decision-human-review/placeholder-workflow",
]


def test_decision_phase2_endpoints_work_and_do_not_expose_secrets_or_live_data() -> None:
    for endpoint in ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        text = str(response.json()).lower()
        assert "password" not in text
        assert "secret" not in text
        assert "token" not in text
        assert "live market data" not in text
        assert "real market data allowed" not in text


def test_decision_phase2_endpoints_do_not_generate_dangerous_outputs() -> None:
    for endpoint in ENDPOINTS:
        text = str(client.get(endpoint).json()).lower()
        assert "recommendations_allowed': true" not in text
        assert "action_generation_allowed': true" not in text
        assert "confidence_scoring_allowed': true" not in text
        assert "decision_object_generation_allowed': true" not in text
        assert "readiness_to_trade_allowed': true" not in text
        assert "approval_granted': true" not in text
        assert "override_granted': true" not in text
        assert "execution_allowed': true" not in text
        assert "trade_signal': true" not in text


def test_health_endpoint_reports_prompt_46_milestone_audit_2() -> None:
    body = client.get("/health").json()

    assert body["prompt"] == "54"
    assert body["audit_status"] == "retail-dashboard-boundary-hardening"
    assert body["execution_apis_enabled"] is False
