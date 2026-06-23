from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/retail_dashboard",
    ROOT / "packages/core/stark_terminal_core/retail_dashboard_api",
    ROOT / "packages/core/stark_terminal_core/retail_dashboard_display",
]


def _module_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for root in MODULE_ROOTS for path in root.glob("*.py"))


def test_retail_dashboard_modules_do_not_generate_recommendations_or_actions() -> None:
    text = _module_text()
    for phrase in [
        "def generate_dashboard_recommendation",
        "def generate_recommendation",
        "def generate_action",
        "def generate_action_state",
        "def score_confidence",
        "def compute_confidence",
        "def generate_decision_object",
        "DecisionObject(",
    ]:
        assert phrase not in text


def test_retail_dashboard_modules_do_not_emit_trade_calls() -> None:
    text = _module_text().lower()
    for phrase in [
        "buy_signal",
        "sell_signal",
        "hold_signal",
        "watch_signal",
        "avoid_signal",
        "trade_call",
        "investment_advice",
    ]:
        assert phrase not in text


def test_retail_dashboard_docs_and_api_explicitly_forbid_recommendations() -> None:
    docs_text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/RETAIL_DASHBOARD_NO_RECOMMENDATION_AUDIT.md",
            "docs/RETAIL_DASHBOARD_SAFETY_BOUNDARY_AUDIT.md",
            "docs/RETAIL_DASHBOARD_API_BOUNDARY_AUDIT.md",
            "docs/RETAIL_DASHBOARD_DISPLAY_BOUNDARY_AUDIT.md",
        ]
    )
    for phrase in [
        "no recommendation cards",
        "no buy/sell/hold/watch/avoid active outputs",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject",
        "no readiness-to-trade",
        "no hidden trade interpretation",
        "no dashboard-as-recommendation behavior",
    ]:
        assert phrase in docs_text
