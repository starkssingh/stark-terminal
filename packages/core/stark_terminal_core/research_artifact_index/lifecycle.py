from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexLifecycleStatus,
    SAFE_INDEX_LIFECYCLE_STATUSES,
    non_empty_text,
    normalize_datetime,
    optional_text,
    utc_now,
)


class ResearchArtifactIndexLifecyclePlaceholder(BaseModel):
    lifecycle_id: str
    index_id: str
    status: ResearchArtifactIndexLifecycleStatus
    allowed_next_statuses: list[ResearchArtifactIndexLifecycleStatus]
    blocked_reason: str | None = None
    schema_version: str = "v1"
    planning_only: bool = True
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("lifecycle_id", "index_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index lifecycle placeholder text fields")

    @field_validator("blocked_reason")
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        return optional_text(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def lifecycle_must_not_imply_active_index_or_trade(self) -> ResearchArtifactIndexLifecyclePlaceholder:
        if not self.planning_only:
            raise ValueError("research artifact index lifecycle must remain planning-only")
        if self.status == ResearchArtifactIndexLifecycleStatus.UNKNOWN:
            raise ValueError("UNKNOWN lifecycle status is not allowed")
        if self.status not in SAFE_INDEX_LIFECYCLE_STATUSES:
            raise ValueError("research artifact index lifecycle status is not allowed in Prompt 77")
        if not self.allowed_next_statuses:
            raise ValueError("research artifact index lifecycle requires allowed_next_statuses")
        unsafe_statuses = [
            status
            for status in self.allowed_next_statuses
            if status == ResearchArtifactIndexLifecycleStatus.UNKNOWN or status not in SAFE_INDEX_LIFECYCLE_STATUSES
        ]
        if unsafe_statuses:
            raise ValueError("allowed_next_statuses contains unsafe lifecycle status")
        searchable = " ".join([self.status.value, *[status.value for status in self.allowed_next_statuses]]).lower()
        forbidden_terms = {
            "indexed",
            "searchable",
            "ranked",
            "embedded",
            "retrieved",
            "validated_strategy",
            "recommendation",
            "readiness_to_trade",
            "execution",
        }
        if any(term in searchable for term in forbidden_terms):
            raise ValueError("research artifact index lifecycle cannot imply active index or trading readiness")
        return self


def default_research_artifact_index_lifecycle_placeholders() -> list[ResearchArtifactIndexLifecyclePlaceholder]:
    return [
        ResearchArtifactIndexLifecyclePlaceholder(
            lifecycle_id="research-artifact-index-placeholder-lifecycle-v1",
            index_id="research-artifact-index-metadata-placeholder-v1",
            status=ResearchArtifactIndexLifecycleStatus.PLACEHOLDER,
            allowed_next_statuses=[
                ResearchArtifactIndexLifecycleStatus.REFERENCED,
                ResearchArtifactIndexLifecycleStatus.REVIEW_REQUIRED,
                ResearchArtifactIndexLifecycleStatus.BLOCKED,
            ],
            blocked_reason="Indexing, search, ranking, embeddings, storage, and execution remain forbidden.",
        ),
        ResearchArtifactIndexLifecyclePlaceholder(
            lifecycle_id="research-artifact-index-deferred-lifecycle-v1",
            index_id="research-artifact-index-key-placeholder-v1",
            status=ResearchArtifactIndexLifecycleStatus.DEFERRED,
            allowed_next_statuses=[
                ResearchArtifactIndexLifecycleStatus.REVIEW_REQUIRED,
                ResearchArtifactIndexLifecycleStatus.BLOCKED,
            ],
            blocked_reason="Future API contract skeleton must come before implementation.",
        ),
    ]
