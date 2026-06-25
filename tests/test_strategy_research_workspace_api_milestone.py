from __future__ import annotations

import json

from fastapi.testclient import TestClient

from stark_terminal_api.main import app
from stark_terminal_api.routes.strategy_research_workspace_api import (
    router as strategy_research_workspace_api_router,
)


client = TestClient(app)

API_ENDPOINTS = [
    "/strategy-research-workspace-api/health",
    "/strategy-research-workspace-api/contracts",
    "/strategy-research-workspace-api/unavailable-template",
    "/strategy-research-workspace-api/response-placeholder",
]


def test_strategy_research_workspace_api_milestone_endpoints_are_read_only() -> None:
    for path in API_ENDPOINTS:
        assert client.get(path).status_code == 200
        assert client.post(path).status_code in {404, 405}


def test_strategy_research_workspace_api_milestone_has_no_processing_routes() -> None:
    for route in strategy_research_workspace_api_router.routes:
        path = getattr(route, "path", "")
        lowered = path.lower()
        for forbidden in [
            "paper-upload",
            "pdf",
            "arxiv",
            "market-data",
            "parse",
            "generate",
            "backtest",
            "recommendation",
            "decisionobject",
            "broker",
            "execution",
            "approve",
            "override",
        ]:
            assert forbidden not in lowered, (path, forbidden)


def test_strategy_research_workspace_api_milestone_returns_placeholder_metadata_only() -> None:
    for path in API_ENDPOINTS:
        serialized = json.dumps(client.get(path).json()).lower()
        for forbidden in [
            '"paper_ingested": true',
            '"paper_parsed": true',
            '"strategy_generated": true',
            '"strategy_code_generated": true',
            '"backtest_generated": true',
            '"recommendation_generated": true',
            '"action_generated": true',
            '"confidence_generated": true',
            '"decision_object_generated": true',
            '"readiness_to_trade_generated": true',
            '"broker_control_generated": true',
            '"execution_allowed": true',
            '"approval_granted": true',
            '"override_granted": true',
        ]:
            assert forbidden not in serialized, (path, forbidden)
