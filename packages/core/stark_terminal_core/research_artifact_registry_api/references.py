from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactKind,
    non_empty_text,
    normalize_datetime,
    utc_now,
)


def _optional_trimmed(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


class ResearchArtifactApiReferencePlaceholder(BaseModel):
    api_reference_id: str
    artifact_id_placeholder: str | None = None
    reference_uri_placeholder: str | None = "api-reference-uri-placeholder"
    external_fetch_enabled: bool = False
    local_file_read_enabled: bool = False
    checksum_validation_enabled: bool = False
    source_trusted: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("api_reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact API reference placeholder text fields")

    @field_validator("artifact_id_placeholder", "reference_uri_placeholder")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def reference_must_remain_descriptive(self) -> ResearchArtifactApiReferencePlaceholder:
        if self.reference_uri_placeholder is not None and "placeholder" not in self.reference_uri_placeholder.lower():
            raise ValueError("reference URI must remain a placeholder")
        dangerous_flags = {
            "external fetch": self.external_fetch_enabled,
            "local file read": self.local_file_read_enabled,
            "checksum validation": self.checksum_validation_enabled,
            "source trust": self.source_trusted,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"API reference placeholder cannot enable: {', '.join(enabled)}")
        return self


class ResearchArtifactMetadataReferencePlaceholder(BaseModel):
    metadata_reference_id: str
    artifact_kind: ResearchArtifactKind = ResearchArtifactKind.PAPER_REFERENCE
    validated_artifact_record: bool = False
    persistent_record_available: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("metadata_reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact metadata API reference placeholder text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def metadata_reference_must_fail_closed(self) -> ResearchArtifactMetadataReferencePlaceholder:
        if self.artifact_kind == ResearchArtifactKind.UNKNOWN:
            raise ValueError("UNKNOWN artifact kind is not allowed in API metadata references")
        if self.validated_artifact_record:
            raise ValueError("API metadata reference cannot claim a validated artifact")
        if self.persistent_record_available:
            raise ValueError("API metadata reference cannot claim persistent storage")
        return self


class ResearchArtifactProvenanceReferencePlaceholder(BaseModel):
    provenance_reference_id: str
    descriptive_only: bool = True
    external_source_validated: bool = False
    real_market_data_trusted: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("provenance_reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact provenance API reference placeholder text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def provenance_reference_must_fail_closed(self) -> ResearchArtifactProvenanceReferencePlaceholder:
        if not self.descriptive_only:
            raise ValueError("API provenance reference must remain descriptive only")
        if self.external_source_validated:
            raise ValueError("API provenance reference cannot validate external sources")
        if self.real_market_data_trusted:
            raise ValueError("API provenance reference cannot trust real market data")
        return self


def default_research_artifact_api_reference_placeholder() -> ResearchArtifactApiReferencePlaceholder:
    return ResearchArtifactApiReferencePlaceholder(
        api_reference_id="research-artifact-api-reference-placeholder-v1",
        artifact_id_placeholder="artifact-id-placeholder",
    )


def default_research_artifact_metadata_reference_placeholder() -> ResearchArtifactMetadataReferencePlaceholder:
    return ResearchArtifactMetadataReferencePlaceholder(
        metadata_reference_id="research-artifact-api-metadata-reference-placeholder-v1",
    )


def default_research_artifact_provenance_reference_placeholder() -> ResearchArtifactProvenanceReferencePlaceholder:
    return ResearchArtifactProvenanceReferencePlaceholder(
        provenance_reference_id="research-artifact-api-provenance-reference-placeholder-v1",
    )
