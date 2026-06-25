from __future__ import annotations

from pathlib import Path

from stark_terminal_api.routes.strategy_research_workspace_display import (
    router as strategy_research_workspace_display_router,
)


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_PACKAGE = ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display"


def test_strategy_research_workspace_display_milestone_remains_contract_skeleton_only() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DISPLAY_PACKAGE.glob("*.py"))

    assert "DecisionObject(" not in combined
    assert "render_active_workspace" not in combined
    assert "@router.post" not in combined


def test_strategy_research_workspace_display_milestone_has_no_active_display_routes() -> None:
    for route in strategy_research_workspace_display_router.routes:
        path = getattr(route, "path", "")
        lowered = path.lower()
        for forbidden in [
            "render",
            "parsed-paper",
            "generated-strategy",
            "backtest-result",
            "recommendation",
            "confidence",
            "decisionobject",
            "readiness-to-trade",
            "broker",
            "execution",
        ]:
            assert forbidden not in lowered, (path, forbidden)


def test_strategy_research_workspace_display_docs_confirm_no_active_ui() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_MILESTONE_AUDIT.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "no active UI",
        "no frontend implementation",
        "no desktop implementation",
        "no parsed-paper display",
        "no generated-strategy display",
        "no backtest-result display",
        "no recommendation display",
        "no broker-control display",
        "no execution display",
    ]:
        assert phrase in text
