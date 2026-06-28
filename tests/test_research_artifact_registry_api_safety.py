from __future__ import annotations

from stark_terminal_core.research_artifact_registry.types import ResearchArtifactForbiddenInteractionKind
from stark_terminal_core.research_artifact_registry_api.safety import (
    assert_no_api_backtesting_enabled,
    assert_no_api_execution_enabled,
    assert_no_api_file_downloads_enabled,
    assert_no_api_file_uploads_enabled,
    assert_no_api_ingestion_enabled,
    assert_no_api_paper_parsing_enabled,
    assert_no_api_recommendation_enabled,
    assert_no_api_strategy_generation_enabled,
    research_artifact_registry_api_forbidden_actions,
)


def test_api_forbidden_actions_cover_dangerous_behaviors() -> None:
    actions = set(research_artifact_registry_api_forbidden_actions())

    required = {
        ResearchArtifactForbiddenInteractionKind.ACTIVE_INGESTION,
        ResearchArtifactForbiddenInteractionKind.PERSISTENT_STORAGE,
        ResearchArtifactForbiddenInteractionKind.FILE_UPLOAD,
        ResearchArtifactForbiddenInteractionKind.FILE_DOWNLOAD,
        ResearchArtifactForbiddenInteractionKind.PAPER_PARSING,
        ResearchArtifactForbiddenInteractionKind.PDF_PARSING,
        ResearchArtifactForbiddenInteractionKind.ARXIV_INGESTION,
        ResearchArtifactForbiddenInteractionKind.LLM_ANALYSIS,
        ResearchArtifactForbiddenInteractionKind.STRATEGY_GENERATION,
        ResearchArtifactForbiddenInteractionKind.BACKTESTING,
        ResearchArtifactForbiddenInteractionKind.RECOMMENDATION_GENERATION,
        ResearchArtifactForbiddenInteractionKind.EXECUTION,
    }
    assert required.issubset(actions)


def test_api_safety_helpers_allow_only_disabled_state() -> None:
    helpers = [
        assert_no_api_ingestion_enabled,
        assert_no_api_file_uploads_enabled,
        assert_no_api_file_downloads_enabled,
        assert_no_api_paper_parsing_enabled,
        assert_no_api_strategy_generation_enabled,
        assert_no_api_backtesting_enabled,
        assert_no_api_recommendation_enabled,
        assert_no_api_execution_enabled,
    ]

    for helper in helpers:
        safe_result = helper(False)
        blocked_result = helper(True)
        assert safe_result.safe is True
        assert blocked_result.safe is False
        assert blocked_result.api_contract_skeleton_only is True
        assert blocked_result.active_ingestion_enabled is False
        assert blocked_result.persistent_storage_enabled is False
        assert blocked_result.file_uploads_enabled is False
        assert blocked_result.file_downloads_enabled is False
        assert blocked_result.paper_parsing_enabled is False
        assert blocked_result.strategy_generation_enabled is False
        assert blocked_result.backtesting_enabled is False
        assert blocked_result.recommendations_enabled is False
        assert blocked_result.execution_enabled is False
