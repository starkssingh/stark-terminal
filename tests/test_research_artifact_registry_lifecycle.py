from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.lifecycle import (
    ResearchArtifactLifecyclePlaceholder,
    default_research_artifact_lifecycle_placeholders,
)
from stark_terminal_core.research_artifact_registry.types import ResearchArtifactLifecycleStatus


def test_lifecycle_placeholder_validates() -> None:
    placeholder = ResearchArtifactLifecyclePlaceholder(
        lifecycle_id="lifecycle-placeholder-v1",
        artifact_id="metadata-placeholder-v1",
        status=ResearchArtifactLifecycleStatus.PLACEHOLDER,
        allowed_next_statuses=[
            ResearchArtifactLifecycleStatus.REFERENCED,
            ResearchArtifactLifecycleStatus.REVIEW_REQUIRED,
        ],
        blocked_reason="Planning only.",
    )

    assert placeholder.status == ResearchArtifactLifecycleStatus.PLACEHOLDER


def test_lifecycle_placeholder_rejects_unknown_status() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactLifecyclePlaceholder(
            lifecycle_id="lifecycle-placeholder-v1",
            artifact_id="metadata-placeholder-v1",
            status=ResearchArtifactLifecycleStatus.UNKNOWN,
            allowed_next_statuses=[ResearchArtifactLifecycleStatus.PLACEHOLDER],
        )


def test_lifecycle_placeholder_supports_blocked_and_deferred_states() -> None:
    placeholders = default_research_artifact_lifecycle_placeholders()
    statuses = {placeholder.status for placeholder in placeholders}
    next_statuses = {status for placeholder in placeholders for status in placeholder.allowed_next_statuses}

    assert ResearchArtifactLifecycleStatus.BLOCKED in statuses
    assert ResearchArtifactLifecycleStatus.DEFERRED in next_statuses


def test_lifecycle_statuses_do_not_imply_strategy_recommendation_or_execution() -> None:
    placeholders = default_research_artifact_lifecycle_placeholders()
    searchable = " ".join(
        [
            placeholder.status.value
            for placeholder in placeholders
        ]
    ).lower()

    assert "approved" not in searchable
    assert "validated" not in searchable
    assert "recommendation" not in searchable
    assert "readiness" not in searchable
    assert "execution" not in searchable

