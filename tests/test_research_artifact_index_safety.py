from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.safety import (
    ResearchArtifactIndexSafetyPolicy,
    default_research_artifact_index_safety_policy,
    evaluate_research_artifact_index_safety,
    reject_embeddings_vector_store,
    reject_index_backtesting,
    reject_index_ingestion_storage,
    reject_index_paper_parsing,
    reject_index_recommendation_execution,
    reject_index_strategy_generation,
    reject_indexing_engine,
    reject_ranking_engine,
    reject_search_engine,
    unavailable_response_template,
)


def test_research_artifact_index_safety_policy_and_evaluation_are_fail_closed() -> None:
    policy = default_research_artifact_index_safety_policy()
    result = evaluate_research_artifact_index_safety(policy)

    assert policy.require_planning_only is True
    assert result.safe is True
    assert result.planning_only is True
    assert result.indexing_engine_enabled is False
    assert result.search_engine_enabled is False
    assert result.ranking_engine_enabled is False
    assert result.embeddings_enabled is False
    assert result.vector_store_enabled is False
    assert result.execution_enabled is False


@pytest.mark.parametrize("field", ["allow_indexing_engine", "allow_search_engine", "allow_ranking_engine", "allow_embeddings", "allow_vector_store", "allow_execution"])
def test_research_artifact_index_safety_policy_rejects_dangerous_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexSafetyPolicy(policy_id="x", name="x", **{field: True})


def test_research_artifact_index_reject_helpers_block_dangerous_behavior() -> None:
    results = [
        reject_indexing_engine(),
        reject_search_engine(),
        reject_ranking_engine(),
        reject_embeddings_vector_store(),
        reject_index_ingestion_storage(),
        reject_index_paper_parsing(),
        reject_index_strategy_generation(),
        reject_index_backtesting(),
        reject_index_recommendation_execution(),
    ]

    assert all(result.safe is False for result in results)
    assert all(result.execution_enabled is False for result in results)


def test_research_artifact_index_unavailable_response_template_is_safe() -> None:
    response = unavailable_response_template()

    assert response.unavailable is True
    assert response.planning_only is True
    assert response.indexing_engine_enabled is False
    assert response.search_engine_enabled is False
    assert response.ranking_engine_enabled is False
    assert response.embeddings_enabled is False
    assert response.vector_store_enabled is False
    assert response.execution_enabled is False

