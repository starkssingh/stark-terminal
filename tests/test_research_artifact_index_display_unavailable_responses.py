from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index_display.unavailable import (
    ResearchArtifactIndexDisplayUnavailableResponse,
    unavailable_display_response_template,
)


def test_research_artifact_index_display_unavailable_response_defaults() -> None:
    response = unavailable_display_response_template()

    assert response.unavailable is True
    assert response.allowed_stage == "display_contract_skeleton"
    for flag in [
        "active_ui_enabled",
        "frontend_components_enabled",
        "desktop_components_enabled",
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


def test_research_artifact_index_display_unavailable_response_requires_reason() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexDisplayUnavailableResponse(reason=" ")


@pytest.mark.parametrize("field_name", ["unavailable", "allowed_stage"])
def test_research_artifact_index_display_unavailable_response_requires_safe_stage(field_name: str) -> None:
    value = False if field_name == "unavailable" else "active_ui"
    with pytest.raises(ValidationError):
        ResearchArtifactIndexDisplayUnavailableResponse(reason="Unavailable", **{field_name: value})
