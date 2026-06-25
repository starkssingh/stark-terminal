from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_readiness_plan_points_to_prompt_63() -> None:
    readiness = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )
    next_plan = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Prompt 63 - Strategy Research Workspace Planning and Guardrails" in readiness
    assert "Prompt 63 - Strategy Research Workspace Planning and Guardrails" in next_plan
    assert "Current Prompt: 63" in north_star
    assert "Prompt 62 - Retail Trader Experience API/Display Integration Readiness Audit" in prompt_log


def test_strategy_research_workspace_plan_remains_planning_only() -> None:
    readiness = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "Planning and Guardrails only",
        "not ready to implement Strategy Research Workspace UI",
        "Active UI is not allowed yet",
        "Recommendation generation is not allowed yet",
        "Broker controls are not allowed yet",
        "execution APIs remain forbidden",
        "no live trading controls",
        "no recommendation generation",
        "no broker linkage",
    ]:
        assert phrase in readiness

