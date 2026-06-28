from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_packages_keep_declared_boundary_roles() -> None:
    package_readmes = {
        "planning": ROOT / "packages/core/stark_terminal_core/strategy_research_workspace/README.md",
        "api": ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api/README.md",
        "display": ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display/README.md",
        "boundary": ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_boundary/README.md",
    }
    for label, path in package_readmes.items():
        assert path.exists(), label
        text = path.read_text(encoding="utf-8").lower()
        assert "no active ui" in text
        assert "no execution" in text

    assert "planning" in package_readmes["planning"].read_text(encoding="utf-8").lower()
    assert "api contract skeleton" in package_readmes["api"].read_text(encoding="utf-8").lower()
    assert "display contract skeleton" in package_readmes["display"].read_text(encoding="utf-8").lower()
    assert "boundary" in package_readmes["boundary"].read_text(encoding="utf-8").lower()


def test_api_display_boundary_docs_forbid_active_paths() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_DISPLAY_BOUNDARY_AUDIT.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "No active display rendering",
        "No parsed-paper display path",
        "No generated-strategy display path",
        "No backtest-result display path",
        "No recommendation-to-display path",
        "No readiness-to-trade display path",
        "No market-data-to-research-decision endpoint",
        "No execution controls",
    ]:
        assert phrase in text


def test_no_market_data_to_research_decision_endpoint_exists() -> None:
    routes_root = ROOT / "apps/api/stark_terminal_api/routes"
    for path in routes_root.glob("strategy_research_workspace*.py"):
        text = path.read_text(encoding="utf-8").lower()
        assert "market-data-to-research-decision" not in text
        assert "market_data_to_research_decision" not in text
        assert "@router.post" not in text
