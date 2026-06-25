from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_phase_has_no_recommendation_or_execution_routes() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        if not path.startswith("/strategy-research-workspace"):
            continue
        lowered = path.lower()
        for forbidden in [
            "recommendation",
            "action",
            "confidence",
            "decisionobject",
            "broker",
            "order",
            "execution",
            "execute",
            "approval",
            "override",
            "readiness-to-trade",
            "market-data-to-recommendation",
        ]:
            assert forbidden not in lowered, (path, forbidden)


def test_strategy_research_workspace_phase_no_recommendation_execution_doc_is_explicit() -> None:
    text = (
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md"
    ).read_text(encoding="utf-8")

    for phrase in [
        "No research-as-recommendation exists",
        "No buy/sell/hold/watch/avoid outputs exist",
        "No action generation exists",
        "No confidence scoring exists",
        "No active DecisionObjects exist",
        "No readiness-to-trade exists",
        "No broker controls exist",
        "No execution APIs exist",
    ]:
        assert phrase in text
