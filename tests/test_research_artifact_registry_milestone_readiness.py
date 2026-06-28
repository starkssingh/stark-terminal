from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_research_artifact_registry_milestone_readiness_recommends_prompt_75() -> None:
    readiness = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_MILESTONE_READINESS.md").read_text(
        encoding="utf-8"
    )
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")

    assert "Prompt 74 milestone audit completed" in readiness
    assert "Prompt 75 - Research Artifact Registry System Boundary Hardening" in readiness
    assert "Prompt 75 - Research Artifact Registry System Boundary Hardening" in next_phase
    for phrase in [
        "Implementation remains forbidden",
        "Active artifact ingestion/storage",
        "file upload/download",
        "paper parsing",
        "strategy generation",
        "backtesting",
        "execution APIs",
    ]:
        assert phrase in readiness


def test_research_artifact_registry_status_docs_reflect_prompt_73() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    readiness_plan = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )

    assert "Current Prompt: 78" in north_star
    assert "Completed Prompts: 74 after completion" in north_star
    assert "Research Artifact Registry Planning Phase - System Boundary Hardening" in north_star
    assert "Prompt 73 - Research Artifact Registry Safety Boundary Audit" in prompt_log
    assert "Prompt 75 - Research Artifact Registry System Boundary Hardening" in readiness_plan


def test_foundation_scripts_include_prompt_73_artifacts() -> None:
    audit = (ROOT / "scripts/audit_foundation.py").read_text(encoding="utf-8")
    verify = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")

    for artifact in [
        "RESEARCH_ARTIFACT_REGISTRY_SAFETY_BOUNDARY_AUDIT.md",
        "RESEARCH_ARTIFACT_REGISTRY_API_BOUNDARY_AUDIT.md",
        "RESEARCH_ARTIFACT_REGISTRY_DISPLAY_BOUNDARY_AUDIT.md",
        "RESEARCH_ARTIFACT_REGISTRY_MILESTONE_READINESS.md",
        "test_research_artifact_registry_milestone_readiness.py",
    ]:
        assert artifact in audit
        assert artifact in verify
