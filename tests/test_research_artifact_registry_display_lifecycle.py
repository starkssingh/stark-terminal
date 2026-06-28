from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.types import ResearchArtifactLifecycleStatus
from stark_terminal_core.research_artifact_registry_display.lifecycle import (
    ResearchArtifactLifecycleDisplayPlaceholder,
    default_research_artifact_lifecycle_display_placeholder,
)


def test_lifecycle_display_placeholder_is_safe() -> None:
    lifecycle = default_research_artifact_lifecycle_display_placeholder()

    assert lifecycle.display_contract_skeleton_only is True
    assert lifecycle.status == ResearchArtifactLifecycleStatus.PLACEHOLDER
    assert lifecycle.validated_strategy is False
    assert lifecycle.approved_strategy is False
    assert lifecycle.recommended_strategy is False
    assert lifecycle.backtested_strategy is False
    assert lifecycle.readiness_to_trade is False
    assert lifecycle.execution_ready is False


@pytest.mark.parametrize(
    "field_name",
    [
        "validated_strategy",
        "approved_strategy",
        "recommended_strategy",
        "backtested_strategy",
        "readiness_to_trade",
        "execution_ready",
    ],
)
def test_lifecycle_display_rejects_strategy_recommendation_or_execution_implications(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactLifecycleDisplayPlaceholder(
            lifecycle_display_id="lifecycle",
            **{field_name: True},
        )


def test_lifecycle_display_rejects_unknown_status() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactLifecycleDisplayPlaceholder(
            lifecycle_display_id="lifecycle",
            status=ResearchArtifactLifecycleStatus.UNKNOWN,
        )
