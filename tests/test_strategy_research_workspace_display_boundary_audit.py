from __future__ import annotations

from pathlib import Path

from stark_terminal_api.routes.strategy_research_workspace_display import (
    router as strategy_research_workspace_display_router,
)


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_PACKAGE = ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display"
DISPLAY_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/strategy_research_workspace_display.py"


def test_strategy_research_workspace_display_package_remains_contract_skeleton_only() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DISPLAY_PACKAGE.glob("*.py"))
    docs = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_BOUNDARY_AUDIT.md").read_text(
        encoding="utf-8"
    )

    assert "display contract skeleton only" in docs
    assert "DecisionObject(" not in combined
    assert "@router.post" not in DISPLAY_ROUTE.read_text(encoding="utf-8")


def test_strategy_research_workspace_display_has_no_active_display_routes() -> None:
    paths = [
        route.path
        for route in strategy_research_workspace_display_router.routes
        if getattr(route, "path", "").startswith("/strategy-research-workspace-display")
    ]

    assert paths
    for path in paths:
        lowered = path.lower()
        for forbidden in [
            "active",
            "render",
            "widget",
            "parsed-paper",
            "generated-strategy",
            "backtest-result",
            "recommendation",
            "confidence",
            "decisionobject",
            "readiness-to-trade",
            "broker",
            "order",
            "execution",
        ]:
            assert forbidden not in lowered, (path, forbidden)


def test_strategy_research_workspace_display_boundary_doc_lists_allowed_and_forbidden_scope() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_BOUNDARY_AUDIT.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "display contract metadata",
        "workspace visual placeholders",
        "artifact visual placeholders",
        "paper visual placeholders",
        "hypothesis visual placeholders",
        "dataset visual placeholders",
        "experiment visual placeholders",
        "badge placeholders",
        "unavailable display responses",
        "cannot render active UI",
        "cannot add frontend components",
        "cannot add desktop components",
        "cannot show parsed paper results",
        "cannot show generated strategies",
        "cannot show backtest results",
        "cannot show recommendation cards",
        "cannot show broker controls",
        "cannot show execution controls",
    ]:
        assert phrase in text
