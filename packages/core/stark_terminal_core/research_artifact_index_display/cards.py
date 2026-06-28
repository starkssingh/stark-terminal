from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexKind,
    ResearchArtifactIndexLifecycleStatus,
    ResearchArtifactIndexTagKind,
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


class _IndexDisplayCardPlaceholderBase(BaseModel):
    card_id: str
    title: str
    index_kind: ResearchArtifactIndexKind = ResearchArtifactIndexKind.METADATA_INDEX_PLACEHOLDER
    lifecycle_status: ResearchArtifactIndexLifecycleStatus = ResearchArtifactIndexLifecycleStatus.PLACEHOLDER
    display_contract_skeleton_only: bool = True
    active_ui: bool = False
    frontend_component: bool = False
    desktop_widget: bool = False
    file_content_preview: bool = False
    indexed_artifact_records_present: bool = False
    search_results_present: bool = False
    ranking_results_present: bool = False
    retrieval_results_present: bool = False
    embeddings_present: bool = False
    vector_ids_present: bool = False
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
        return non_empty_text(value, "research artifact index display card text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def card_must_remain_placeholder(self) -> _IndexDisplayCardPlaceholderBase:
        if self.index_kind == ResearchArtifactIndexKind.UNKNOWN:
            raise ValueError("UNKNOWN index kind is not allowed in display card placeholders")
        if self.lifecycle_status == ResearchArtifactIndexLifecycleStatus.UNKNOWN:
            raise ValueError("UNKNOWN lifecycle status is not allowed in display card placeholders")
        if not self.display_contract_skeleton_only:
            raise ValueError("display card must remain display-contract-skeleton-only")
        dangerous_flags = {
            "active UI": self.active_ui,
            "frontend component": self.frontend_component,
            "desktop widget": self.desktop_widget,
            "file content preview": self.file_content_preview,
            "indexed artifact records": self.indexed_artifact_records_present,
            "search results": self.search_results_present,
            "ranking results": self.ranking_results_present,
            "retrieval results": self.retrieval_results_present,
            "embeddings": self.embeddings_present,
            "vector IDs": self.vector_ids_present,
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
            raise ValueError(f"Research Artifact Index display card placeholder cannot include: {', '.join(enabled)}")
        return self


class ResearchArtifactIndexCardPlaceholder(_IndexDisplayCardPlaceholderBase):
    subtitle: str | None = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def tags_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)


class ResearchArtifactIndexMetadataCardPlaceholder(_IndexDisplayCardPlaceholderBase):
    metadata_reference_id: str = "index-metadata-reference-placeholder"

    @field_validator("metadata_reference_id")
    @classmethod
    def metadata_reference_id_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index metadata card reference")


class ResearchArtifactIndexReferenceCardPlaceholder(_IndexDisplayCardPlaceholderBase):
    reference_id_placeholder: str = "index-reference-id-placeholder"
    source_label_placeholder: str | None = "source-label-placeholder"

    @field_validator("reference_id_placeholder")
    @classmethod
    def reference_id_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index reference card placeholder")


class ResearchArtifactIndexTagCardPlaceholder(_IndexDisplayCardPlaceholderBase):
    tag_kind: ResearchArtifactIndexTagKind = ResearchArtifactIndexTagKind.TOPIC
    tag_label_placeholder: str = "tag-label-placeholder"
    search_filter_enabled: bool = False
    ranking_weight_displayed: bool = False

    @field_validator("tag_label_placeholder")
    @classmethod
    def tag_label_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index tag card placeholder")

    @model_validator(mode="after")
    def tag_card_must_remain_inert(self) -> ResearchArtifactIndexTagCardPlaceholder:
        if self.tag_kind == ResearchArtifactIndexTagKind.UNKNOWN:
            raise ValueError("UNKNOWN tag kind is not allowed in display tag cards")
        if self.search_filter_enabled:
            raise ValueError("tag card placeholder cannot enable search filters")
        if self.ranking_weight_displayed:
            raise ValueError("tag card placeholder cannot display ranking weights")
        return self


def default_research_artifact_index_card_placeholder() -> ResearchArtifactIndexCardPlaceholder:
    return ResearchArtifactIndexCardPlaceholder(
        card_id="research-artifact-index-display-card-placeholder-v1",
        title="Research Artifact Index Card Placeholder",
        subtitle="Backend display contract metadata only.",
        tags=["display-contract-skeleton-only"],
        notes=["No active UI, index records, search, ranking, embeddings, preview, recommendation, or execution."],
    )


def default_research_artifact_index_metadata_card_placeholder() -> ResearchArtifactIndexMetadataCardPlaceholder:
    return ResearchArtifactIndexMetadataCardPlaceholder(
        card_id="research-artifact-index-display-metadata-card-placeholder-v1",
        title="Index Metadata Card Placeholder",
        notes=["Metadata display placeholder only; no indexed artifact record."],
    )


def default_research_artifact_index_reference_card_placeholder() -> ResearchArtifactIndexReferenceCardPlaceholder:
    return ResearchArtifactIndexReferenceCardPlaceholder(
        card_id="research-artifact-index-display-reference-card-placeholder-v1",
        title="Index Reference Card Placeholder",
        notes=["Reference display placeholder only; no registry lookup, index lookup, file read, or URL fetch."],
    )


def default_research_artifact_index_tag_card_placeholder() -> ResearchArtifactIndexTagCardPlaceholder:
    return ResearchArtifactIndexTagCardPlaceholder(
        card_id="research-artifact-index-display-tag-card-placeholder-v1",
        title="Index Tag Card Placeholder",
        notes=["Tag display placeholder only; no search filter, ranking weight, embedding, or vector-store behavior."],
    )

