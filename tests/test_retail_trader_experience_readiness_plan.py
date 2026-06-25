from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_retail_trader_experience_readiness_plan_recommends_prompt_59() -> None:
    readiness = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Prompt 59 completes Retail Trader Experience Safety Boundary Audit" in readiness
    assert "Prompt 59 - Retail Trader Experience Safety Boundary Audit" in readiness
    assert "Prompt 59 - Retail Trader Experience Safety Boundary Audit" in next_phase
    assert "Current Prompt: 60" in north_star
    assert "Prompt 58 - Retail Trader Experience Display Contract Skeleton" in prompt_log


def test_retail_trader_experience_readiness_plan_is_planning_only() -> None:
    text = (ROOT / "docs/RETAIL_TRADER_EXPERIENCE_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "safety helpers",
        "implementation is not allowed yet",
        "Active UI",
        "recommendation cards",
        "broker controls",
        "execution APIs",
        "no active UI",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
    ]:
        assert phrase in text
