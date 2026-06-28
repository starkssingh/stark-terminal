from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexKeyKind,
    ResearchArtifactIndexKind,
)
from stark_terminal_core.research_artifact_index_api.references import (
    ResearchArtifactIndexApiReferencePlaceholder,
    ResearchArtifactIndexKeyReferencePlaceholder,
    ResearchArtifactIndexMetadataReferencePlaceholder,
    ResearchArtifactIndexProvenanceReferencePlaceholder,
    default_research_artifact_index_api_reference_placeholder,
    default_research_artifact_index_key_reference_placeholder,
    default_research_artifact_index_metadata_reference_placeholder,
    default_research_artifact_index_provenance_reference_placeholder,
    default_research_artifact_index_registry_reference_placeholder,
)


def test_research_artifact_index_api_reference_placeholders_validate() -> None:
    placeholders = [
        default_research_artifact_index_api_reference_placeholder(),
        default_research_artifact_index_metadata_reference_placeholder(),
        default_research_artifact_index_key_reference_placeholder(),
        default_research_artifact_index_provenance_reference_placeholder(),
        default_research_artifact_index_registry_reference_placeholder(),
    ]

    assert all(placeholder.descriptive_only for placeholder in placeholders)
    assert all(placeholder.external_fetch_enabled is False for placeholder in placeholders)
    assert all(placeholder.local_file_read_enabled is False for placeholder in placeholders)
    assert all(placeholder.registry_lookup_enabled is False for placeholder in placeholders)
    assert all(placeholder.index_lookup_enabled is False for placeholder in placeholders)
    assert all(placeholder.source_trusted is False for placeholder in placeholders)


@pytest.mark.parametrize(
    "field_name",
    [
        "descriptive_only",
        "external_fetch_enabled",
        "local_file_read_enabled",
        "registry_lookup_enabled",
        "index_lookup_enabled",
        "checksum_validation_enabled",
        "source_trusted",
    ],
)
def test_research_artifact_index_api_references_reject_fetch_lookup_or_trust(field_name: str) -> None:
    value = False if field_name == "descriptive_only" else True
    with pytest.raises(ValidationError):
        ResearchArtifactIndexApiReferencePlaceholder(
            reference_id="reference",
            label="reference",
            **{field_name: value},
        )


def test_research_artifact_index_api_references_reject_unknown_or_validated_claims() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexMetadataReferencePlaceholder(
            reference_id="metadata",
            label="metadata",
            index_kind=ResearchArtifactIndexKind.UNKNOWN,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactIndexMetadataReferencePlaceholder(
            reference_id="metadata",
            label="metadata",
            validated_index_record=True,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactIndexKeyReferencePlaceholder(
            reference_id="key",
            label="key",
            key_kind=ResearchArtifactIndexKeyKind.UNKNOWN,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactIndexProvenanceReferencePlaceholder(
            reference_id="provenance",
            label="provenance",
            external_source_validated=True,
        )
