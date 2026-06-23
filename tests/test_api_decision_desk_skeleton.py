from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_decision_desk_api_health_endpoint_is_safe() -> None:
    response = client.get("/decision-desk-api/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-desk-api"
    assert body["enabled"] is True
    assert body["stage"] == "contract_skeleton"
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    assert body["returns_unavailable_by_default"] is True
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_decision_desk_api_contracts_endpoint_is_skeleton_only() -> None:
    response = client.get("/decision-desk-api/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-desk-api"
    assert body["computation_scope"] == "contract-skeleton-only"
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["approval_allowed_now"] is False
    assert body["override_allowed_now"] is False
    assert body["returns_unavailable_by_default"] is True
    assert "SNAPSHOT_REQUEST" in body["request_kinds"]
    assert "CONTRACT_SKELETON_ONLY" in body["unavailable_reasons"]
    assert "DecisionObject_generation" in body["forbidden_outputs"]


def test_decision_desk_api_templates_return_no_generated_outputs() -> None:
    unavailable = client.get("/decision-desk-api/unavailable-template").json()
    assert unavailable["contract_skeleton_only"] is True
    assert unavailable["unavailable_response"]["unavailable"] is True
    assert unavailable["unavailable_response"]["recommendations_allowed"] is False
    assert unavailable["unavailable_response"]["decision_object_generation_allowed"] is False
    assert unavailable["unavailable_response"]["approval_granted"] is False
    assert unavailable["unavailable_response"]["override_granted"] is False
    assert unavailable["no_recommendations"] is True
    assert unavailable["no_decision_object"] is True
    assert unavailable["no_approval"] is True
    assert unavailable["no_execution"] is True

    placeholder = client.get("/decision-desk-api/response-placeholder").json()
    assert placeholder["no_generated_outputs"] is True
    assert placeholder["recommendation_generated"] is False
    assert placeholder["action_generated"] is False
    assert placeholder["confidence_generated"] is False
    assert placeholder["decision_object_generated"] is False
    assert placeholder["execution_ready"] is False
    assert placeholder["approval_granted"] is False
    assert placeholder["override_granted"] is False
    assert placeholder["response_placeholder"]["unavailable_response"]["unavailable"] is True
    assert "password" not in str(placeholder).lower()
    assert "secret" not in str(placeholder).lower()

