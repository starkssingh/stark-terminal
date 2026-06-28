from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


BOUNDARY_ALLOW_FLAGS = [
    "research_artifact_registry_boundary_allow_active_ingestion",
    "research_artifact_registry_boundary_allow_persistent_storage",
    "research_artifact_registry_boundary_allow_file_uploads",
    "research_artifact_registry_boundary_allow_file_downloads",
    "research_artifact_registry_boundary_allow_file_previews",
    "research_artifact_registry_boundary_allow_active_ui",
    "research_artifact_registry_boundary_allow_frontend_components",
    "research_artifact_registry_boundary_allow_desktop_components",
    "research_artifact_registry_boundary_allow_paper_parsing",
    "research_artifact_registry_boundary_allow_pdf_parsing",
    "research_artifact_registry_boundary_allow_arxiv_ingestion",
    "research_artifact_registry_boundary_allow_llm_analysis",
    "research_artifact_registry_boundary_allow_strategy_generation",
    "research_artifact_registry_boundary_allow_strategy_code_generation",
    "research_artifact_registry_boundary_allow_backtesting",
    "research_artifact_registry_boundary_allow_optimization",
    "research_artifact_registry_boundary_allow_recommendations",
    "research_artifact_registry_boundary_allow_action_generation",
    "research_artifact_registry_boundary_allow_confidence_scoring",
    "research_artifact_registry_boundary_allow_decision_object_generation",
    "research_artifact_registry_boundary_allow_readiness_to_trade",
    "research_artifact_registry_boundary_allow_broker_controls",
    "research_artifact_registry_boundary_allow_execution",
    "research_artifact_registry_boundary_allow_approval",
    "research_artifact_registry_boundary_allow_override",
]


def test_research_artifact_registry_boundary_settings_safe_defaults() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.research_artifact_registry_boundary_enabled is True
    assert settings.research_artifact_registry_boundary_schema_version == "v1"
    assert settings.research_artifact_registry_boundary_stage == "boundary_hardening"
    for flag in BOUNDARY_ALLOW_FLAGS:
        assert getattr(settings, flag) is False


@pytest.mark.parametrize("flag", BOUNDARY_ALLOW_FLAGS)
def test_research_artifact_registry_boundary_settings_reject_dangerous_flags(flag: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{flag: True})


def test_research_artifact_registry_boundary_settings_validate_schema_and_stage() -> None:
    with pytest.raises(ValidationError):
        Settings(research_artifact_registry_boundary_schema_version="")
    with pytest.raises(ValidationError):
        Settings(research_artifact_registry_boundary_stage="implementation")


def test_research_artifact_registry_boundary_safe_snapshot_exposes_safe_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["prompt_number"] == "107"
    assert snapshot["research_artifact_registry_boundary_enabled"] is True
    assert snapshot["research_artifact_registry_boundary_schema_version"] == "v1"
    assert snapshot["research_artifact_registry_boundary_stage"] == "boundary_hardening"
    for flag in BOUNDARY_ALLOW_FLAGS:
        assert snapshot[flag] is False
