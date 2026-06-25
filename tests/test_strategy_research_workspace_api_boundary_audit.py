from __future__ import annotations

from pathlib import Path

from stark_terminal_api.routes.strategy_research_workspace_api import (
    router as strategy_research_workspace_api_router,
)


ROOT = Path(__file__).resolve().parents[1]
API_PACKAGE = ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api"
API_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/strategy_research_workspace_api.py"


def test_strategy_research_workspace_api_package_remains_contract_skeleton_only() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in API_PACKAGE.glob("*.py"))
    docs = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_BOUNDARY_AUDIT.md").read_text(
        encoding="utf-8"
    )

    assert "API contract skeleton only" in docs
    assert "DecisionObject(" not in combined
    assert "@router.post" not in API_ROUTE.read_text(encoding="utf-8")


def test_strategy_research_workspace_api_has_no_processing_or_execution_endpoints() -> None:
    paths = [
        route.path
        for route in strategy_research_workspace_api_router.routes
        if getattr(route, "path", "").startswith("/strategy-research-workspace-api")
    ]

    assert paths
    for path in paths:
        lowered = path.lower()
        for forbidden in [
            "paper-upload",
            "pdf",
            "arxiv",
            "market-data",
            "parse",
            "generate",
            "backtest",
            "recommendation",
            "decisionobject",
            "active-workspace",
            "broker",
            "order",
            "execute",
            "execution",
            "approve",
            "override",
        ]:
            assert forbidden not in lowered, (path, forbidden)


def test_strategy_research_workspace_api_boundary_doc_lists_allowed_and_forbidden_scope() -> None:
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_BOUNDARY_AUDIT.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "request placeholders",
        "response placeholders",
        "workspace reference placeholders",
        "artifact reference placeholders",
        "paper reference placeholders",
        "hypothesis reference placeholders",
        "dataset reference placeholders",
        "experiment reference placeholders",
        "safety reference placeholders",
        "unavailable responses",
        "read-only skeleton endpoints",
        "cannot ingest papers",
        "cannot parse papers",
        "cannot generate strategies",
        "cannot run backtests",
        "cannot generate recommendations",
        "cannot expose broker controls",
        "cannot expose execution APIs",
    ]:
        assert phrase in text
