from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_boundary.forbidden import (
    REQUIRED_RESEARCH_ARTIFACT_FORBIDDEN_BEHAVIORS,
    ResearchArtifactBoundarySeverity,
    ResearchArtifactForbiddenBehavior,
    ResearchArtifactForbiddenBehaviorKind,
    ResearchArtifactForbiddenBehaviorRegistry,
    default_research_artifact_forbidden_behavior_registry,
    default_research_artifact_forbidden_behaviors,
)


def test_research_artifact_forbidden_registry_validates_and_covers_required_behaviors() -> None:
    registry = default_research_artifact_forbidden_behavior_registry()

    assert registry.complete is True
    assert {behavior.kind for behavior in registry.behaviors}.issuperset(
        REQUIRED_RESEARCH_ARTIFACT_FORBIDDEN_BEHAVIORS
    )
    assert registry.active_ingestion_allowed is False
    assert registry.persistent_storage_allowed is False
    assert registry.file_uploads_allowed is False
    assert registry.file_downloads_allowed is False
    assert registry.file_previews_allowed is False
    assert registry.active_ui_allowed is False
    assert registry.paper_parsing_allowed is False
    assert registry.strategy_generation_allowed is False
    assert registry.backtesting_allowed is False
    assert registry.recommendations_allowed is False
    assert registry.confidence_scoring_allowed is False
    assert registry.decision_object_generation_allowed is False
    assert registry.readiness_to_trade_allowed is False
    assert registry.broker_controls_allowed is False
    assert registry.execution_allowed is False


@pytest.mark.parametrize("flag", ["forbidden_now", "requires_future_prompt", "requires_audit_before_unlock"])
def test_research_artifact_forbidden_behavior_enforces_locked_flags(flag: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactForbiddenBehavior(
            behavior_id="research-artifact-test-forbidden-v1",
            kind=ResearchArtifactForbiddenBehaviorKind.ACTIVE_INGESTION,
            name="Active ingestion",
            description="Active ingestion remains forbidden.",
            **{flag: False},
        )


def test_research_artifact_forbidden_behavior_rejects_unknown_kind_and_severity() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactForbiddenBehavior(
            behavior_id="research-artifact-unknown-kind-v1",
            kind=ResearchArtifactForbiddenBehaviorKind.UNKNOWN,
            name="Unknown",
            description="Unknown behavior.",
        )
    with pytest.raises(ValidationError):
        ResearchArtifactForbiddenBehavior(
            behavior_id="research-artifact-unknown-severity-v1",
            kind=ResearchArtifactForbiddenBehaviorKind.ACTIVE_INGESTION,
            name="Unknown severity",
            description="Unknown severity.",
            severity=ResearchArtifactBoundarySeverity.UNKNOWN,
        )


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
        "pdf_parsing_allowed",
        "arxiv_ingestion_allowed",
        "llm_analysis_allowed",
        "strategy_generation_allowed",
        "strategy_code_generation_allowed",
        "backtesting_allowed",
        "optimization_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
    ],
)
def test_research_artifact_forbidden_registry_rejects_dangerous_allow_flags(flag: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactForbiddenBehaviorRegistry(
            registry_id="research-artifact-forbidden-registry-test-v1",
            behaviors=default_research_artifact_forbidden_behaviors(),
            **{flag: True},
        )


def test_research_artifact_forbidden_registry_requires_complete_coverage() -> None:
    behaviors = [
        behavior
        for behavior in default_research_artifact_forbidden_behaviors()
        if behavior.kind != ResearchArtifactForbiddenBehaviorKind.EXECUTION
    ]

    with pytest.raises(ValidationError):
        ResearchArtifactForbiddenBehaviorRegistry(
            registry_id="research-artifact-incomplete-registry-test-v1",
            behaviors=behaviors,
        )

