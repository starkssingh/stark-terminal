from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def _module_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for root in [
            ROOT / "packages/core/stark_terminal_core/retail_dashboard",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_api",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_display",
        ]
        for path in root.glob("*.py")
    )


def test_retail_dashboard_modules_do_not_generate_recommendations_actions_confidence_or_decisionobjects() -> None:
    text = _module_text()
    for phrase in [
        "def generate_dashboard_recommendation",
        "def generate_recommendation",
        "def generate_action_state",
        "def score_confidence",
        "def compute_confidence",
        "def generate_decision_object",
        "DecisionObject(",
    ]:
        assert phrase not in text


def test_retail_dashboard_routes_have_no_execution_broker_order_or_readiness_to_trade_paths() -> None:
    for path, operations in app.openapi()["paths"].items():
        if path.startswith(("/retail-dashboard", "/retail-dashboard-api", "/retail-dashboard-display")):
            lowered = path.lower()
            assert "execution" not in lowered
            assert "execute" not in lowered
            assert "broker" not in lowered
            assert "order" not in lowered
            assert "market-data-to-recommendation" not in lowered
            assert "readiness-to-trade" not in lowered
            assert "post" not in operations
            assert "put" not in operations
            assert "patch" not in operations
            assert "delete" not in operations


def test_phase_no_recommendation_execution_doc_forbids_trade_interpretation() -> None:
    text = (ROOT / "docs/RETAIL_DASHBOARD_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "no recommendation cards",
        "no buy/sell/hold/watch/avoid active outputs",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject display",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "no hidden trade interpretation",
    ]:
        assert phrase in text
