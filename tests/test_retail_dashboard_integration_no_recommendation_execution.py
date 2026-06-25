from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def test_retail_dashboard_modules_do_not_generate_recommendations_or_execution() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in [
            ROOT / "packages/core/stark_terminal_core/retail_dashboard",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_api",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_display",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_boundary",
        ]
        for path in root.glob("*.py")
    )
    for forbidden in [
        "def generate_dashboard_recommendation",
        "def generate_recommendation",
        "def generate_action_state",
        "def score_confidence",
        "def generate_decision_object",
        "DecisionObject(",
        "def execute_trade",
        "def place_order",
        "def create_order_button",
    ]:
        assert forbidden not in source


def test_retail_dashboard_routes_do_not_include_execution_or_broker_paths() -> None:
    forbidden_terms = (
        "execute",
        "execution",
        "broker",
        "order",
        "trade",
        "recommendation",
        "readiness-to-trade",
    )
    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-dashboard"):
            lowered = path.lower()
            for term in forbidden_terms:
                assert term not in lowered, path


def test_integration_docs_explicitly_forbid_recommendation_and_execution() -> None:
    text = (
        ROOT / "docs/RETAIL_DASHBOARD_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "no recommendation cards",
        "no buy/sell/hold/watch/avoid active outputs",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject display",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "no API-to-display recommendation path",
    ]:
        assert phrase in text
