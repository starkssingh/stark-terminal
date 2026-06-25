from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_api.routes.strategy_research_workspace_api import (
    router as strategy_research_workspace_api_router,
)


client = TestClient(app)


def _assert_no_dangerous_payload_flags(payload: dict):
    text = str(payload).lower()
    assert "secret" not in text
    assert "credential" not in text
    assert "api_key" not in text
    assert payload.get("execution_allowed", False) is False
    assert payload.get("execution_allowed_now", False) is False
    assert payload.get("strategy_generation_allowed", False) is False
    assert payload.get("backtesting_allowed", False) is False
    assert payload.get("recommendation_generated", False) is False
    assert payload.get("decision_object_generated", False) is False


def test_strategy_research_workspace_api_health_endpoint_is_safe():
    response = client.get("/strategy-research-workspace-api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-strategy-research-workspace-api"
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


def test_strategy_research_workspace_api_contracts_endpoint_is_contract_only():
    response = client.get("/strategy-research-workspace-api/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-strategy-research-workspace-api"
    assert body["computation_scope"] == "api-contract-skeleton-only"
    assert body["forbidden_outputs"]
    assert body["paper_parsing_allowed_now"] is False
    assert body["strategy_generation_allowed_now"] is False
    assert body["backtesting_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    _assert_no_dangerous_payload_flags(body)


def test_strategy_research_workspace_api_unavailable_template_is_fail_closed():
    response = client.get("/strategy-research-workspace-api/unavailable-template")

    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_skeleton_only"] is True
    assert body["unavailable_response"]["unavailable"] is True
    assert body["no_active_ui"] is True
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


def test_strategy_research_workspace_api_response_placeholder_has_no_generated_outputs():
    response = client.get("/strategy-research-workspace-api/response-placeholder")

    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_skeleton_only"] is True
    assert body["request_placeholder"]
    assert body["response_placeholder"]
    assert body["workspace_reference"]
    assert body["artifact_reference"]
    assert body["paper_reference"]
    assert body["hypothesis_reference"]
    assert body["dataset_reference"]
    assert body["experiment_reference"]
    assert body["safety_reference"]
    assert body["unavailable_response"]
    assert body["no_generated_outputs"] is True
    assert body["no_paper_parsing"] is True
    assert body["no_strategy_generation"] is True
    assert body["no_backtesting"] is True
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


def test_strategy_research_workspace_api_adds_no_post_endpoints():
    paths = [
        route.path
        for route in strategy_research_workspace_api_router.routes
        if getattr(route, "path", "").startswith("/strategy-research-workspace-api")
        and "POST" in getattr(route, "methods", set())
    ]

    assert paths == []
