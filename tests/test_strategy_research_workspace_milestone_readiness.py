from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_milestone_readiness_recommends_prompt_68() -> None:
    readiness = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_MILESTONE_READINESS.md").read_text(
        encoding="utf-8"
    )
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")

    assert "Prompt 68 - Strategy Research Workspace System Boundary Hardening" in readiness
    assert "Prompt 68 - Strategy Research Workspace System Boundary Hardening" in next_phase
    assert "active UI" in readiness
    assert "paper ingestion" in readiness
    assert "paper parsing" in readiness
    assert "strategy generation" in readiness
    assert "backtesting" in readiness
    assert "recommendation" in readiness
    assert "broker controls" in readiness
    assert "execution APIs" in readiness


def test_strategy_research_workspace_status_docs_reflect_prompt_67() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    readiness_plan = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )

    assert "Current Prompt: 67" in north_star
    assert "Completed Prompts: 68 after completion" in north_star
    assert "Strategy Research Workspace Planning Phase - Milestone Audit completed" in north_star
    assert "Prompt 66 - Strategy Research Workspace Safety Boundary Audit" in prompt_log
    assert "Prompt 68 - Strategy Research Workspace System Boundary Hardening" in readiness_plan


def test_verify_foundation_includes_prompt_63_to_67_artifacts() -> None:
    verify = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")

    for artifact in [
        "STRATEGY_RESEARCH_WORKSPACE_PLANNING.md",
        "STRATEGY_RESEARCH_WORKSPACE_API_CONTRACT_SKELETON.md",
        "STRATEGY_RESEARCH_WORKSPACE_DISPLAY_CONTRACT_SKELETON.md",
        "STRATEGY_RESEARCH_WORKSPACE_SAFETY_BOUNDARY_AUDIT.md",
        "STRATEGY_RESEARCH_WORKSPACE_MILESTONE_AUDIT.md",
        "test_strategy_research_workspace_next_phase_readiness.py",
    ]:
        assert artifact in verify


def test_audit_foundation_passes_for_strategy_research_workspace_milestone_readiness() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/audit_foundation.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
