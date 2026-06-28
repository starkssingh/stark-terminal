from __future__ import annotations

from stark_terminal_core.research_artifact_index.types import ResearchArtifactIndexForbiddenInteractionKind
from stark_terminal_core.research_artifact_index_api.safety import (
    assert_no_index_api_backtesting_enabled,
    assert_no_index_api_embeddings_enabled,
    assert_no_index_api_execution_enabled,
    assert_no_index_api_file_downloads_enabled,
    assert_no_index_api_file_previews_enabled,
    assert_no_index_api_file_uploads_enabled,
    assert_no_index_api_indexing_engine_enabled,
    assert_no_index_api_ingestion_enabled,
    assert_no_index_api_paper_parsing_enabled,
    assert_no_index_api_ranking_engine_enabled,
    assert_no_index_api_recommendation_enabled,
    assert_no_index_api_retrieval_engine_enabled,
    assert_no_index_api_search_engine_enabled,
    assert_no_index_api_strategy_generation_enabled,
    assert_no_index_api_vector_store_enabled,
    research_artifact_index_api_forbidden_actions,
)


def test_research_artifact_index_api_forbidden_actions_cover_dangerous_behavior() -> None:
    actions = set(research_artifact_index_api_forbidden_actions())

    for action in [
        ResearchArtifactIndexForbiddenInteractionKind.INDEXING_ENGINE,
        ResearchArtifactIndexForbiddenInteractionKind.SEARCH_ENGINE,
        ResearchArtifactIndexForbiddenInteractionKind.RANKING_ENGINE,
        ResearchArtifactIndexForbiddenInteractionKind.RETRIEVAL_ENGINE,
        ResearchArtifactIndexForbiddenInteractionKind.EMBEDDING_PIPELINE,
        ResearchArtifactIndexForbiddenInteractionKind.VECTOR_STORE,
        ResearchArtifactIndexForbiddenInteractionKind.SEMANTIC_SEARCH,
        ResearchArtifactIndexForbiddenInteractionKind.KEYWORD_SEARCH,
        ResearchArtifactIndexForbiddenInteractionKind.ACTIVE_INGESTION,
        ResearchArtifactIndexForbiddenInteractionKind.PERSISTENT_STORAGE,
        ResearchArtifactIndexForbiddenInteractionKind.FILE_UPLOAD,
        ResearchArtifactIndexForbiddenInteractionKind.FILE_DOWNLOAD,
        ResearchArtifactIndexForbiddenInteractionKind.FILE_PREVIEW,
        ResearchArtifactIndexForbiddenInteractionKind.PAPER_PARSING,
        ResearchArtifactIndexForbiddenInteractionKind.ARXIV_INGESTION,
        ResearchArtifactIndexForbiddenInteractionKind.LLM_PAPER_ANALYSIS,
        ResearchArtifactIndexForbiddenInteractionKind.STRATEGY_GENERATION,
        ResearchArtifactIndexForbiddenInteractionKind.BACKTESTING,
        ResearchArtifactIndexForbiddenInteractionKind.RECOMMENDATION_GENERATION,
        ResearchArtifactIndexForbiddenInteractionKind.EXECUTION,
    ]:
        assert action in actions


def test_research_artifact_index_api_assert_helpers_block_dangerous_actions() -> None:
    helpers = [
        assert_no_index_api_indexing_engine_enabled,
        assert_no_index_api_search_engine_enabled,
        assert_no_index_api_ranking_engine_enabled,
        assert_no_index_api_retrieval_engine_enabled,
        assert_no_index_api_embeddings_enabled,
        assert_no_index_api_vector_store_enabled,
        assert_no_index_api_ingestion_enabled,
        assert_no_index_api_file_uploads_enabled,
        assert_no_index_api_file_downloads_enabled,
        assert_no_index_api_file_previews_enabled,
        assert_no_index_api_paper_parsing_enabled,
        assert_no_index_api_strategy_generation_enabled,
        assert_no_index_api_backtesting_enabled,
        assert_no_index_api_recommendation_enabled,
        assert_no_index_api_execution_enabled,
    ]

    safe_results = [helper(False) for helper in helpers]
    blocked_results = [helper(True) for helper in helpers]

    assert all(result.safe is True for result in safe_results)
    assert all(result.safe is False for result in blocked_results)
    assert all(result.execution_enabled is False for result in blocked_results)
