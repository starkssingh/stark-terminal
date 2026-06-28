from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.types import ResearchArtifactIndexTagKind
from stark_terminal_core.research_artifact_index_display.tags import (
    ResearchArtifactIndexTagDisplayPlaceholder,
    default_research_artifact_index_tag_display_placeholder,
)


def test_research_artifact_index_tag_display_placeholder_is_label_only() -> None:
    placeholder = default_research_artifact_index_tag_display_placeholder()

    assert placeholder.display_label_only is True
    assert placeholder.search_behavior_enabled is False
    assert placeholder.ranking_behavior_enabled is False
    assert placeholder.ranking_weight_displayed is False
    assert placeholder.embeddings_enabled is False
    assert placeholder.vector_store_reference_present is False
    assert placeholder.active_filter_ui_enabled is False


@pytest.mark.parametrize(
    "field_name",
    [
        "display_label_only",
        "search_behavior_enabled",
        "ranking_behavior_enabled",
        "ranking_weight_displayed",
        "embeddings_enabled",
        "vector_store_reference_present",
        "active_filter_ui_enabled",
    ],
)
def test_research_artifact_index_tag_display_rejects_behavior_fields(field_name: str) -> None:
    value = False if field_name == "display_label_only" else True
    with pytest.raises(ValidationError):
        ResearchArtifactIndexTagDisplayPlaceholder(
            tag_display_id="tag",
            tag_label="Tag",
            **{field_name: value},
        )


def test_research_artifact_index_tag_display_rejects_unknown_tag_kind() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexTagDisplayPlaceholder(
            tag_display_id="tag",
            tag_label="Tag",
            tag_kind=ResearchArtifactIndexTagKind.UNKNOWN,
        )
