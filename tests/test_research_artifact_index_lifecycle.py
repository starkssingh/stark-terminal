from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.lifecycle import (
    ResearchArtifactIndexLifecyclePlaceholder,
    default_research_artifact_index_lifecycle_placeholders,
)
from stark_terminal_core.research_artifact_index.types import ResearchArtifactIndexLifecycleStatus


def test_research_artifact_index_lifecycle_placeholder_validates() -> None:
    placeholder = ResearchArtifactIndexLifecyclePlaceholder(
        lifecycle_id="lifecycle-placeholder",
        index_id="index-placeholder",
        status=ResearchArtifactIndexLifecycleStatus.PLACEHOLDER,
        allowed_next_statuses=[ResearchArtifactIndexLifecycleStatus.BLOCKED],
    )

    assert placeholder.planning_only is True
    assert placeholder.status == ResearchArtifactIndexLifecycleStatus.PLACEHOLDER


def test_research_artifact_index_lifecycle_rejects_unknown_and_missing_next_states() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexLifecyclePlaceholder(
            lifecycle_id="x",
            index_id="x",
            status=ResearchArtifactIndexLifecycleStatus.UNKNOWN,
            allowed_next_statuses=[ResearchArtifactIndexLifecycleStatus.BLOCKED],
        )
    with pytest.raises(ValidationError):
        ResearchArtifactIndexLifecyclePlaceholder(
            lifecycle_id="x",
            index_id="x",
            status=ResearchArtifactIndexLifecycleStatus.BLOCKED,
            allowed_next_statuses=[],
        )


def test_default_research_artifact_index_lifecycle_supports_blocked_and_deferred_states() -> None:
    statuses = {item.status for item in default_research_artifact_index_lifecycle_placeholders()}

    assert ResearchArtifactIndexLifecycleStatus.PLACEHOLDER in statuses
    assert ResearchArtifactIndexLifecycleStatus.DEFERRED in statuses

