from __future__ import annotations

import json

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)

ENDPOINTS = [
    "/strategy-research-workspace/health",
    "/strategy-research-workspace/contracts",
    "/strategy-research-workspace/placeholder-workspace",
    "/strategy-research-workspace/readiness-template",
    "/strategy-research-workspace-api/health",
    "/strategy-research-workspace-api/contracts",
    "/strategy-research-workspace-api/unavailable-template",
    "/strategy-research-workspace-api/response-placeholder",
    "/strategy-research-workspace-display/health",
    "/strategy-research-workspace-display/contracts",
    "/strategy-research-workspace-display/unavailable-template",
    "/strategy-research-workspace-display/placeholder-workspace",
]

FALSE_FLAGS = {
    "active_ui_allowed",
    "frontend_components_allowed",
    "desktop_components_allowed",
    "paper_ingestion_allowed",
    "paper_parsing_allowed",
    "strategy_generation_allowed",
    "strategy_code_generation_allowed",
    "backtesting_allowed",
    "optimization_allowed",
    "recommendations_allowed",
    "action_generation_allowed",
    "confidence_scoring_allowed",
    "decision_object_generation_allowed",
    "readiness_to_trade_allowed",
    "broker_controls_allowed",
    "execution_allowed",
    "approval_allowed",
    "override_allowed",
    "active_ui_allowed_now",
    "frontend_components_allowed_now",
    "desktop_components_allowed_now",
    "paper_ingestion_allowed_now",
    "paper_parsing_allowed_now",
    "strategy_generation_allowed_now",
    "strategy_code_generation_allowed_now",
    "backtesting_allowed_now",
    "optimization_allowed_now",
    "recommendations_allowed_now",
    "action_generation_allowed_now",
    "confidence_scoring_allowed_now",
    "decision_object_generation_allowed_now",
    "readiness_to_trade_allowed_now",
    "broker_controls_allowed_now",
    "execution_allowed_now",
    "approval_allowed_now",
    "override_allowed_now",
    "active_ui_generated",
    "frontend_component_generated",
    "desktop_component_generated",
    "paper_ingested",
    "paper_parsed",
    "strategy_generated",
    "strategy_code_generated",
    "backtest_generated",
    "optimization_generated",
    "recommendation_generated",
    "action_generated",
    "confidence_generated",
    "decision_object_generated",
    "readiness_to_trade_generated",
    "broker_control_generated",
    "execution_ready",
    "approval_granted",
    "override_granted",
    "real_market_data",
    "live_data",
    "safety_passed",
    "display_ready",
}


def _walk(payload: object):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield key, value
            yield from _walk(value)
    elif isinstance(payload, list):
        for item in payload:
            yield from _walk(item)


def test_strategy_research_workspace_endpoint_families_work() -> None:
    for path in ENDPOINTS:
        response = client.get(path)
        assert response.status_code == 200, path


def test_strategy_research_workspace_endpoint_families_are_read_only() -> None:
    for path in ENDPOINTS:
        assert client.post(path).status_code in {404, 405}

    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/strategy-research-workspace"):
            assert getattr(route, "methods", set()) <= {"GET", "HEAD", "OPTIONS"}


def test_strategy_research_workspace_endpoint_payloads_do_not_expose_secrets_or_live_data_claims() -> None:
    for path in ENDPOINTS:
        payload = client.get(path).json()
        serialized = json.dumps(payload).lower()
        for forbidden in [
            "password",
            "api_key",
            "token",
            "secret",
            "credential",
            '"live_market_data": true',
            '"real_market_data": true',
            '"live_data": true',
        ]:
            assert forbidden not in serialized, (path, forbidden)


def test_strategy_research_workspace_endpoint_payloads_keep_dangerous_flags_false() -> None:
    for path in ENDPOINTS:
        payload = client.get(path).json()
        for key, value in _walk(payload):
            if key in FALSE_FLAGS:
                assert value is False, (path, key)


def test_strategy_research_workspace_endpoint_payloads_do_not_return_active_research_outputs() -> None:
    snippets = [
        '"paper_ingested": true',
        '"paper_parsed": true',
        '"strategy_generated": true',
        '"strategy_code_generated": true',
        '"backtest_generated": true',
        '"optimization_generated": true',
        '"recommendation_generated": true',
        '"action_generated": true',
        '"confidence_generated": true',
        '"decision_object_generated": true',
        '"readiness_to_trade_generated": true',
        '"execution_ready": true',
        '"approval_granted": true',
        '"override_granted": true',
    ]

    for path in ENDPOINTS:
        serialized = json.dumps(client.get(path).json()).lower()
        for snippet in snippets:
            assert snippet not in serialized, (path, snippet)
