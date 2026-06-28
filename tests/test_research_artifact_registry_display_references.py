from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_display.references import (
    ResearchArtifactDisplayReferencePlaceholder,
    ResearchArtifactSourceDisplayPlaceholder,
    default_research_artifact_display_reference_placeholder,
    default_research_artifact_source_display_placeholder,
)


def test_display_reference_placeholders_validate_as_descriptive_only() -> None:
    reference = default_research_artifact_display_reference_placeholder()
    source = default_research_artifact_source_display_placeholder()

    assert reference.descriptive_only is True
    assert reference.external_fetch_enabled is False
    assert reference.local_file_read_enabled is False
    assert reference.source_trusted is False
    assert reference.parsed_paper_excerpt_present is False
    assert source.descriptive_only is True
    assert source.trusted_source_content_displayed is False
    assert source.external_fetch_enabled is False
    assert source.local_file_read_enabled is False
    assert source.parsed_paper_excerpt_present is False


def test_display_reference_requires_placeholder_uri() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactDisplayReferencePlaceholder(
            display_reference_id="reference",
            reference_uri_placeholder="https://example.com/paper.pdf",
        )


@pytest.mark.parametrize("field_name", ["external_fetch_enabled", "local_file_read_enabled", "source_trusted", "parsed_paper_excerpt_present"])
def test_display_reference_rejects_fetch_read_trust_or_excerpt(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactDisplayReferencePlaceholder(display_reference_id="reference", **{field_name: True})


@pytest.mark.parametrize("field_name", ["trusted_source_content_displayed", "external_fetch_enabled", "local_file_read_enabled", "parsed_paper_excerpt_present"])
def test_source_display_rejects_fetch_read_trust_or_excerpt(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactSourceDisplayPlaceholder(source_display_id="source", **{field_name: True})
