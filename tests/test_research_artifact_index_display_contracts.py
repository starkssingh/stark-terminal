from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index_display.contracts import (
    ResearchArtifactIndexDisplayContract,
    default_research_artifact_index_display_contract,
)


def test_research_artifact_index_display_contract_defaults_validate() -> None:
    contract = default_research_artifact_index_display_contract()

    assert contract.service == "stark-terminal-research-artifact-index-display"
    assert contract.stage == "display_contract_skeleton"
    assert contract.read_only is True
    assert contract.unavailable_by_default is True
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
        assert getattr(contract, flag) is False


@pytest.mark.parametrize("field_name", ["contract_id", "service", "stage", "schema_version"])
def test_research_artifact_index_display_contract_rejects_empty_text(field_name: str) -> None:
    data = {"contract_id": "contract", field_name: " "}
    with pytest.raises(ValidationError):
        ResearchArtifactIndexDisplayContract(**data)


@pytest.mark.parametrize("field_name", ["read_only", "unavailable_by_default"])
def test_research_artifact_index_display_contract_requires_safe_true_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexDisplayContract(contract_id="contract", **{field_name: False})


@pytest.mark.parametrize(
    "field_name",
    [
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
    ],
)
def test_research_artifact_index_display_contract_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexDisplayContract(contract_id="contract", **{field_name: True})
