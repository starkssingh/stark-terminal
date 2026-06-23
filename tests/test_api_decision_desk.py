from fastapi.testclient import TestClient

from stark_terminal_api.main import app


FORBIDDEN_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_password",
    "kafka_bootstrap_servers",
    "broker_secret",
    "broker_token",
}


def _collect_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for nested in value.values():
            keys.update(_collect_keys(nested))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_collect_keys(item))
        return keys
    return set()


def test_decision_desk_health_returns_safe_status() -> None:
    client = TestClient(app)

    response = client.get("/decision-desk/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-decision-desk"
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_objects_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["evidence_required"] is True
    assert body["human_review_required"] is True
    assert body["status"] == "healthy"


def test_decision_desk_contracts_return_placeholders_and_forbidden_outputs() -> None:
    client = TestClient(app)

    response = client.get("/decision-desk/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["computation_scope"] == "planning-and-guardrails-only"
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_objects_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert "BUY_BIAS" in body["planned_action_placeholders"]
    assert "recommendation_generation" in body["forbidden_outputs"]


def test_decision_desk_readiness_template_generates_no_outputs() -> None:
    client = TestClient(app)

    response = client.get("/decision-desk/readiness-template")

    assert response.status_code == 200
    body = response.json()
    assert body["planning_only"] is True
    assert body["recommendations_allowed_now"] is False
    assert body["decision_objects_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["must_not_generate_action_states"] is True
    assert body["must_not_generate_confidence_scores"] is True
    assert body["must_not_generate_decision_objects"] is True
    assert body["must_not_generate_recommendations"] is True
    assert body["readiness_report"]["ready_for_recommendations"] is False
    assert body["readiness_report"]["ready_for_confidence_scoring"] is False
    assert body["readiness_report"]["ready_for_decision_objects"] is False
    assert body["readiness_report"]["ready_for_execution"] is False


def test_decision_desk_display_boundary_is_safe() -> None:
    client = TestClient(app)

    response = client.get("/decision-desk/display-boundary")

    assert response.status_code == 200
    body = response.json()
    assert body["planning_only"] is True
    assert body["no_recommendations"] is True
    assert body["no_confidence"] is True
    assert body["no_execution"] is True
    assert "execution_buttons" in body["forbidden_sections"]


def test_decision_desk_endpoints_do_not_expose_secrets_or_active_decisions() -> None:
    client = TestClient(app)

    for endpoint in [
        "/decision-desk/health",
        "/decision-desk/contracts",
        "/decision-desk/readiness-template",
        "/decision-desk/display-boundary",
    ]:
        body = client.get(endpoint).json()
        body_text = repr(body).lower()
        assert FORBIDDEN_KEYS.isdisjoint(_collect_keys(body))
        assert "decisionobject(" not in body_text
        assert "execution_allowed': true" not in body_text
        assert "recommendations_allowed': true" not in body_text
