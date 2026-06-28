from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_77_DOCS = [
    "docs/RESEARCH_ARTIFACT_INDEX_PLANNING.md",
    "docs/RESEARCH_ARTIFACT_INDEX_GUARDRAILS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_METADATA_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_KEY_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_TAG_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_PROVENANCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_LIFECYCLE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_FORBIDDEN_INTERACTIONS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_INDEXING_ENGINE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_SEARCH_RANKING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_EMBEDDINGS_VECTOR_STORE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_INGESTION_STORAGE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_RECOMMENDATION_EXECUTION_POLICY.md",
]


def test_prompt_77_docs_exist_and_state_boundaries() -> None:
    text = ""
    for doc in PROMPT_77_DOCS:
        path = ROOT / doc
        assert path.exists(), doc
        text += "\n" + path.read_text(encoding="utf-8")

    for phrase in [
        "Research Artifact Index",
        "planning",
        "guardrails",
        "No indexing engine",
        "No search engine",
        "No ranking engine",
        "No retrieval engine",
        "No embedding",
        "No vector store",
        "No active artifact ingestion",
        "No file upload/download/preview",
        "No paper parsing",
        "No strategy generation",
        "No backtesting",
        "No recommendations",
        "No broker controls",
        "No execution",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_77_status_docs_are_updated() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Current Prompt: 78" in north_star
    assert "Completed Prompts: 79 after completion" in north_star
    assert "Research Artifact Index Status: planning and guardrails only" in north_star
    assert "research_artifact_index" in project_map
    assert "Prompt 78 - Research Artifact Index API Contract Skeleton" in next_phase
    assert "Prompt 77 - Research Artifact Index Planning and Guardrails" in prompt_log

