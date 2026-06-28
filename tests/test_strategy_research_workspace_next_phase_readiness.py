from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_next_phase_plan_recommends_prompt_68() -> None:
    strategy_plan = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_NEXT_PHASE_PLAN.md").read_text(
        encoding="utf-8"
    )
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")

    assert "Prompt 69 - Strategy Research Workspace API/Display Integration Readiness Audit" in strategy_plan
    assert "Prompt 69 - Strategy Research Workspace API/Display Integration Readiness Audit" in next_phase
    assert "active strategy research workspace ui is still not allowed" in strategy_plan.lower()
    assert "execution APIs remain forbidden" in strategy_plan


def test_strategy_research_workspace_status_docs_reflect_prompt_67() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Current Prompt: 78" in north_star
    assert "Completed Prompts: 72 after completion" in north_star
    assert "Research Artifact Registry Planning Phase - API Contract Skeleton" in north_star
    assert "Prompt 68 - Strategy Research Workspace System Boundary Hardening" in prompt_log


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
