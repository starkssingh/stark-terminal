from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_display.badges import (
    ResearchArtifactDisplayBadgeMeaning,
    ResearchArtifactLifecycleBadgePlaceholder,
    ResearchArtifactSafetyBadgePlaceholder,
    default_research_artifact_lifecycle_badge_placeholder,
    default_research_artifact_safety_badge_placeholder,
)


def test_display_badge_placeholders_validate() -> None:
    lifecycle = default_research_artifact_lifecycle_badge_placeholder()
    safety = default_research_artifact_safety_badge_placeholder()

    for badge in [lifecycle, safety]:
        assert badge.display_contract_skeleton_only is True
        assert badge.active_ui is False
        assert badge.recommendation_ready is False
        assert badge.backtest_ready is False
        assert badge.readiness_to_trade is False
        assert badge.broker_control is False
        assert badge.execution_ready is False
    assert safety.unavailable is True


def test_forbidden_badge_meanings_are_absent() -> None:
    forbidden = {
        "APPROVED_STRATEGY",
        "VALIDATED_STRATEGY",
        "BACKTESTED_PROFITABLE",
        "RECOMMENDED",
        "READY_TO_TRADE",
        "EXECUTABLE",
    }

    assert forbidden.isdisjoint(set(ResearchArtifactDisplayBadgeMeaning.__members__))


def test_badges_reject_unknown_or_active_meanings() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactLifecycleBadgePlaceholder(
            badge_id="badge",
            label="Unknown",
            meaning=ResearchArtifactDisplayBadgeMeaning.UNKNOWN,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactSafetyBadgePlaceholder(badge_id="badge", label="Safety", unavailable=False)


@pytest.mark.parametrize(
    "field_name",
    ["active_ui", "recommendation_ready", "backtest_ready", "readiness_to_trade", "broker_control", "execution_ready"],
)
def test_badges_reject_recommendation_backtest_readiness_broker_or_execution_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactLifecycleBadgePlaceholder(badge_id="badge", label="Badge", **{field_name: True})
