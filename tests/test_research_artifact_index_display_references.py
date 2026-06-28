from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index_display.references import (
    ResearchArtifactIndexDisplayReferencePlaceholder,
    default_research_artifact_index_display_reference_placeholder,
    default_research_artifact_index_registry_display_reference_placeholder,
    default_research_artifact_index_source_display_placeholder,
)


def test_research_artifact_index_display_references_are_descriptive_only() -> None:
    for placeholder in [
        default_research_artifact_index_display_reference_placeholder(),
        default_research_artifact_index_source_display_placeholder(),
        default_research_artifact_index_registry_display_reference_placeholder(),
    ]:
        assert placeholder.descriptive_only is True
        assert placeholder.external_fetch_enabled is False
        assert placeholder.local_file_read_enabled is False
        assert placeholder.registry_lookup_enabled is False
        assert placeholder.index_lookup_enabled is False
        assert placeholder.trusted_source_content_displayed is False
        assert placeholder.parsed_paper_excerpt_present is False


@pytest.mark.parametrize(
    "field_name",
    [
        "descriptive_only",
        "external_fetch_enabled",
        "local_file_read_enabled",
        "registry_lookup_enabled",
        "index_lookup_enabled",
        "trusted_source_content_displayed",
        "parsed_paper_excerpt_present",
    ],
)
def test_research_artifact_index_display_reference_rejects_fetch_lookup_and_trust_fields(
    field_name: str,
) -> None:
    value = False if field_name == "descriptive_only" else True
    with pytest.raises(ValidationError):
        ResearchArtifactIndexDisplayReferencePlaceholder(
            display_reference_id="reference",
            label="Reference",
            **{field_name: value},
        )


def test_research_artifact_index_display_reference_has_no_fetch_fields() -> None:
    fields = set(ResearchArtifactIndexDisplayReferencePlaceholder.model_fields)

    for forbidden in ["url_to_fetch", "file_path", "registry_lookup", "index_lookup", "paper_excerpt"]:
        assert forbidden not in fields
