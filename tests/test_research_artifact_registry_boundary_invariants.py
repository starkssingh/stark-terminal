from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_boundary.forbidden import (
    ResearchArtifactBoundarySafetyLabel,
)
from stark_terminal_core.research_artifact_registry_boundary.invariants import (
    ResearchArtifactBoundaryInvariantResult,
    evaluate_research_artifact_boundary_invariants,
    reject_research_artifact_active_ui_boundary_violation,
    reject_research_artifact_backtesting_boundary_violation,
    reject_research_artifact_broker_control_boundary_violation,
    reject_research_artifact_execution_boundary_violation,
    reject_research_artifact_ingestion_boundary_violation,
    reject_research_artifact_paper_parsing_boundary_violation,
    reject_research_artifact_readiness_to_trade_boundary_violation,
    reject_research_artifact_recommendation_boundary_violation,
    reject_research_artifact_storage_boundary_violation,
    reject_research_artifact_strategy_generation_boundary_violation,
    reject_research_artifact_upload_download_boundary_violation,
)


def test_research_artifact_boundary_default_invariants_pass() -> None:
    result = evaluate_research_artifact_boundary_invariants()

    assert result.passed is True
    assert result.blockers == []
    assert "research_artifact_registry_boundary" in result.checked_families
    assert result.safety_label == ResearchArtifactBoundarySafetyLabel.BOUNDARY_HARDENING_ONLY
    assert result.active_ingestion_allowed is False
    assert result.persistent_storage_allowed is False
    assert result.file_uploads_allowed is False
    assert result.file_downloads_allowed is False
    assert result.file_previews_allowed is False
    assert result.active_ui_allowed is False
    assert result.strategy_generation_allowed is False
    assert result.backtesting_allowed is False
    assert result.recommendations_allowed is False
    assert result.execution_allowed is False


@pytest.mark.parametrize(
    "flag",
    [
        "active_ingestion_allowed",
        "persistent_storage_allowed",
        "file_uploads_allowed",
        "file_downloads_allowed",
        "file_previews_allowed",
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "paper_parsing_allowed",
        "strategy_generation_allowed",
        "strategy_code_generation_allowed",
        "backtesting_allowed",
        "optimization_allowed",
        "recommendations_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
    ],
)
def test_research_artifact_boundary_invariant_result_rejects_dangerous_flags(flag: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactBoundaryInvariantResult(
            result_id="research-artifact-boundary-invariant-test-v1",
            passed=False,
            checked_families=["research_artifact_registry_boundary"],
            **{flag: True},
        )


def test_research_artifact_boundary_invariant_result_cannot_pass_with_blockers() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactBoundaryInvariantResult(
            result_id="research-artifact-boundary-invariant-test-v1",
            passed=True,
            checked_families=["research_artifact_registry_boundary"],
            blockers=["blocked"],
        )


def test_research_artifact_boundary_reject_helpers_return_blocked_safe_results() -> None:
    helpers = [
        reject_research_artifact_ingestion_boundary_violation,
        reject_research_artifact_storage_boundary_violation,
        reject_research_artifact_upload_download_boundary_violation,
        reject_research_artifact_active_ui_boundary_violation,
        reject_research_artifact_paper_parsing_boundary_violation,
        reject_research_artifact_strategy_generation_boundary_violation,
        reject_research_artifact_backtesting_boundary_violation,
        reject_research_artifact_recommendation_boundary_violation,
        reject_research_artifact_execution_boundary_violation,
        reject_research_artifact_broker_control_boundary_violation,
        reject_research_artifact_readiness_to_trade_boundary_violation,
    ]

    for helper in helpers:
        result = helper()
        assert result.passed is False
        assert result.blockers
        assert result.safety_label == ResearchArtifactBoundarySafetyLabel.BLOCKED
        assert result.execution_allowed is False

