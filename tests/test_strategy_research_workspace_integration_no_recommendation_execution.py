from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
STRATEGY_ROOT = ROOT / "packages/core/stark_terminal_core"
client = TestClient(app)


def test_no_recommendation_or_execution_functions_exist() -> None:
    forbidden = [
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def compute_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def create_order_button",
        "def execute_trade",
    ]
    for package in [
        "strategy_research_workspace",
        "strategy_research_workspace_api",
        "strategy_research_workspace_display",
        "strategy_research_workspace_boundary",
    ]:
        for path in (STRATEGY_ROOT / package).rglob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                if phrase in text:
                    assert f"def reject_strategy_research_{phrase.removeprefix('def ')}" in text


def test_no_execution_like_strategy_research_routes_exist() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/strategy-research-workspace"):
            lowered = path.lower()
            assert "execute" not in lowered
            assert "broker" not in lowered
            assert "order" not in lowered
            assert "approval" not in lowered
            assert "override" not in lowered
            assert "market-data-to-recommendation" not in lowered
            assert "readiness-to-trade" not in lowered
            assert "POST" not in methods


def test_no_recommendation_execution_doc_is_explicit() -> None:
    text = (
        ROOT
        / "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "No recommendations exist",
        "No action generation exists",
        "No confidence scoring exists",
        "No active DecisionObjects exist",
        "No readiness-to-trade exists",
        "No broker controls exist",
        "No approval or override POST routes exist",
        "No execution APIs exist",
    ]:
        assert phrase in text
