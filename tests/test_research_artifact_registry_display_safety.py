from __future__ import annotations

import pytest

from stark_terminal_core.research_artifact_registry_display.safety import (
    ResearchArtifactRegistryDisplayForbiddenAction,
    assert_no_display_active_ui_enabled,
    assert_no_display_backtesting_enabled,
    assert_no_display_desktop_components_enabled,
    assert_no_display_execution_enabled,
    assert_no_display_file_downloads_enabled,
    assert_no_display_file_uploads_enabled,
    assert_no_display_frontend_components_enabled,
    assert_no_display_ingestion_enabled,
    assert_no_display_paper_parsing_enabled,
    assert_no_display_recommendation_enabled,
    assert_no_display_strategy_generation_enabled,
    research_artifact_registry_display_forbidden_actions,
)


def test_display_forbidden_actions_cover_dangerous_behaviors() -> None:
    actions = set(research_artifact_registry_display_forbidden_actions())

    for expected in [
        ResearchArtifactRegistryDisplayForbiddenAction.ACTIVE_UI,
        ResearchArtifactRegistryDisplayForbiddenAction.FRONTEND_COMPONENT,
        ResearchArtifactRegistryDisplayForbiddenAction.DESKTOP_COMPONENT,
        ResearchArtifactRegistryDisplayForbiddenAction.ACTIVE_INGESTION,
        ResearchArtifactRegistryDisplayForbiddenAction.PERSISTENT_STORAGE,
        ResearchArtifactRegistryDisplayForbiddenAction.FILE_PREVIEW,
        ResearchArtifactRegistryDisplayForbiddenAction.FILE_UPLOAD,
        ResearchArtifactRegistryDisplayForbiddenAction.FILE_DOWNLOAD,
        ResearchArtifactRegistryDisplayForbiddenAction.PAPER_PARSING,
        ResearchArtifactRegistryDisplayForbiddenAction.STRATEGY_GENERATION,
        ResearchArtifactRegistryDisplayForbiddenAction.BACKTESTING,
        ResearchArtifactRegistryDisplayForbiddenAction.RECOMMENDATION_GENERATION,
        ResearchArtifactRegistryDisplayForbiddenAction.BROKER_CONTROL,
        ResearchArtifactRegistryDisplayForbiddenAction.EXECUTION,
    ]:
        assert expected in actions


@pytest.mark.parametrize(
    "helper",
    [
        assert_no_display_active_ui_enabled,
        assert_no_display_frontend_components_enabled,
        assert_no_display_desktop_components_enabled,
        assert_no_display_ingestion_enabled,
        assert_no_display_file_uploads_enabled,
        assert_no_display_file_downloads_enabled,
        assert_no_display_paper_parsing_enabled,
        assert_no_display_strategy_generation_enabled,
        assert_no_display_backtesting_enabled,
        assert_no_display_recommendation_enabled,
        assert_no_display_execution_enabled,
    ],
)
def test_display_safety_helpers_block_when_enabled(helper) -> None:
    safe = helper(False)
    blocked = helper(True)

    assert safe.safe is True
    assert blocked.safe is False
    assert safe.display_contract_skeleton_only is True
    assert blocked.display_contract_skeleton_only is True
