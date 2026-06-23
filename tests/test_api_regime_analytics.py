from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_regime_analytics_health_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/regime-analytics/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-regime-analytics"
    assert body["enabled"] is True
    assert body["schema_version"] == "v1"
    assert body["dependency_stage"] == "planning_only"
    assert body["real_data_allowed"] is False
    assert body["classification_allowed"] is False
    assert body["trade_signals_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["decision_objects_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["evidence_required"] is True
    assert body["human_review_required"] is True
    assert body["planned_label_count"] > 0
    assert body["roadmap_item_count"] > 0
    assert body["status"] == "healthy"


def test_regime_analytics_contracts_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/regime-analytics/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-regime-analytics"
    assert body["computation_scope"] == "planning-and-guardrails-only"
    assert body["classification_allowed_now"] is False
    assert body["real_data_allowed_now"] is False
    assert body["trade_signals_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["decision_objects_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert "TRENDING_UP" in body["planned_labels"]
    assert "RETURNS" in body["required_evidence_kinds"]
    assert "trading_signals" in body["forbidden_outputs"]
    assert "DecisionObject_generation" in body["forbidden_outputs"]


def test_regime_analytics_readiness_template_does_not_classify() -> None:
    client = TestClient(app)

    response = client.get("/regime-analytics/readiness-template")

    assert response.status_code == 200
    body = response.json()
    assert body["planning_only"] is True
    assert body["classification_allowed_now"] is False
    assert body["must_not_classify_market_state"] is True
    assert body["must_not_generate_signals_or_decisions"] is True
    assert body["readiness_report"]["ready_for_classification"] is False
    assert body["readiness_report"]["ready_for_production"] is False


def test_regime_analytics_dependency_gate_endpoint_is_safe() -> None:
    client = TestClient(app)

    response = client.get("/regime-analytics/dependency-gate")

    assert response.status_code == 200
    body = response.json()
    assert body["current_stage"] == "planning_only"
    assert body["heavy_dependencies_blocked"] is True
    assert body["no_classification"] is True
    assert "hmmlearn" in body["blocked_now"]
    assert "ruptures" in body["blocked_now"]


def test_regime_analytics_endpoints_do_not_accept_user_data_or_expose_secrets() -> None:
    client = TestClient(app)

    assert client.post("/regime-analytics/contracts", json={}).status_code == 405
    assert client.post("/regime-analytics/readiness-template", json={}).status_code == 405

    for endpoint in [
        "/regime-analytics/health",
        "/regime-analytics/contracts",
        "/regime-analytics/readiness-template",
        "/regime-analytics/dependency-gate",
    ]:
        body = client.get(endpoint).json()
        text = str(body).lower()
        assert "database_url" not in text
        assert "broker_secret" not in text
        assert "api_key" not in text
        assert "trade_signal': true" not in text
        assert "recommendation': true" not in text
        assert "decision_object_generated': true" not in text
