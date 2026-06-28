from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.metadata import (
    ResearchArtifactIndexMetadataPlaceholder,
    default_research_artifact_index_metadata_placeholders,
)
from stark_terminal_core.research_artifact_index.types import ResearchArtifactIndexKind


def test_research_artifact_index_metadata_placeholder_validates() -> None:
    placeholder = ResearchArtifactIndexMetadataPlaceholder(
        index_id="index-placeholder",
        index_kind=ResearchArtifactIndexKind.METADATA_INDEX_PLACEHOLDER,
        title="Index Placeholder",
        description="Planning-only placeholder",
    )

    assert placeholder.planning_only is True
    assert placeholder.indexing_engine_enabled is False
    assert placeholder.search_engine_enabled is False
    assert placeholder.ranking_engine_enabled is False
    assert placeholder.embeddings_enabled is False
    assert placeholder.vector_store_enabled is False
    assert placeholder.persistent_storage_enabled is False


def test_research_artifact_index_metadata_rejects_empty_or_unknown_values() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexMetadataPlaceholder(index_id="", index_kind=ResearchArtifactIndexKind.METADATA_INDEX_PLACEHOLDER, title="x")
    with pytest.raises(ValidationError):
        ResearchArtifactIndexMetadataPlaceholder(index_id="x", index_kind=ResearchArtifactIndexKind.UNKNOWN, title="x")
    with pytest.raises(ValidationError):
        ResearchArtifactIndexMetadataPlaceholder(index_id="x", index_kind=ResearchArtifactIndexKind.METADATA_INDEX_PLACEHOLDER, title="")


@pytest.mark.parametrize(
    "flag",
    [
        "indexing_engine_enabled",
        "search_engine_enabled",
        "ranking_engine_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistent_storage_enabled",
    ],
)
def test_research_artifact_index_metadata_rejects_enabled_dangerous_flags(flag: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexMetadataPlaceholder(
            index_id="x",
            index_kind=ResearchArtifactIndexKind.METADATA_INDEX_PLACEHOLDER,
            title="x",
            **{flag: True},
        )


def test_default_research_artifact_index_metadata_placeholders_are_planning_only() -> None:
    placeholders = default_research_artifact_index_metadata_placeholders()

    assert placeholders
    assert all(item.planning_only for item in placeholders)
    assert all(item.indexing_engine_enabled is False for item in placeholders)

