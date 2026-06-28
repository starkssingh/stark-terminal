from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index_display.badges import (
    ResearchArtifactIndexDisplayBadgeMeaning,
    ResearchArtifactIndexLifecycleBadgePlaceholder,
    default_research_artifact_index_lifecycle_badge_placeholder,
    default_research_artifact_index_safety_badge_placeholder,
)


def test_research_artifact_index_display_badges_validate_allowed_meanings() -> None:
    lifecycle_badge = default_research_artifact_index_lifecycle_badge_placeholder()
    safety_badge = default_research_artifact_index_safety_badge_placeholder()

    assert lifecycle_badge.meaning == ResearchArtifactIndexDisplayBadgeMeaning.PLACEHOLDER
    assert safety_badge.unavailable is True
    allowed = {meaning.value for meaning in ResearchArtifactIndexDisplayBadgeMeaning}
    assert {
        "PLACEHOLDER",
        "REFERENCED",
        "DRAFT",
        "REVIEW_REQUIRED",
        "BLOCKED",
        "DEFERRED",
        "UNAVAILABLE",
        "UNKNOWN",
    } <= allowed
    for forbidden in [
        "INDEXED",
        "SEARCHABLE",
        "RANKED",
        "EMBEDDED",
        "RETRIEVED",
        "VALIDATED_STRATEGY",
        "BACKTESTED_PROFITABLE",
        "RECOMMENDED",
        "READY_TO_TRADE",
        "EXECUTABLE",
    ]:
        assert forbidden not in allowed


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui",
        "indexed_ready",
        "searchable_ready",
        "ranked_ready",
        "embedded_ready",
        "retrieved_ready",
        "recommendation_ready",
        "backtest_ready",
        "readiness_to_trade",
        "broker_control",
        "execution_ready",
    ],
)
def test_research_artifact_index_display_badge_rejects_forbidden_meanings(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexLifecycleBadgePlaceholder(
            badge_id="badge",
            label="Badge",
            **{field_name: True},
        )
