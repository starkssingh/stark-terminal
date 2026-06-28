from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRATEGY_ROOT = ROOT / "packages/core/stark_terminal_core"


def test_no_strategy_generation_or_backtest_functions_exist() -> None:
    forbidden = [
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
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


def test_no_backtest_result_endpoint_exists() -> None:
    route_root = ROOT / "apps/api/stark_terminal_api/routes"
    for path in route_root.glob("strategy_research_workspace*.py"):
        text = path.read_text(encoding="utf-8").lower()
        assert "backtest-result" not in text
        assert "backtest_result" not in text
        assert "@router.post" not in text


def test_no_strategy_backtest_integration_doc_is_explicit() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_STRATEGY_BACKTEST_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "No strategy generation exists",
        "No strategy code generation exists",
        "No signal generation exists",
        "No factor generation exists",
        "No alpha generation exists",
        "No backtesting engine exists",
        "No optimization exists",
        "No parameter search exists",
        "No walk-forward analysis exists",
        "No performance claims exist",
        "No backtest result endpoint exists",
    ]:
        assert phrase in text
