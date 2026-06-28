from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexKeyKind,
    ResearchArtifactIndexKind,
    non_empty_text,
    normalize_datetime,
    optional_text,
    utc_now,
)


class _IndexApiReferencePlaceholderBase(BaseModel):
    reference_id: str
    label: str
    placeholder_text: str | None = None
    descriptive_only: bool = True
    external_fetch_enabled: bool = False
    local_file_read_enabled: bool = False
    registry_lookup_enabled: bool = False
    index_lookup_enabled: bool = False
    checksum_validation_enabled: bool = False
    source_trusted: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("reference_id", "label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API reference placeholder text fields")

    @field_validator("placeholder_text")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return optional_text(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def reference_must_remain_descriptive(self) -> _IndexApiReferencePlaceholderBase:
        if not self.descriptive_only:
            raise ValueError("Research Artifact Index API reference placeholders must remain descriptive only")
        dangerous_flags = {
            "external fetch": self.external_fetch_enabled,
            "local file read": self.local_file_read_enabled,
            "registry lookup": self.registry_lookup_enabled,
            "index lookup": self.index_lookup_enabled,
            "checksum validation": self.checksum_validation_enabled,
            "source trust": self.source_trusted,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"Research Artifact Index API reference placeholder cannot enable: {', '.join(enabled)}")
        return self


class ResearchArtifactIndexApiReferencePlaceholder(_IndexApiReferencePlaceholderBase):
    api_family: str = "research-artifact-index-api"

    @field_validator("api_family")
    @classmethod
    def api_family_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API family")


class ResearchArtifactIndexMetadataReferencePlaceholder(_IndexApiReferencePlaceholderBase):
    index_kind: ResearchArtifactIndexKind = ResearchArtifactIndexKind.METADATA_INDEX_PLACEHOLDER
    validated_index_record: bool = False
    persistent_record_available: bool = False

    @model_validator(mode="after")
    def metadata_reference_must_fail_closed(self) -> ResearchArtifactIndexMetadataReferencePlaceholder:
        if self.index_kind == ResearchArtifactIndexKind.UNKNOWN:
            raise ValueError("UNKNOWN index kind is not allowed in API metadata references")
        if self.validated_index_record:
            raise ValueError("API metadata reference cannot claim a validated index record")
        if self.persistent_record_available:
            raise ValueError("API metadata reference cannot claim persistent storage")
        return self


class ResearchArtifactIndexKeyReferencePlaceholder(_IndexApiReferencePlaceholderBase):
    key_kind: ResearchArtifactIndexKeyKind = ResearchArtifactIndexKeyKind.ARTIFACT_ID

    @model_validator(mode="after")
    def key_reference_must_use_known_kind(self) -> ResearchArtifactIndexKeyReferencePlaceholder:
        if self.key_kind == ResearchArtifactIndexKeyKind.UNKNOWN:
            raise ValueError("UNKNOWN key kind is not allowed in API key references")
        return self


class ResearchArtifactIndexProvenanceReferencePlaceholder(_IndexApiReferencePlaceholderBase):
    external_source_validated: bool = False
    real_market_data_trusted: bool = False

    @model_validator(mode="after")
    def provenance_reference_must_fail_closed(self) -> ResearchArtifactIndexProvenanceReferencePlaceholder:
        if self.external_source_validated:
            raise ValueError("API provenance reference cannot validate external sources")
        if self.real_market_data_trusted:
            raise ValueError("API provenance reference cannot trust real market data")
        return self


class ResearchArtifactIndexRegistryReferencePlaceholder(_IndexApiReferencePlaceholderBase):
    registry_reference_placeholder: str = "registry-reference-placeholder"

    @field_validator("registry_reference_placeholder")
    @classmethod
    def registry_placeholder_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index API registry reference placeholder")


def default_research_artifact_index_api_reference_placeholder() -> ResearchArtifactIndexApiReferencePlaceholder:
    return ResearchArtifactIndexApiReferencePlaceholder(
        reference_id="research-artifact-index-api-reference-placeholder-v1",
        label="Research Artifact Index API Reference Placeholder",
        placeholder_text="Descriptive API reference only; no external fetch, local file read, registry lookup, or index lookup.",
    )


def default_research_artifact_index_metadata_reference_placeholder() -> ResearchArtifactIndexMetadataReferencePlaceholder:
    return ResearchArtifactIndexMetadataReferencePlaceholder(
        reference_id="research-artifact-index-api-metadata-reference-placeholder-v1",
        label="Research Artifact Index Metadata Reference Placeholder",
    )


def default_research_artifact_index_key_reference_placeholder() -> ResearchArtifactIndexKeyReferencePlaceholder:
    return ResearchArtifactIndexKeyReferencePlaceholder(
        reference_id="research-artifact-index-api-key-reference-placeholder-v1",
        label="Research Artifact Index Key Reference Placeholder",
    )


def default_research_artifact_index_provenance_reference_placeholder() -> ResearchArtifactIndexProvenanceReferencePlaceholder:
    return ResearchArtifactIndexProvenanceReferencePlaceholder(
        reference_id="research-artifact-index-api-provenance-reference-placeholder-v1",
        label="Research Artifact Index Provenance Reference Placeholder",
    )


def default_research_artifact_index_registry_reference_placeholder() -> ResearchArtifactIndexRegistryReferencePlaceholder:
    return ResearchArtifactIndexRegistryReferencePlaceholder(
        reference_id="research-artifact-index-api-registry-reference-placeholder-v1",
        label="Research Artifact Registry Reference Placeholder",
    )
