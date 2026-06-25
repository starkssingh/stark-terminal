from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_next_phase_plan_recommends_prompt_68() -> None:
    strategy_plan = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_NEXT_PHASE_PLAN.md").read_text(
        encoding="utf-8"
    )
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")

    assert "Prompt 68 - Strategy Research Workspace System Boundary Hardening" in strategy_plan
    assert "Prompt 68 - Strategy Research Workspace System Boundary Hardening" in next_phase
    assert "active strategy research workspace ui is still not allowed" in strategy_plan.lower()
    assert "execution APIs remain forbidden" in strategy_plan


def test_strategy_research_workspace_status_docs_reflect_prompt_67() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Current Prompt: 67" in north_star
    assert "Completed Prompts: 68 after completion" in north_star
    assert "Strategy Research Workspace Planning Phase - Milestone Audit completed" in north_star
    assert "Prompt 67 - Strategy Research Workspace Milestone Audit" in prompt_log


def test_strategy_research_workspace_verifier_and_audit_include_prompt_67() -> None:
    verify = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")
    audit = (ROOT / "scripts/audit_foundation.py").read_text(encoding="utf-8")

    for artifact in [
        "STRATEGY_RESEARCH_WORKSPACE_MILESTONE_AUDIT.md",
        "STRATEGY_RESEARCH_WORKSPACE_NEXT_PHASE_PLAN.md",
        "test_strategy_research_workspace_next_phase_readiness.py",
    ]:
        assert artifact in verify
        assert artifact in audit
