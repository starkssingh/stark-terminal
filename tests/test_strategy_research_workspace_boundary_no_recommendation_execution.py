from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_boundary_has_no_recommendation_or_execution_functions() -> None:
    code = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "packages/core/stark_terminal_core").rglob("*.py")
        if "strategy_research_workspace" in path.as_posix()
    )

    for name in [
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def create_order_button",
        "def execute_trade",
    ]:
        assert name not in code


def test_strategy_research_workspace_boundary_has_no_execution_like_routes() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/strategy-research-workspace"):
            lowered = path.lower()
            assert "execute" not in lowered
            assert "execution" not in lowered
            assert "broker" not in lowered
            assert "order" not in lowered
            assert "approval" not in lowered
            assert "override" not in lowered
            assert "recommendation" not in lowered


def test_strategy_research_workspace_boundary_docs_forbid_recommendation_and_execution() -> None:
    docs = (ROOT / "docs/STRATEGY_RESEARCH_BOUNDARY_NO_EXECUTION_POLICY.md").read_text(
        encoding="utf-8"
    )

    assert "does not add recommendation generation" in docs
    assert "confidence scoring" in docs
    assert "DecisionObject generation" in docs
    assert "broker controls" in docs
    assert "execution APIs" in docs
