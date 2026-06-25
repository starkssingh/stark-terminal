from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display",
]
ROUTES = list((ROOT / "apps/api/stark_terminal_api/routes").glob("strategy_research_workspace*.py"))


def _combined_code() -> str:
    return "\n".join(
        [path.read_text(encoding="utf-8") for package in PACKAGES for path in package.glob("*.py")]
        + [route.read_text(encoding="utf-8") for route in ROUTES]
    )


def test_strategy_research_workspace_has_no_backtesting_functions() -> None:
    combined = _combined_code()

    for forbidden in [
        "def run_backtest",
        "def backtest_strategy",
        "def walk_forward",
        "def optimize_strategy",
        "def parameter_search",
        "def calculate_performance",
        "def validate_strategy",
    ]:
        assert forbidden not in combined


def test_strategy_research_workspace_has_no_backtest_result_endpoints() -> None:
    combined = "\n".join(route.read_text(encoding="utf-8") for route in ROUTES)

    for forbidden_path in [
        "run-backtest",
        "backtest-result",
        "walk-forward",
        "optimize",
        "parameter-search",
        "performance",
        "strategy-validation",
    ]:
        assert forbidden_path not in combined


def test_strategy_research_workspace_no_backtesting_docs_forbid_backtesting() -> None:
    docs = [
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_NO_BACKTESTING_AUDIT.md",
        ROOT / "docs/STRATEGY_RESEARCH_NO_BACKTESTING_POLICY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_BACKTESTING_POLICY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_BACKTESTING_POLICY.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs).lower()

    for phrase in [
        "no backtesting engine",
        "no walk-forward analysis",
        "no optimization",
        "no parameter search",
        "no performance claims",
        "no strategy validation",
        "no backtest result endpoints",
    ]:
        assert phrase in combined
