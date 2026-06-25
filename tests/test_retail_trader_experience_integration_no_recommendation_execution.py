from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def test_retail_trader_experience_modules_do_not_generate_recommendations_or_execution() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in [
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
            ROOT / "packages/core/stark_terminal_core/retail_trader_experience_boundary",
        ]
        for path in root.glob("*.py")
    )
    for forbidden in [
        "def generate_trader_recommendation",
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


def test_retail_trader_experience_routes_do_not_include_execution_or_broker_paths() -> None:
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
        if path.startswith("/retail-trader-experience"):
            lowered = path.lower()
            if path.startswith("/retail-trader-experience-boundary"):
                continue
            for term in forbidden_terms:
                assert term not in lowered, path


def test_integration_docs_explicitly_forbid_recommendation_and_execution() -> None:
    text = (
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md"
    ).read_text(encoding="utf-8")
    for phrase in [
        "No recommendation cards",
        "No buy/sell/hold/watch/avoid active outputs",
        "No action generation",
        "No confidence scoring",
        "No active DecisionObject display",
        "No readiness-to-trade",
        "No broker controls",
        "No execution APIs",
        "No API-to-display recommendation path",
    ]:
        assert phrase in text

