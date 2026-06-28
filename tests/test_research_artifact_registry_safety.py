from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.safety import (
    ResearchArtifactRegistrySafetyPolicy,
    assert_no_artifact_ingestion_enabled,
    assert_no_backtesting_enabled,
    assert_no_execution_enabled,
    assert_no_paper_parsing_enabled,
    assert_no_recommendation_enabled,
    assert_no_strategy_generation_enabled,
    default_research_artifact_registry_safety_policy,
    forbidden_interactions,
    unavailable_response_template,
)


def test_default_safety_policy_forbids_dangerous_capabilities() -> None:
    policy = default_research_artifact_registry_safety_policy()

    assert policy.require_planning_only is True
    assert policy.allow_active_ingestion is False
    assert policy.allow_persistent_storage is False
    assert policy.allow_file_uploads is False
    assert policy.allow_file_downloads is False
    assert policy.allow_paper_parsing is False
    assert policy.allow_pdf_parsing is False
    assert policy.allow_arxiv_ingestion is False
    assert policy.allow_llm_analysis is False
    assert policy.allow_strategy_generation is False
    assert policy.allow_backtesting is False
    assert policy.allow_recommendations is False
    assert policy.allow_execution is False


def test_safety_policy_rejects_dangerous_allow_flags() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactRegistrySafetyPolicy(
            policy_id="unsafe-policy",
            name="Unsafe policy",
            allow_strategy_generation=True,
        )


def test_unavailable_template_blocks_all_dangerous_actions() -> None:
    response = unavailable_response_template()

    assert response.unavailable is True
    assert response.planning_only is True
    assert response.active_ingestion_enabled is False
    assert response.persistent_storage_enabled is False
    assert response.file_uploads_enabled is False
    assert response.file_downloads_enabled is False
    assert response.paper_parsing_enabled is False
    assert response.strategy_generation_enabled is False
    assert response.backtesting_enabled is False
    assert response.recommendations_enabled is False
    assert response.execution_enabled is False


def test_forbidden_interactions_helper_returns_locked_interactions() -> None:
    interactions = forbidden_interactions()

    assert interactions
    assert all(interaction.forbidden_now for interaction in interactions)


@pytest.mark.parametrize(
    "helper",
    [
        assert_no_artifact_ingestion_enabled,
        assert_no_paper_parsing_enabled,
        assert_no_strategy_generation_enabled,
        assert_no_backtesting_enabled,
        assert_no_recommendation_enabled,
        assert_no_execution_enabled,
    ],
)
def test_assert_helpers_block_when_enabled(helper) -> None:  # type: ignore[no-untyped-def]
    safe_result = helper(False)
    blocked_result = helper(True)

    assert safe_result.safe is True
    assert blocked_result.safe is False
    assert blocked_result.planning_only is True
    assert blocked_result.execution_enabled is False

