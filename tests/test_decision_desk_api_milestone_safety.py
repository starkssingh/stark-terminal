from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)

ENDPOINTS = [
    "/decision-desk/health",
    "/decision-desk/contracts",
    "/decision-desk/readiness-template",
    "/decision-desk/display-boundary",
    "/decision-evidence/health",
    "/decision-evidence/contracts",
    "/decision-evidence/readiness-template",
    "/decision-evidence/human-review-template",
    "/decision-safety/health",
    "/decision-safety/contracts",
    "/decision-safety/readiness-template",
    "/decision-safety/human-review-template",
    "/decision-desk-api/health",
    "/decision-desk-api/contracts",
    "/decision-desk-api/unavailable-template",
    "/decision-desk-api/response-placeholder",
]


def test_decision_milestone_endpoints_work_and_do_not_expose_secrets() -> None:
    for endpoint in ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body_text = str(response.json()).lower()
        assert "password" not in body_text
        assert "secret" not in body_text
        assert "token" not in body_text
        assert "live market data" not in body_text
        assert "real market data allowed" not in body_text


def test_decision_milestone_endpoints_remain_non_decision_surfaces() -> None:
    for endpoint in ENDPOINTS:
        body = client.get(endpoint).json()
        text = str(body).lower()
        assert "execution_allowed': true" not in text
        assert "recommendations_allowed': true" not in text
        assert "action_generation_allowed': true" not in text
        assert "confidence_scoring_allowed': true" not in text
        assert "decision_object_generation_allowed': true" not in text
        assert "approval_granted': true" not in text
        assert "override_granted': true" not in text
        assert "trade_signal': true" not in text


def test_health_endpoint_reports_prompt_41_decision_desk_milestone() -> None:
    body = client.get("/health").json()

    assert body["prompt"] == "54"
    assert body["audit_status"] == "retail-dashboard-boundary-hardening"
    assert body["execution_apis_enabled"] is False
