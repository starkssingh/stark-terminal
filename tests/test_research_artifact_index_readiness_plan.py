from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/RESEARCH_ARTIFACT_INDEX_READINESS_PLAN.md"


def test_research_artifact_index_readiness_plan_exists() -> None:
    assert DOC.exists()


def test_research_artifact_index_readiness_plan_recommends_prompt_77() -> None:
    text = DOC.read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Prompt 77 - Research Artifact Index Planning and Guardrails" in text
    assert "Prompt 77 - Research Artifact Index Planning and Guardrails" in next_phase
    assert "Current Prompt: 78" in north_star
    assert "Prompt 76 - Research Artifact Registry API/Display Integration Readiness Audit" in prompt_log


def test_research_artifact_index_readiness_plan_is_planning_only() -> None:
    text = DOC.read_text(encoding="utf-8").lower()
    for phrase in [
        "planning and guardrails only",
        "research artifact index implementation is not yet allowed",
        "indexing, search",
        "ranking",
        "storage",
        "ingestion",
        "embedding",
        "vector store",
        "parsing",
        "retrieval",
        "no indexing engine",
        "no search engine",
        "no ranking engine",
        "no embedding/vector store",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendation generation",
        "no execution",
        "decision candidate is not a trade",
    ]:
        assert phrase in text

