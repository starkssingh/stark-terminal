from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_phase_has_no_backtest_result_routes() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        if not path.startswith("/strategy-research-workspace"):
            continue
        lowered = path.lower()
        for forbidden in ["backtest", "walk-forward", "optimization", "parameter-search", "performance"]:
            assert forbidden not in lowered, (path, forbidden)


def test_strategy_research_workspace_phase_no_backtesting_doc_is_explicit() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_BACKTESTING_AUDIT.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "No backtesting engine exists",
        "No optimization exists",
        "No parameter search exists",
        "No walk-forward analysis exists",
        "No performance claims exist",
        "No backtest result endpoints exist",
    ]:
        assert phrase in text
