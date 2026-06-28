from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.keys import (
    ResearchArtifactIndexKeyPlaceholder,
    default_research_artifact_index_key_placeholders,
)
from stark_terminal_core.research_artifact_index.types import ResearchArtifactIndexKeyKind


def test_research_artifact_index_key_placeholder_validates() -> None:
    placeholder = ResearchArtifactIndexKeyPlaceholder(
        key_id="key-placeholder",
        key_kind=ResearchArtifactIndexKeyKind.ARTIFACT_ID,
        key_label="Artifact placeholder",
        key_value_placeholder="artifact-id-placeholder",
    )

    assert placeholder.planning_only is True
    assert placeholder.key_value_placeholder == "artifact-id-placeholder"


def test_research_artifact_index_key_rejects_empty_unknown_or_non_placeholder_values() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexKeyPlaceholder(key_id="", key_kind=ResearchArtifactIndexKeyKind.ARTIFACT_ID, key_label="x")
    with pytest.raises(ValidationError):
        ResearchArtifactIndexKeyPlaceholder(key_id="x", key_kind=ResearchArtifactIndexKeyKind.UNKNOWN, key_label="x")
    with pytest.raises(ValidationError):
        ResearchArtifactIndexKeyPlaceholder(
            key_id="x",
            key_kind=ResearchArtifactIndexKeyKind.ARTIFACT_ID,
            key_label="x",
            key_value_placeholder="real-key",
        )


def test_default_research_artifact_index_key_placeholders_do_not_lookup_search_or_fetch() -> None:
    placeholders = default_research_artifact_index_key_placeholders()
    fields = set(ResearchArtifactIndexKeyPlaceholder.model_fields)

    assert placeholders
    assert "lookup_url" not in fields
    assert "search_query" not in fields
    assert "retrieval_path" not in fields
    assert "fetch_url" not in fields
    assert all(item.planning_only for item in placeholders)

