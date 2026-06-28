from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_boundary.py"


def test_boundary_has_no_backtesting_optimization_or_performance_functions() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("*.py"))
    for phrase in [
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
        "def calculate_performance",
    ]:
        assert phrase not in text


def test_boundary_has_no_backtest_result_routes() -> None:
    route_text = ROUTE_PATH.read_text(encoding="utf-8").lower()
    for phrase in ["/backtest", "/optimize", "/performance", "@router.post"]:
        assert phrase not in route_text


def test_boundary_docs_state_no_backtesting_policy() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_BACKTESTING_POLICY.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no backtesting",
        "no optimization",
        "no parameter search",
        "no walk-forward analysis",
        "no performance claims",
        "future prompt and audit required",
    ]:
        assert phrase in text

