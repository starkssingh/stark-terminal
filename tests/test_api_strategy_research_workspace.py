from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def _assert_no_dangerous_payload_flags(payload: dict):
    text = str(payload).lower()
    assert "secret" not in text
    assert "credential" not in text
    assert "api_key" not in text
    assert payload.get("execution_allowed", False) is False
    assert payload.get("execution_allowed_now", False) is False


def test_strategy_research_workspace_health_endpoint_is_safe():
    response = client.get("/strategy-research-workspace/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-strategy-research-workspace"
    assert body["status"] == "healthy"
    assert body["active_ui_allowed"] is False
    assert body["frontend_components_allowed"] is False
    assert body["desktop_components_allowed"] is False
    assert body["paper_ingestion_allowed"] is False
    assert body["paper_parsing_allowed"] is False
    assert body["strategy_generation_allowed"] is False
    assert body["strategy_code_generation_allowed"] is False
    assert body["backtesting_allowed"] is False
    assert body["optimization_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["broker_controls_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    _assert_no_dangerous_payload_flags(body)


def test_strategy_research_workspace_contracts_endpoint_is_planning_only():
    response = client.get("/strategy-research-workspace/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["computation_scope"] == "planning-and-guardrails-only"
    assert body["forbidden_interactions"]
    assert body["strategy_generation_allowed_now"] is False
    assert body["backtesting_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    _assert_no_dangerous_payload_flags(body)


def test_strategy_research_workspace_placeholder_endpoint_has_no_generated_outputs():
    response = client.get("/strategy-research-workspace/placeholder-workspace")

    assert response.status_code == 200
    body = response.json()
    assert body["planning_only"] is True
    assert body["workspaces"]
    assert body["artifacts"]
    assert body["paper_references"]
    assert body["hypotheses"]
    assert body["dataset_references"]
    assert body["experiments"]
    assert body["no_active_ui"] is True
    assert body["no_paper_parsing"] is True
    assert body["no_strategy_generation"] is True
    assert body["no_backtesting"] is True
    assert body["no_recommendations"] is True
    assert body["no_broker_controls"] is True
    assert body["no_execution"] is True
    assert body["strategy_generated"] is False
    assert body["backtest_generated"] is False
    assert body["recommendation_generated"] is False
    assert body["decision_object_generated"] is False
    assert body["readiness_to_trade"] is False
    _assert_no_dangerous_payload_flags(body)


def test_strategy_research_workspace_readiness_template_blocks_active_readiness():
    response = client.get("/strategy-research-workspace/readiness-template")

    assert response.status_code == 200
    body = response.json()
    assert body["planning_only"] is True
    assert body["ready_for_active_ui"] is False
    assert body["ready_for_strategy_generation"] is False
    assert body["ready_for_backtesting"] is False
    assert body["ready_for_recommendations"] is False
    assert body["ready_for_broker_controls"] is False
    assert body["ready_for_execution"] is False
    assert body["no_readiness_to_trade"] is True
    assert body["readiness_report"]["ready_for_execution"] is False
    _assert_no_dangerous_payload_flags(body)


def test_strategy_research_workspace_adds_no_post_endpoints():
    paths = [
        route.path
        for route in app.routes
        if getattr(route, "path", "").startswith("/strategy-research-workspace")
        and "POST" in getattr(route, "methods", set())
    ]

    assert paths == []
