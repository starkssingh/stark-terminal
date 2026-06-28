from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index_api.responses import (
    ResearchArtifactIndexApiResponsePlaceholder,
    ResearchArtifactIndexMetadataResponsePlaceholder,
    default_research_artifact_index_api_response_placeholder,
)


def test_research_artifact_index_api_response_placeholders_validate() -> None:
    response = default_research_artifact_index_api_response_placeholder()

    assert response.unavailable is True
    assert response.placeholder_only is True
    assert response.indexed_artifact_records_present is False
    assert response.search_results_present is False
    assert response.ranking_results_present is False
    assert response.retrieval_results_present is False
    assert response.embeddings_present is False
    assert response.vector_ids_present is False
    assert response.parsed_paper_content_present is False
    assert response.generated_strategy_present is False
    assert response.backtest_result_present is False
    assert response.recommendation_present is False
    assert response.decision_object_present is False
    assert response.readiness_to_trade_present is False
    assert response.execution_fields_present is False


@pytest.mark.parametrize(
    "field_name",
    [
        "indexed_artifact_records_present",
        "search_results_present",
        "ranking_results_present",
        "retrieval_results_present",
        "embeddings_present",
        "vector_ids_present",
        "parsed_paper_content_present",
        "generated_strategy_present",
        "backtest_result_present",
        "recommendation_present",
        "decision_object_present",
        "readiness_to_trade_present",
        "execution_fields_present",
    ],
)
def test_research_artifact_index_api_response_placeholders_reject_dangerous_content(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexMetadataResponsePlaceholder(response_id="response", **{field_name: True})


def test_research_artifact_index_api_response_models_have_no_result_payload_fields() -> None:
    fields = set(ResearchArtifactIndexApiResponsePlaceholder.model_fields)

    for field in [
        "indexed_artifact_records",
        "search_results",
        "rankings",
        "retrieval_results",
        "embeddings",
        "vector_ids",
        "parsed_paper_content",
        "generated_strategy",
        "backtest_result",
        "recommendation",
        "decision_object",
        "readiness_to_trade",
        "execution",
    ]:
        assert field not in fields
