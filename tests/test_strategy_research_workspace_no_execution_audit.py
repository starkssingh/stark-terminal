from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
ROUTES = list((ROOT / "apps/api/stark_terminal_api/routes").glob("strategy_research_workspace*.py"))


def test_strategy_research_workspace_has_no_execution_like_routes() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/strategy-research-workspace"):
            lowered = path.lower()
            for forbidden in [
                "execute",
                "execution",
                "broker",
                "order",
                "approve",
                "approval",
                "override",
                "market-data-to-recommendation",
                "readiness-to-trade",
            ]:
                assert forbidden not in lowered, (path, forbidden)
            assert getattr(route, "methods", set()) <= {"GET", "HEAD", "OPTIONS"}


def test_strategy_research_workspace_routes_expose_no_post_approval_or_override_surfaces() -> None:
    combined = "\n".join(route.read_text(encoding="utf-8") for route in ROUTES)

    for forbidden in [
        "@router.post",
        "approval_granted=True",
        "override_granted=True",
        "broker_control_enabled=True",
        "execution_allowed=True",
        "execute_trade",
        "create_order_button",
    ]:
        assert forbidden not in combined


def test_strategy_research_workspace_no_execution_docs_forbid_execution() -> None:
    docs = [
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_NO_EXECUTION_AUDIT.md",
        ROOT / "docs/STRATEGY_RESEARCH_NO_EXECUTION_POLICY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_EXECUTION_POLICY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_EXECUTION_POLICY.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs).lower()

    for phrase in [
        "no execution APIs",
        "no broker controls",
        "no order buttons",
        "no paper trading controls",
        "no live trading controls",
        "no real-money routing",
        "no research-to-execution path",
        "no approval workflow",
        "no override workflow",
    ]:
        assert phrase.lower() in combined
