from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactDisplayReferencePlaceholder(BaseModel):
    display_reference_id: str
    artifact_id_placeholder: str | None = "artifact-id-placeholder"
    reference_uri_placeholder: str | None = "display-reference-uri-placeholder"
    descriptive_only: bool = True
    external_fetch_enabled: bool = False
    local_file_read_enabled: bool = False
    source_trusted: bool = False
    parsed_paper_excerpt_present: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("display_reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact display reference text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def reference_must_remain_descriptive(self) -> ResearchArtifactDisplayReferencePlaceholder:
        if not self.descriptive_only:
            raise ValueError("display reference must remain descriptive only")
        if self.reference_uri_placeholder is not None and "placeholder" not in self.reference_uri_placeholder.lower():
            raise ValueError("display reference URI must remain a placeholder")
        dangerous_flags = {
            "external fetch": self.external_fetch_enabled,
            "local file read": self.local_file_read_enabled,
            "source trust": self.source_trusted,
            "parsed paper excerpt": self.parsed_paper_excerpt_present,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"display reference placeholder cannot enable: {', '.join(enabled)}")
        return self


class ResearchArtifactSourceDisplayPlaceholder(BaseModel):
    source_display_id: str
    source_label_placeholder: str = "source-label-placeholder"
    descriptive_only: bool = True
    trusted_source_content_displayed: bool = False
    external_fetch_enabled: bool = False
    local_file_read_enabled: bool = False
    parsed_paper_excerpt_present: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("source_display_id", "source_label_placeholder", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact source display placeholder text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def source_display_must_fail_closed(self) -> ResearchArtifactSourceDisplayPlaceholder:
        if not self.descriptive_only:
            raise ValueError("source display must remain descriptive only")
        dangerous_flags = {
            "trusted source content": self.trusted_source_content_displayed,
            "external fetch": self.external_fetch_enabled,
            "local file read": self.local_file_read_enabled,
            "parsed paper excerpt": self.parsed_paper_excerpt_present,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"source display placeholder cannot enable: {', '.join(enabled)}")
        return self


def default_research_artifact_display_reference_placeholder() -> ResearchArtifactDisplayReferencePlaceholder:
    return ResearchArtifactDisplayReferencePlaceholder(
        display_reference_id="research-artifact-display-reference-placeholder-v1",
    )


def default_research_artifact_source_display_placeholder() -> ResearchArtifactSourceDisplayPlaceholder:
    return ResearchArtifactSourceDisplayPlaceholder(
        source_display_id="research-artifact-source-display-placeholder-v1",
    )
