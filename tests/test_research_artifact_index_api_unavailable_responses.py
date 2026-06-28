from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index_api.unavailable import (
    ResearchArtifactIndexApiUnavailableResponse,
    unavailable_response_template,
)


def test_research_artifact_index_api_unavailable_response_defaults_are_safe() -> None:
    response = unavailable_response_template()

    assert response.unavailable is True
    assert response.allowed_stage == "api_contract_skeleton"
    assert response.reason
    for flag in [
        "indexing_engine_enabled",
        "search_engine_enabled",
        "ranking_engine_enabled",
        "retrieval_engine_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "active_ingestion_enabled",
        "persistent_storage_enabled",
        "file_uploads_enabled",
        "file_downloads_enabled",
        "file_previews_enabled",
        "paper_parsing_enabled",
        "strategy_generation_enabled",
        "backtesting_enabled",
        "recommendations_enabled",
        "execution_enabled",
    ]:
        assert getattr(response, flag) is False


def test_research_artifact_index_api_unavailable_response_requires_reason_and_stage() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexApiUnavailableResponse(reason="")
    with pytest.raises(ValidationError):
        ResearchArtifactIndexApiUnavailableResponse(reason="blocked", allowed_stage="active")


@pytest.mark.parametrize(
    "field_name",
    [
        "indexing_engine_enabled",
        "search_engine_enabled",
        "ranking_engine_enabled",
        "retrieval_engine_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "active_ingestion_enabled",
        "persistent_storage_enabled",
        "file_uploads_enabled",
        "file_downloads_enabled",
        "file_previews_enabled",
        "paper_parsing_enabled",
        "strategy_generation_enabled",
        "backtesting_enabled",
        "recommendations_enabled",
        "execution_enabled",
    ],
)
def test_research_artifact_index_api_unavailable_response_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexApiUnavailableResponse(reason="blocked", **{field_name: True})
