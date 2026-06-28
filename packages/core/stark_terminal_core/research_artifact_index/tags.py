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


class ResearchArtifactIndexTagPlaceholder(BaseModel):
    tag_id: str
    tag_kind: ResearchArtifactIndexTagKind
    tag_label: str
    tag_value_placeholder: str | None = None
    schema_version: str = "v1"
    planning_only: bool = True
    ranking_weight: float | None = None
    search_enabled: bool = False
    ranking_enabled: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("tag_id", "tag_label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index tag placeholder text fields")

    @field_validator("tag_value_placeholder")
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        return optional_text(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def tag_must_remain_inert(self) -> ResearchArtifactIndexTagPlaceholder:
        if self.tag_kind == ResearchArtifactIndexTagKind.UNKNOWN:
            raise ValueError("UNKNOWN research artifact index tag kind is not allowed")
        if not self.planning_only:
            raise ValueError("research artifact index tag must remain planning-only")
        if self.ranking_weight is not None:
            raise ValueError("ranking_weight must remain None in Prompt 77")
        if self.search_enabled or self.ranking_enabled:
            raise ValueError("research artifact index tag cannot enable search or ranking")
        if self.tag_value_placeholder is not None and "placeholder" not in self.tag_value_placeholder.lower():
            raise ValueError("tag_value_placeholder must remain placeholder-only")
        return self


def default_research_artifact_index_tag_placeholders() -> list[ResearchArtifactIndexTagPlaceholder]:
    return [
        ResearchArtifactIndexTagPlaceholder(
            tag_id="research-artifact-index-topic-tag-placeholder-v1",
            tag_kind=ResearchArtifactIndexTagKind.TOPIC,
            tag_label="Topic tag placeholder",
            tag_value_placeholder="topic-tag-placeholder",
        ),
        ResearchArtifactIndexTagPlaceholder(
            tag_id="research-artifact-index-safety-tag-placeholder-v1",
            tag_kind=ResearchArtifactIndexTagKind.SAFETY,
            tag_label="Safety tag placeholder",
            tag_value_placeholder="safety-tag-placeholder",
        ),
        ResearchArtifactIndexTagPlaceholder(
            tag_id="research-artifact-index-status-tag-placeholder-v1",
            tag_kind=ResearchArtifactIndexTagKind.STATUS,
            tag_label="Lifecycle status tag placeholder",
            tag_value_placeholder="status-tag-placeholder",
        ),
    ]
