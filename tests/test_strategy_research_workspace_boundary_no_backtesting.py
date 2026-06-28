from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_boundary_has_no_backtesting_functions() -> None:
    code = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "packages/core/stark_terminal_core").rglob("*.py")
        if "strategy_research_workspace" in path.as_posix()
    )

    for name in [
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward_analysis",
    ]:
        assert name not in code


def test_strategy_research_workspace_boundary_docs_forbid_backtesting() -> None:
    docs = (ROOT / "docs/STRATEGY_RESEARCH_BOUNDARY_NO_BACKTESTING_POLICY.md").read_text(
        encoding="utf-8"
    )

    assert "does not add a backtesting engine" in docs
    assert "optimization" in docs
    assert "walk-forward analysis" in docs
    assert "no backtesting" in docs.lower()
