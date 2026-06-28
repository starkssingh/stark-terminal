from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    non_empty_text,
    normalize_datetime,
    optional_text,
    utc_now,
)


class _IndexDisplayReferencePlaceholderBase(BaseModel):
    display_reference_id: str
    label: str
    placeholder_text: str | None = None
    descriptive_only: bool = True
    external_fetch_enabled: bool = False
    local_file_read_enabled: bool = False
    registry_lookup_enabled: bool = False
    index_lookup_enabled: bool = False
    trusted_source_content_displayed: bool = False
    parsed_paper_excerpt_present: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("display_reference_id", "label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index display reference text fields")

    @field_validator("placeholder_text")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return optional_text(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def reference_must_remain_descriptive(self) -> _IndexDisplayReferencePlaceholderBase:
        if not self.descriptive_only:
            raise ValueError("Research Artifact Index display references must remain descriptive only")
        dangerous_flags = {
            "external fetch": self.external_fetch_enabled,
            "local file read": self.local_file_read_enabled,
            "registry lookup": self.registry_lookup_enabled,
            "index lookup": self.index_lookup_enabled,
            "trusted source content": self.trusted_source_content_displayed,
            "parsed paper excerpt": self.parsed_paper_excerpt_present,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"Research Artifact Index display reference cannot enable: {', '.join(enabled)}")
        return self


class ResearchArtifactIndexDisplayReferencePlaceholder(_IndexDisplayReferencePlaceholderBase):
    index_id_placeholder: str = "index-id-placeholder"

    @field_validator("index_id_placeholder")
    @classmethod
    def index_id_placeholder_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index display reference placeholder")


class ResearchArtifactIndexSourceDisplayPlaceholder(_IndexDisplayReferencePlaceholderBase):
    source_label_placeholder: str = "source-label-placeholder"

    @field_validator("source_label_placeholder")
    @classmethod
    def source_label_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index source display placeholder")


class ResearchArtifactIndexRegistryDisplayReferencePlaceholder(_IndexDisplayReferencePlaceholderBase):
    registry_reference_placeholder: str = "registry-reference-placeholder"

    @field_validator("registry_reference_placeholder")
    @classmethod
    def registry_reference_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index registry display reference placeholder")


def default_research_artifact_index_display_reference_placeholder() -> ResearchArtifactIndexDisplayReferencePlaceholder:
    return ResearchArtifactIndexDisplayReferencePlaceholder(
        display_reference_id="research-artifact-index-display-reference-placeholder-v1",
        label="Research Artifact Index Display Reference Placeholder",
        placeholder_text="Descriptive display reference only; no external fetch, local file read, registry lookup, or index lookup.",
    )


def default_research_artifact_index_source_display_placeholder() -> ResearchArtifactIndexSourceDisplayPlaceholder:
    return ResearchArtifactIndexSourceDisplayPlaceholder(
        display_reference_id="research-artifact-index-source-display-placeholder-v1",
        label="Research Artifact Index Source Display Placeholder",
    )


def default_research_artifact_index_registry_display_reference_placeholder() -> ResearchArtifactIndexRegistryDisplayReferencePlaceholder:
    return ResearchArtifactIndexRegistryDisplayReferencePlaceholder(
        display_reference_id="research-artifact-index-registry-display-reference-placeholder-v1",
        label="Research Artifact Registry Display Reference Placeholder",
    )

