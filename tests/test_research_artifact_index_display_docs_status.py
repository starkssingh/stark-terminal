from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_79_DOCS = [
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_CONTRACT_SKELETON.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_METADATA_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_CARD_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_TAG_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_PROVENANCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_LIFECYCLE_BADGES.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_ACTIVE_UI_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_INDEXING_ENGINE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_SEARCH_RANKING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_EMBEDDINGS_VECTOR_STORE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_INGESTION_STORAGE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_RECOMMENDATION_EXECUTION_POLICY.md",
]


def test_research_artifact_index_display_prompt_79_docs_exist() -> None:
    for relative in PROMPT_79_DOCS:
        assert (ROOT / relative).exists()


def test_research_artifact_index_display_docs_state_boundaries() -> None:
    combined = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in PROMPT_79_DOCS)

    for phrase in [
        "Prompt 79",
        "Research Artifact Index Display",
        "display contract skeleton",
        "backend-only",
        "read-only",
        "unavailable-by-default",
        "No active UI",
        "No frontend implementation",
        "No desktop implementation",
        "No file preview",
        "No indexing engine",
        "No search engine",
        "No ranking engine",
        "No retrieval engine",
        "No embeddings",
        "No vector store",
        "No active artifact ingestion/storage",
        "No file upload/download/preview",
        "No paper parsing",
        "No PDF",
        "No arXiv",
        "No LLM paper analysis",
        "No strategy generation",
        "No strategy code generation",
        "No backtesting",
        "No optimization",
        "No recommendations",
        "No confidence scoring",
        "No DecisionObject",
        "No readiness-to-trade",
        "No broker controls",
        "No execution",
        "Prompt 80",
        "Mac mini M2",
        "Windows-native",
        "decision candidate is not a trade",
        "execution APIs remain forbidden",
    ]:
        assert phrase in combined


def test_research_artifact_index_display_status_docs_updated() -> None:
    assert "Prompt 79" in (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    assert "Current Prompt: 79" in north_star
    assert "Research Artifact Index Planning Phase - Display Contract Skeleton" in north_star
    assert "Prompt 80 - Research Artifact Index Safety Boundary Audit" in (
        ROOT / "docs/NEXT_PHASE_PLAN.md"
    ).read_text(encoding="utf-8")
    assert "Research Artifact Index Display Contract Skeleton" in (ROOT / "PROJECT_MAP.md").read_text(
        encoding="utf-8"
    )
