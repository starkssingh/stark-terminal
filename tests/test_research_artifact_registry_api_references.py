from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.types import ResearchArtifactKind
from stark_terminal_core.research_artifact_registry_api.references import (
    ResearchArtifactApiReferencePlaceholder,
    ResearchArtifactMetadataReferencePlaceholder,
    ResearchArtifactProvenanceReferencePlaceholder,
    default_research_artifact_api_reference_placeholder,
    default_research_artifact_metadata_reference_placeholder,
    default_research_artifact_provenance_reference_placeholder,
)


def test_api_reference_placeholders_validate() -> None:
    api_reference = default_research_artifact_api_reference_placeholder()
    metadata_reference = default_research_artifact_metadata_reference_placeholder()
    provenance_reference = default_research_artifact_provenance_reference_placeholder()

    assert api_reference.external_fetch_enabled is False
    assert api_reference.local_file_read_enabled is False
    assert api_reference.checksum_validation_enabled is False
    assert api_reference.source_trusted is False
    assert metadata_reference.validated_artifact_record is False
    assert metadata_reference.persistent_record_available is False
    assert provenance_reference.descriptive_only is True
    assert provenance_reference.external_source_validated is False
    assert provenance_reference.real_market_data_trusted is False


@pytest.mark.parametrize(
    "field_name",
    [
        "external_fetch_enabled",
        "local_file_read_enabled",
        "checksum_validation_enabled",
        "source_trusted",
    ],
)
def test_api_reference_placeholder_rejects_active_reference_behavior(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactApiReferencePlaceholder(api_reference_id="reference", **{field_name: True})


def test_api_reference_placeholder_requires_placeholder_uri() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactApiReferencePlaceholder(
            api_reference_id="reference",
            reference_uri_placeholder="https://example.com/paper.pdf",
        )


def test_metadata_reference_rejects_validated_or_persistent_records() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactMetadataReferencePlaceholder(
            metadata_reference_id="metadata",
            artifact_kind=ResearchArtifactKind.UNKNOWN,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactMetadataReferencePlaceholder(
            metadata_reference_id="metadata",
            validated_artifact_record=True,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactMetadataReferencePlaceholder(
            metadata_reference_id="metadata",
            persistent_record_available=True,
        )


def test_provenance_reference_rejects_source_validation_and_trust_claims() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactProvenanceReferencePlaceholder(
            provenance_reference_id="provenance",
            descriptive_only=False,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactProvenanceReferencePlaceholder(
            provenance_reference_id="provenance",
            external_source_validated=True,
        )
    with pytest.raises(ValidationError):
        ResearchArtifactProvenanceReferencePlaceholder(
            provenance_reference_id="provenance",
            real_market_data_trusted=True,
        )
