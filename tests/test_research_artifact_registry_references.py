from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.references import (
    ResearchArtifactReferencePlaceholder,
    default_research_artifact_reference_placeholders,
)
from stark_terminal_core.research_artifact_registry.types import ResearchArtifactReferenceKind


def _reference(**overrides: object) -> ResearchArtifactReferencePlaceholder:
    data = {
        "reference_id": "reference-placeholder-v1",
        "artifact_id": "metadata-placeholder-v1",
        "reference_kind": ResearchArtifactReferenceKind.PAPER_REFERENCE_PLACEHOLDER,
        "reference_uri_placeholder": "uri-placeholder",
        "source_label": "Source placeholder",
        "checksum_placeholder": "checksum-placeholder",
    }
    data.update(overrides)
    return ResearchArtifactReferencePlaceholder(**data)


def test_reference_placeholder_validates_without_external_fetch() -> None:
    placeholder = _reference()

    assert placeholder.reference_uri_placeholder == "uri-placeholder"
    assert placeholder.checksum_placeholder == "checksum-placeholder"


def test_reference_placeholder_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _reference(reference_kind=ResearchArtifactReferenceKind.UNKNOWN)


def test_reference_uri_and_checksum_must_remain_placeholder_values() -> None:
    with pytest.raises(ValidationError):
        _reference(reference_uri_placeholder="https://example.com/paper.pdf")
    with pytest.raises(ValidationError):
        _reference(checksum_placeholder="abc123")


def test_reference_placeholder_has_no_file_read_behavior() -> None:
    fields = set(ResearchArtifactReferencePlaceholder.model_fields)

    assert "file_bytes" not in fields
    assert "downloaded_content" not in fields
    assert "parsed_content" not in fields


def test_default_reference_placeholders_validate() -> None:
    assert default_research_artifact_reference_placeholders()

