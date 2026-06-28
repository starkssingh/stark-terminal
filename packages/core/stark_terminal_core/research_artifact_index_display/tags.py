from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexTagKind,
    non_empty_text,
    normalize_datetime,
    optional_text,
    utc_now,
)


class ResearchArtifactIndexTagDisplayPlaceholder(BaseModel):
    tag_display_id: str
    tag_kind: ResearchArtifactIndexTagKind = ResearchArtifactIndexTagKind.TOPIC
    tag_label: str
    tag_value_placeholder: str | None = "tag-value-placeholder"
    display_label_only: bool = True
    search_behavior_enabled: bool = False
    ranking_behavior_enabled: bool = False
    ranking_weight_displayed: bool = False
    embeddings_enabled: bool = False
    vector_store_reference_present: bool = False
    active_filter_ui_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("tag_display_id", "tag_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index tag display placeholder text fields")

    @field_validator("tag_value_placeholder")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return optional_text(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def tag_display_must_remain_inert(self) -> ResearchArtifactIndexTagDisplayPlaceholder:
        if self.tag_kind == ResearchArtifactIndexTagKind.UNKNOWN:
            raise ValueError("UNKNOWN tag kind is not allowed in display tag placeholders")
        if not self.display_label_only:
            raise ValueError("tag display placeholder must remain display-label-only")
        dangerous_flags = {
            "search behavior": self.search_behavior_enabled,
            "ranking behavior": self.ranking_behavior_enabled,
            "ranking weight display": self.ranking_weight_displayed,
            "embeddings": self.embeddings_enabled,
            "vector-store reference": self.vector_store_reference_present,
            "active filter UI": self.active_filter_ui_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"tag display placeholder cannot enable: {', '.join(enabled)}")
        return self


def default_research_artifact_index_tag_display_placeholder() -> ResearchArtifactIndexTagDisplayPlaceholder:
    return ResearchArtifactIndexTagDisplayPlaceholder(
        tag_display_id="research-artifact-index-tag-display-placeholder-v1",
        tag_label="Index tag display placeholder",
        tag_value_placeholder="tag-value-placeholder",
    )

