from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_api.routes.strategy_research_workspace_display import (
    router as strategy_research_workspace_display_router,
)


client = TestClient(app)


def _assert_no_dangerous_payload_flags(payload: dict):
    text = str(payload).lower()
    assert "secret" not in text
    assert "credential" not in text
    assert "api_key" not in text
    for key in [
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "paper_ingestion_allowed",
        "paper_parsing_allowed",
        "strategy_generation_allowed",
        "backtesting_allowed",
        "recommendation_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "broker_controls_allowed",
        "execution_allowed",
        "execution_ready",
        "approval_granted",
        "override_granted",
    ]:
        assert payload.get(key, False) is False


def test_strategy_research_workspace_display_health_endpoint_is_safe():
    response = client.get("/strategy-research-workspace-display/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-strategy-research-workspace-display"
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
    assert body["workspace_count"] > 0
    assert body["badge_count"] > 0
    _assert_no_dangerous_payload_flags(body)


def test_strategy_research_workspace_display_contracts_endpoint_is_contract_only():
    response = client.get("/strategy-research-workspace-display/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-strategy-research-workspace-display"
    assert body["computation_scope"] == "display-contract-skeleton-only"
    assert body["returns_unavailable_by_default"] is True
    assert body["workspace_kinds"]
    assert body["artifact_kinds"]
    assert body["paper_kinds"]
    assert body["hypothesis_kinds"]
    assert body["dataset_kinds"]
    assert body["experiment_kinds"]
    assert body["badge_kinds"]
    assert body["forbidden_outputs"]
    assert body["paper_parsing_allowed_now"] is False
    assert body["strategy_generation_allowed_now"] is False
    assert body["backtesting_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    _assert_no_dangerous_payload_flags(body)


def test_strategy_research_workspace_display_unavailable_template_is_fail_closed():
    response = client.get("/strategy-research-workspace-display/unavailable-template")

    assert response.status_code == 200
    body = response.json()
    assert body["display_contract_skeleton_only"] is True
    assert body["unavailable_response"]["unavailable"] is True
    assert body["no_active_ui"] is True
    assert body["no_frontend_components"] is True
    assert body["no_desktop_components"] is True
    assert body["no_paper_ingestion"] is True
    assert body["no_paper_parsing"] is True
    assert body["no_strategy_generation"] is True
    assert body["no_backtesting"] is True
    assert body["no_recommendations"] is True
    assert body["no_decision_object"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_broker_controls"] is True
    assert body["no_execution"] is True
    _assert_no_dangerous_payload_flags(body)


def test_strategy_research_workspace_display_placeholder_workspace_has_no_generated_outputs():
    response = client.get("/strategy-research-workspace-display/placeholder-workspace")

    assert response.status_code == 200
    body = response.json()
    assert body["display_contract_skeleton_only"] is True
    assert body["workspace_placeholders"]
    assert body["artifact_placeholders"]
    assert body["paper_placeholders"]
    assert body["hypothesis_placeholders"]
    assert body["dataset_placeholders"]
    assert body["experiment_placeholders"]
    assert body["badges"]
    assert body["unavailable_response"]
    assert body["no_generated_outputs"] is True
    assert body["no_active_ui"] is True
    assert body["no_paper_parsing"] is True
    assert body["no_strategy_generation"] is True
    assert body["no_backtesting"] is True
    assert body["no_broker_controls"] is True
    assert body["no_execution"] is True
    assert body["paper_ingested"] is False
    assert body["paper_parsed"] is False
    assert body["strategy_generated"] is False
    assert body["backtest_generated"] is False
    assert body["recommendation_generated"] is False
    assert body["decision_object_generated"] is False
    assert body["readiness_to_trade_generated"] is False
    assert body["execution_ready"] is False
    _assert_no_dangerous_payload_flags(body)


def test_strategy_research_workspace_display_adds_no_post_endpoints():
    paths = [
        route.path
        for route in strategy_research_workspace_display_router.routes
        if getattr(route, "path", "").startswith("/strategy-research-workspace-display")
        and "POST" in getattr(route, "methods", set())
    ]

    assert paths == []

