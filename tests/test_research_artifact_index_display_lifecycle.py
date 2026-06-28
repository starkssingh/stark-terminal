from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index_display.lifecycle import (
    ResearchArtifactIndexLifecycleDisplayPlaceholder,
    default_research_artifact_index_lifecycle_display_placeholder,
)


def test_research_artifact_index_lifecycle_display_is_inert() -> None:
    placeholder = default_research_artifact_index_lifecycle_display_placeholder()

    assert placeholder.display_contract_skeleton_only is True
    for field_name in [
        "indexed",
        "searchable",
        "ranked",
        "embedded",
        "retrieved",
        "validated_strategy",
        "approved_strategy",
        "recommended_strategy",
        "backtested_strategy",
        "readiness_to_trade",
        "execution_ready",
    ]:
        assert getattr(placeholder, field_name) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "indexed",
        "searchable",
        "ranked",
        "embedded",
        "retrieved",
        "validated_strategy",
        "approved_strategy",
        "recommended_strategy",
        "backtested_strategy",
        "readiness_to_trade",
        "execution_ready",
    ],
)
def test_research_artifact_index_lifecycle_display_rejects_active_meanings(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexLifecycleDisplayPlaceholder(
            lifecycle_display_id="lifecycle",
            label="Lifecycle",
            status="PLACEHOLDER",
            **{field_name: True},
        )
