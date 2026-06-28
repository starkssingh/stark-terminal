from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.tags import (
    ResearchArtifactIndexTagPlaceholder,
    default_research_artifact_index_tag_placeholders,
)
from stark_terminal_core.research_artifact_index.types import ResearchArtifactIndexTagKind


def test_research_artifact_index_tag_placeholder_validates() -> None:
    placeholder = ResearchArtifactIndexTagPlaceholder(
        tag_id="tag-placeholder",
        tag_kind=ResearchArtifactIndexTagKind.TOPIC,
        tag_label="Topic placeholder",
        tag_value_placeholder="topic-placeholder",
    )

    assert placeholder.planning_only is True
    assert placeholder.ranking_weight is None
    assert placeholder.search_enabled is False
    assert placeholder.ranking_enabled is False


@pytest.mark.parametrize("kwargs", [{"tag_kind": ResearchArtifactIndexTagKind.UNKNOWN}, {"search_enabled": True}, {"ranking_enabled": True}, {"ranking_weight": 1.0}])
def test_research_artifact_index_tag_rejects_unknown_search_ranking_or_weights(kwargs: dict[str, object]) -> None:
    values = {
        "tag_id": "tag-placeholder",
        "tag_kind": ResearchArtifactIndexTagKind.TOPIC,
        "tag_label": "Topic placeholder",
        "tag_value_placeholder": "topic-placeholder",
    }
    values.update(kwargs)
    with pytest.raises(ValidationError):
        ResearchArtifactIndexTagPlaceholder(**values)


def test_default_research_artifact_index_tag_placeholders_are_inert() -> None:
    placeholders = default_research_artifact_index_tag_placeholders()

    assert placeholders
    assert all(item.search_enabled is False for item in placeholders)
    assert all(item.ranking_enabled is False for item in placeholders)
    assert all(item.ranking_weight is None for item in placeholders)

