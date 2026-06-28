from __future__ import annotations

from stark_terminal_core.research_artifact_index.health import check_research_artifact_index_health
from stark_terminal_core.research_artifact_index.readiness import research_artifact_index_readiness


def test_research_artifact_index_readiness_returns_planning_only_next_phase() -> None:
    readiness = research_artifact_index_readiness()

    assert readiness.index_planning_ready is True
    assert readiness.ready_for_api_contract_skeleton is True
    assert readiness.indexing_engine_enabled is False
    assert readiness.search_engine_enabled is False
    assert readiness.ranking_engine_enabled is False
    assert readiness.retrieval_engine_enabled is False
    assert readiness.embeddings_enabled is False
    assert readiness.vector_store_enabled is False
    assert readiness.active_ingestion_enabled is False
    assert readiness.persistent_storage_enabled is False
    assert readiness.file_uploads_enabled is False
    assert readiness.file_downloads_enabled is False
    assert readiness.file_previews_enabled is False
    assert readiness.paper_parsing_enabled is False
    assert readiness.strategy_generation_enabled is False
    assert readiness.backtesting_enabled is False
    assert readiness.recommendations_enabled is False
    assert readiness.execution_enabled is False
    assert readiness.next_allowed_phase == "api_contract_skeleton"


def test_research_artifact_index_health_is_safe() -> None:
    health = check_research_artifact_index_health()

    assert health.status == "healthy"
    assert health.planning_only is True
    assert health.unavailable_by_default is True
    assert health.indexing_engine_enabled is False
    assert health.search_engine_enabled is False
    assert health.ranking_engine_enabled is False
    assert health.retrieval_engine_enabled is False
    assert health.embeddings_enabled is False
    assert health.vector_store_enabled is False
    assert health.execution_enabled is False

