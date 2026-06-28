from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry.py"


def _source_text() -> str:
    files = [*PACKAGE_ROOT.glob("*.py"), ROUTE_PATH]
    return "\n".join(path.read_text(encoding="utf-8") for path in files)


def test_no_strategy_backtest_recommendation_or_execution_functions_exist() -> None:
    text = _source_text()
    forbidden_names = [
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def create_order_button",
        "def execute_trade",
    ]

    for name in forbidden_names:
        assert name not in text


def test_no_execution_broker_order_or_approval_routes_exist() -> None:
    route_paths = [
        route.path
        for route in app.routes
        if getattr(route, "path", "").startswith("/research-artifact-registry")
    ]
    joined = " ".join(route_paths).lower()

    assert "execute" not in joined
    assert "broker" not in joined
    assert "order" not in joined
    assert "approval" not in joined
    assert "override" not in joined
    assert "recommendation" not in joined
    assert "backtest" not in joined
    assert "strategy" not in joined


def test_no_active_decision_or_confidence_fields_are_exposed() -> None:
    text = _source_text().lower()

    assert "confidence_score" not in text
    assert "decisionobject(" not in text
    assert "buy/sell/hold" not in text
    assert "watch/avoid" not in text

