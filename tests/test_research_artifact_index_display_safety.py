from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index_display import safety
from stark_terminal_core.research_artifact_index_display.safety import (
    ResearchArtifactIndexDisplayForbiddenAction,
    ResearchArtifactIndexDisplaySafetyResult,
)


def test_research_artifact_index_display_forbidden_actions_are_complete() -> None:
    returned_actions = safety.research_artifact_index_display_forbidden_actions()
    actions = {action.value for action in returned_actions}

    expected = {
        "ACTIVE_UI",
        "FRONTEND_COMPONENT",
        "DESKTOP_COMPONENT",
        "INDEXING_ENGINE",
        "SEARCH_ENGINE",
        "RANKING_ENGINE",
        "RETRIEVAL_ENGINE",
        "EMBEDDING_PIPELINE",
        "VECTOR_STORE",
        "ACTIVE_INGESTION",
        "PERSISTENT_STORAGE",
        "FILE_UPLOAD",
        "FILE_DOWNLOAD",
        "FILE_PREVIEW",
        "PAPER_PARSING",
        "STRATEGY_GENERATION",
        "BACKTESTING",
        "RECOMMENDATION_GENERATION",
        "CONFIDENCE_SCORING",
        "DECISION_OBJECT_GENERATION",
        "READINESS_TO_TRADE",
        "BROKER_CONTROL",
        "EXECUTION",
    }
    assert expected <= actions
    assert all(isinstance(action, ResearchArtifactIndexDisplayForbiddenAction) for action in returned_actions)


@pytest.mark.parametrize(
    "helper_name",
    [
        "assert_no_index_display_active_ui_enabled",
        "assert_no_index_display_frontend_components_enabled",
        "assert_no_index_display_desktop_components_enabled",
        "assert_no_index_display_indexing_engine_enabled",
        "assert_no_index_display_search_engine_enabled",
        "assert_no_index_display_ranking_engine_enabled",
        "assert_no_index_display_retrieval_engine_enabled",
        "assert_no_index_display_embeddings_enabled",
        "assert_no_index_display_vector_store_enabled",
        "assert_no_index_display_ingestion_enabled",
        "assert_no_index_display_file_uploads_enabled",
        "assert_no_index_display_file_downloads_enabled",
        "assert_no_index_display_file_previews_enabled",
        "assert_no_index_display_paper_parsing_enabled",
        "assert_no_index_display_strategy_generation_enabled",
        "assert_no_index_display_backtesting_enabled",
        "assert_no_index_display_recommendation_enabled",
        "assert_no_index_display_execution_enabled",
    ],
)
def test_research_artifact_index_display_safety_helpers_block_when_enabled(helper_name: str) -> None:
    helper = getattr(safety, helper_name)

    safe_result = helper(False)
    blocked_result = helper(True)

    assert safe_result.safe is True
    assert blocked_result.safe is False
    assert blocked_result.display_contract_skeleton_only is True


def test_research_artifact_index_display_safety_result_rejects_dangerous_flags() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexDisplaySafetyResult(
            result_id="result",
            safe=True,
            reasons=["unsafe"],
            active_ui_enabled=True,
        )
