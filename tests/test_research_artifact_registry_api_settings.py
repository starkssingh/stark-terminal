from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_research_artifact_registry_api_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.research_artifact_registry_api_enabled is True
    assert settings.research_artifact_registry_api_schema_version == "v1"
    assert settings.research_artifact_registry_api_stage == "api_contract_skeleton"
    assert settings.research_artifact_registry_api_allow_active_ingestion is False
    assert settings.research_artifact_registry_api_allow_persistent_storage is False
    assert settings.research_artifact_registry_api_allow_file_uploads is False
    assert settings.research_artifact_registry_api_allow_file_downloads is False
    assert settings.research_artifact_registry_api_allow_paper_parsing is False
    assert settings.research_artifact_registry_api_allow_pdf_parsing is False
    assert settings.research_artifact_registry_api_allow_arxiv_ingestion is False
    assert settings.research_artifact_registry_api_allow_llm_analysis is False
    assert settings.research_artifact_registry_api_allow_strategy_generation is False
    assert settings.research_artifact_registry_api_allow_backtesting is False
    assert settings.research_artifact_registry_api_allow_recommendations is False
    assert settings.research_artifact_registry_api_allow_execution is False


def test_research_artifact_registry_api_settings_snapshot_is_safe() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["prompt_number"] == "107"
    assert snapshot["research_artifact_registry_api_enabled"] is True
    assert snapshot["research_artifact_registry_api_schema_version"] == "v1"
    assert snapshot["research_artifact_registry_api_stage"] == "api_contract_skeleton"
    for key, value in snapshot.items():
        if key.startswith("research_artifact_registry_api_allow_"):
            assert value is False


@pytest.mark.parametrize(
    "field_name",
    [
        "research_artifact_registry_api_allow_active_ingestion",
        "research_artifact_registry_api_allow_persistent_storage",
        "research_artifact_registry_api_allow_file_uploads",
        "research_artifact_registry_api_allow_file_downloads",
        "research_artifact_registry_api_allow_paper_parsing",
        "research_artifact_registry_api_allow_pdf_parsing",
        "research_artifact_registry_api_allow_arxiv_ingestion",
        "research_artifact_registry_api_allow_llm_analysis",
        "research_artifact_registry_api_allow_strategy_generation",
        "research_artifact_registry_api_allow_backtesting",
        "research_artifact_registry_api_allow_recommendations",
        "research_artifact_registry_api_allow_execution",
    ],
)
def test_research_artifact_registry_api_rejects_dangerous_allow_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field_name: True})


def test_research_artifact_registry_api_stage_validation() -> None:
    assert (
        Settings(research_artifact_registry_api_stage="audit_only").research_artifact_registry_api_stage
        == "audit_only"
    )
    with pytest.raises(ValidationError):
        Settings(research_artifact_registry_api_stage="active_api")
