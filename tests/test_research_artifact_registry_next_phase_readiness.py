from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_research_artifact_registry_next_phase_plan_recommends_prompt_76() -> None:
    next_phase = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_NEXT_PHASE_PLAN.md").read_text(
        encoding="utf-8"
    )
    global_next = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")

    assert "Prompt 76 - Research Artifact Registry API/Display Integration Readiness Audit" in next_phase
    assert "Prompt 76 - Research Artifact Registry API/Display Integration Readiness Audit" in global_next
    for phrase in [
        "implementation remains forbidden",
        "active artifact ingestion/storage",
        "file upload/download",
        "paper parsing",
        "strategy generation",
        "backtesting",
        "recommendations",
        "execution APIs",
    ]:
        assert phrase in next_phase


def test_research_artifact_registry_status_docs_reflect_prompt_75() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    readiness_plan = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )

    assert "Current Prompt: 78" in north_star
    assert "Completed Prompts: 76 after completion" in north_star
    assert "Research Artifact Registry Planning Phase - System Boundary Hardening" in north_star
    assert "Prompt 74 - Research Artifact Registry Milestone Audit" in prompt_log
    assert "Prompt 76 - Research Artifact Registry API/Display Integration Readiness Audit" in readiness_plan


def test_foundation_scripts_include_prompt_75_artifacts() -> None:
    audit = (ROOT / "scripts/audit_foundation.py").read_text(encoding="utf-8")
    verify = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")
    for artifact in [
        "RESEARCH_ARTIFACT_REGISTRY_SYSTEM_BOUNDARY_HARDENING.md",
        "RESEARCH_ARTIFACT_FORBIDDEN_BEHAVIOR_REGISTRY.md",
        "RESEARCH_ARTIFACT_ENDPOINT_BOUNDARY_POLICY.md",
        "research_artifact_registry_boundary",
        "test_research_artifact_registry_boundary_invariants.py",
    ]:
        assert artifact in audit
        assert artifact in verify
