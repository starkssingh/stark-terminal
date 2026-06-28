from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.references import (
    ResearchArtifactIndexReferencePlaceholder,
    default_research_artifact_index_reference_placeholders,
)


def test_research_artifact_index_reference_placeholder_validates() -> None:
    placeholder = ResearchArtifactIndexReferencePlaceholder(
        reference_id="reference-placeholder",
        index_id="index-placeholder",
        artifact_id_placeholder="artifact-id-placeholder",
        registry_id_placeholder="registry-id-placeholder",
        source_label="descriptive placeholder",
    )

    assert placeholder.planning_only is True


def test_research_artifact_index_reference_rejects_empty_or_trust_claims() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexReferencePlaceholder(reference_id="", index_id="index-placeholder")
    with pytest.raises(ValidationError):
        ResearchArtifactIndexReferencePlaceholder(
            reference_id="x",
            index_id="index-placeholder",
            artifact_id_placeholder="artifact-id-placeholder",
            source_label="validated source",
        )


def test_default_research_artifact_index_references_do_not_fetch_or_read_files() -> None:
    fields = set(ResearchArtifactIndexReferencePlaceholder.model_fields)
    placeholders = default_research_artifact_index_reference_placeholders()

    assert placeholders
    assert "fetch_url" not in fields
    assert "file_path" not in fields
    assert "source_uri_to_fetch" not in fields
    assert "trusted_source" not in fields
    assert all(item.planning_only for item in placeholders)

