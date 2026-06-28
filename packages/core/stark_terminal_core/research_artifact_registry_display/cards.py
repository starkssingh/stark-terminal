from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactKind,
    ResearchArtifactLifecycleStatus,
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


class _CardPlaceholderBase(BaseModel):
    card_id: str
    title: str
    artifact_kind: ResearchArtifactKind = ResearchArtifactKind.PAPER_REFERENCE
    lifecycle_status: ResearchArtifactLifecycleStatus = ResearchArtifactLifecycleStatus.PLACEHOLDER
    display_contract_skeleton_only: bool = True
    active_ui: bool = False
    frontend_component: bool = False
    desktop_widget: bool = False
    file_content_preview: bool = False
    parsed_paper_content: bool = False
    generated_strategy_content: bool = False
    backtest_metrics_present: bool = False
    recommendation_fields_present: bool = False
    action_fields_present: bool = False
    confidence_fields_present: bool = False
    execution_controls_present: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("card_id", "title", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact display card text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def card_must_remain_placeholder(self) -> _CardPlaceholderBase:
        if self.artifact_kind == ResearchArtifactKind.UNKNOWN:
            raise ValueError("UNKNOWN artifact kind is not allowed in display card placeholders")
        if self.lifecycle_status == ResearchArtifactLifecycleStatus.UNKNOWN:
            raise ValueError("UNKNOWN lifecycle status is not allowed in display card placeholders")
        if not self.display_contract_skeleton_only:
            raise ValueError("display card must remain display-contract-skeleton-only")
        dangerous_flags = {
            "active UI": self.active_ui,
            "frontend component": self.frontend_component,
            "desktop widget": self.desktop_widget,
            "file content preview": self.file_content_preview,
            "parsed paper content": self.parsed_paper_content,
            "generated strategy content": self.generated_strategy_content,
            "backtest metrics": self.backtest_metrics_present,
            "recommendation fields": self.recommendation_fields_present,
            "action fields": self.action_fields_present,
            "confidence fields": self.confidence_fields_present,
            "execution controls": self.execution_controls_present,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"display card placeholder cannot include: {', '.join(enabled)}")
        return self


class ResearchArtifactCardPlaceholder(_CardPlaceholderBase):
    subtitle: str | None = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def tags_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)


class ResearchArtifactMetadataCardPlaceholder(_CardPlaceholderBase):
    metadata_reference_id: str = "metadata-reference-placeholder"

    @field_validator("metadata_reference_id")
    @classmethod
    def metadata_reference_id_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact metadata card reference")


class ResearchArtifactReferenceCardPlaceholder(_CardPlaceholderBase):
    reference_id_placeholder: str = "reference-id-placeholder"
    source_label_placeholder: str | None = "source-label-placeholder"

    @field_validator("reference_id_placeholder")
    @classmethod
    def reference_id_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact reference card placeholder")


def default_research_artifact_card_placeholder() -> ResearchArtifactCardPlaceholder:
    return ResearchArtifactCardPlaceholder(
        card_id="research-artifact-display-card-placeholder-v1",
        title="Research Artifact Card Placeholder",
        subtitle="Backend display contract metadata only.",
        tags=["display-contract-skeleton-only"],
        notes=["No active UI, file preview, parsed paper, strategy, backtest, recommendation, or execution."],
    )


def default_research_artifact_metadata_card_placeholder() -> ResearchArtifactMetadataCardPlaceholder:
    return ResearchArtifactMetadataCardPlaceholder(
        card_id="research-artifact-display-metadata-card-placeholder-v1",
        title="Metadata Card Placeholder",
        notes=["Metadata display placeholder only; no validated artifact record."],
    )


def default_research_artifact_reference_card_placeholder() -> ResearchArtifactReferenceCardPlaceholder:
    return ResearchArtifactReferenceCardPlaceholder(
        card_id="research-artifact-display-reference-card-placeholder-v1",
        title="Reference Card Placeholder",
        notes=["Reference display placeholder only; no file read, URL fetch, or content preview."],
    )
