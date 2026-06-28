from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py"


def _source_text() -> str:
    paths = list(PACKAGE_ROOT.glob("*.py")) + [ROUTE_PATH]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_display_package_has_no_strategy_backtest_recommendation_or_execution_functions() -> None:
    text = _source_text()
    forbidden = [
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def create_order_button",
        "def execute_trade",
    ]

    for phrase in forbidden:
        assert phrase not in text


def test_display_route_has_no_execution_broker_strategy_backtest_or_recommendation_paths() -> None:
    text = ROUTE_PATH.read_text(encoding="utf-8").lower()
    forbidden_route_terms = [
        "/execute",
        "/trade",
        "/order",
        "/broker",
        "/approval",
        "/override",
        "/recommendation",
        "/backtest",
        "/strategy",
        "/readiness-to-trade",
    ]

    for term in forbidden_route_terms:
        assert term not in text
    assert "@router.post" not in text


def test_display_package_has_no_active_trade_call_terms() -> None:
    text = _source_text()
    forbidden_terms = [
        "DecisionObject(",
        "confidence_score",
        "readiness_to_trade=True",
        "buy/sell/hold",
        "watch/avoid",
    ]

    for term in forbidden_terms:
        assert term not in text
