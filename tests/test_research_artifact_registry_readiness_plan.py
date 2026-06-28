from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_research_artifact_registry_readiness_plan_recommends_prompt_70() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_READINESS_PLAN.md").read_text(
        encoding="utf-8"
    )
    assert "Prompt 70 - Research Artifact Registry Planning and Guardrails" in text
    assert "Research Artifact Registry Planning and Guardrails only" in text
    assert "Research Artifact Registry implementation is not yet allowed" in text
    assert "Active artifact ingestion/storage is not yet allowed" in text
    assert "Paper parsing is still not allowed" in text
    assert "execution remain forbidden" in text


def test_global_next_phase_docs_recommend_research_artifact_registry_planning() -> None:
    assert "Prompt 70 - Research Artifact Registry Planning and Guardrails" in (
        ROOT / "docs/NEXT_PHASE_PLAN.md"
    ).read_text(encoding="utf-8")
    assert "Prompt 70 - Research Artifact Registry Planning and Guardrails" in (
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_NEXT_PHASE_PLAN.md"
    ).read_text(encoding="utf-8")


def test_prompt_69_status_and_readiness_are_documented() -> None:
    assert "Current Prompt: 78" in (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    assert "Prompt 69 - Strategy Research Workspace API/Display Integration Readiness Audit" in (
        ROOT / "docs/PROMPT_LOG.md"
    ).read_text(encoding="utf-8")
    assert "Research Artifact Registry Planning and Guardrails only" in (
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_READINESS_PLAN.md"
    ).read_text(encoding="utf-8")
