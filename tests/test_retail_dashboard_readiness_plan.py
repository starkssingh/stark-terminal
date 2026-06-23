from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_retail_dashboard_readiness_plan_recommends_prompt_51_history_and_prompt_52_next() -> None:
    plan = (ROOT / "docs/RETAIL_DASHBOARD_READINESS_PLAN.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")

    assert "Prompt 49 - Retail Dashboard Planning and Guardrails" in plan
    assert "Prompt 50 - Retail Dashboard API Contract Skeleton" in plan
    assert "Prompt 51 - Retail Dashboard Display Contract Skeleton" in plan
    assert "Prompt 52 - Retail Dashboard Safety Boundary Audit" in next_phase


def test_prompt_51_status_docs_reflect_dashboard_display_skeleton_only() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs/RETAIL_DASHBOARD_READINESS_PLAN.md").read_text(encoding="utf-8")

    assert "Current Prompt: 54" in north_star
    assert "Prompt 48 - Decision Desk API/Display Integration Readiness Audit" in prompt_log
    assert "Retail Dashboard Status: Planning/guardrails, API contract skeleton, and display contract skeleton implemented; no active UI, no recommendation cards, no broker controls, no execution" in north_star
    assert "Retail Dashboard Planning and Guardrails only" in plan


def test_retail_dashboard_readiness_plan_forbids_active_ui_and_trading_controls() -> None:
    plan = (ROOT / "docs/RETAIL_DASHBOARD_READINESS_PLAN.md").read_text(encoding="utf-8")

    for phrase in [
        "no active UI",
        "no recommendation cards",
        "no trading controls",
        "no broker linkage",
        "no readiness-to-trade display",
        "execution APIs remain forbidden",
    ]:
        assert phrase in plan
