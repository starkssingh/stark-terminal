from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_78_DOCS = [
    "docs/RESEARCH_ARTIFACT_INDEX_API_CONTRACT_SKELETON.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_UNAVAILABLE_RESPONSES.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_SAFETY_BOUNDARY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_INDEXING_ENGINE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_SEARCH_RANKING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_EMBEDDINGS_VECTOR_STORE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_INGESTION_STORAGE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_RECOMMENDATION_EXECUTION_POLICY.md",
]


def test_prompt_78_docs_exist_and_state_api_boundaries() -> None:
    text = ""
    for doc in PROMPT_78_DOCS:
        path = ROOT / doc
        assert path.exists(), doc
        text += "\n" + path.read_text(encoding="utf-8")

    for phrase in [
        "Research Artifact Index API",
        "API contract skeleton",
        "read-only",
        "unavailable-by-default",
        "No indexing engine",
        "No search engine",
        "No ranking engine",
        "No retrieval engine",
        "No embeddings",
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


def test_prompt_78_status_docs_are_updated() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")

    assert "Current Prompt: 78" in north_star
    assert "Completed Prompts: 79 after completion" in north_star
    assert "Research Artifact Index Status: planning/guardrails and API contract skeleton only" in north_star
    assert "research_artifact_index_api" in project_map
    assert "Prompt 79 - Research Artifact Index Display Contract Skeleton" in next_phase
    assert "Prompt 78 - Research Artifact Index API Contract Skeleton" in prompt_log
