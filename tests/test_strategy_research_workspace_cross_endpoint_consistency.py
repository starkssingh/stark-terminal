from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)

STRATEGY_RESEARCH_ENDPOINTS = [
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
    "/strategy-research-workspace-boundary/health",
    "/strategy-research-workspace-boundary/contracts",
    "/strategy-research-workspace-boundary/invariants",
]

DANGEROUS_FALSE_KEYS = {
    "active_ui_allowed",
    "active_ui_allowed_now",
    "active_ui_generated",
    "active_ui",
    "rendered_now",
    "frontend_components_allowed",
    "frontend_components_allowed_now",
    "frontend_component_generated",
    "desktop_components_allowed",
    "desktop_components_allowed_now",
    "desktop_component_generated",
    "paper_ingestion_allowed",
    "paper_ingestion_allowed_now",
    "paper_ingested",
    "paper_parsing_allowed",
    "paper_parsing_allowed_now",
    "paper_parsed",
    "strategy_generation_allowed",
    "strategy_generation_allowed_now",
    "strategy_generated",
    "strategy_code_generation_allowed",
    "strategy_code_generation_allowed_now",
    "strategy_code_generated",
    "backtesting_allowed",
    "backtesting_allowed_now",
    "backtest_generated",
    "optimization_allowed",
    "optimization_allowed_now",
    "optimization_generated",
    "recommendations_allowed",
    "recommendations_allowed_now",
    "recommendation_generated",
    "action_generation_allowed",
    "action_generation_allowed_now",
    "action_generated",
    "confidence_scoring_allowed",
    "confidence_scoring_allowed_now",
    "confidence_generated",
    "decision_object_generation_allowed",
    "decision_object_generation_allowed_now",
    "decision_object_generated",
    "readiness_to_trade_allowed",
    "readiness_to_trade_allowed_now",
    "readiness_to_trade_generated",
    "broker_controls_allowed",
    "broker_controls_allowed_now",
    "broker_control_generated",
    "broker_control_enabled",
    "execution_allowed",
    "execution_allowed_now",
    "execution_ready",
    "executes_trade",
    "approval_allowed",
    "approval_allowed_now",
    "approval_granted",
    "override_allowed",
    "override_allowed_now",
    "override_granted",
    "accepts_paper_input",
    "accepts_market_data_for_research_decision",
    "generates_active_ui",
    "generates_strategy",
    "generates_backtest",
    "generates_recommendation",
    "generates_decision_object",
    "exposes_broker_controls",
    "real_market_data",
    "live_data",
    "display_ready",
    "safety_passed",
}

FORBIDDEN_SECRET_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_password",
    "kafka_bootstrap_servers",
    "sasl_password",
    "api_key",
    "token",
    "broker_token",
    "broker_secret",
    "password",
}


def _walk(value: object) -> Iterator[tuple[str | None, object]]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key, nested
            yield from _walk(nested)
    elif isinstance(value, list):
        for nested in value:
            yield None, nested
            yield from _walk(nested)


def test_strategy_research_workspace_endpoint_families_are_safe_and_consistent() -> None:
    for endpoint in STRATEGY_RESEARCH_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        for key, value in _walk(body):
            if key in DANGEROUS_FALSE_KEYS:
                assert value is False, f"{endpoint}:{key}"
            if key is not None:
                assert key.lower() not in FORBIDDEN_SECRET_KEYS, f"{endpoint}:{key}"
        lowered = repr(body).lower()
        assert "claims live market data" not in lowered
        assert "validated real market data" not in lowered
        assert "trading decision" not in lowered
        assert "readiness-to-trade generated" not in lowered
        assert "execute trade" not in lowered


def test_strategy_research_workspace_endpoint_families_have_no_post_methods() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/strategy-research-workspace"):
            assert "POST" not in methods, path


def test_cross_endpoint_consistency_doc_lists_expected_endpoint_families() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for family in [
        "strategy-research-workspace",
        "strategy-research-workspace-api",
        "strategy-research-workspace-display",
        "strategy-research-workspace-boundary",
    ]:
        assert family in text
