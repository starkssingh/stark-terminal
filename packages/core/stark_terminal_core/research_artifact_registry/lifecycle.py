from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactLifecycleStatus,
    SAFE_LIFECYCLE_STATUSES,
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactLifecyclePlaceholder(BaseModel):
    lifecycle_id: str
    artifact_id: str
    status: ResearchArtifactLifecycleStatus
    allowed_next_statuses: list[ResearchArtifactLifecycleStatus]
    blocked_reason: str | None = None
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("lifecycle_id", "artifact_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact lifecycle placeholder text fields")

    @field_validator("blocked_reason")
    @classmethod
    def optional_text_fields_must_be_stripped(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def lifecycle_must_not_imply_trading_readiness(self) -> ResearchArtifactLifecyclePlaceholder:
        if self.status == ResearchArtifactLifecycleStatus.UNKNOWN:
            raise ValueError("UNKNOWN lifecycle status is not allowed")
        if self.status not in SAFE_LIFECYCLE_STATUSES:
            raise ValueError("research artifact lifecycle status is not allowed in Prompt 70")
        if not self.allowed_next_statuses:
            raise ValueError("research artifact lifecycle placeholders require allowed_next_statuses")
        unsafe_statuses = [
            status for status in self.allowed_next_statuses
            if status == ResearchArtifactLifecycleStatus.UNKNOWN or status not in SAFE_LIFECYCLE_STATUSES
        ]
        if unsafe_statuses:
            raise ValueError("allowed_next_statuses contains unsafe lifecycle status")
        searchable = " ".join(
            [self.status.value, *[status.value for status in self.allowed_next_statuses]]
        ).lower()
        forbidden_terms = {
            "approved",
            "validated strategy",
            "recommendation",
            "readiness-to-trade",
            "ready_to_trade",
            "execution",
        }
        if any(term in searchable for term in forbidden_terms):
            raise ValueError("research artifact lifecycle cannot imply strategy approval or execution")
        return self


def default_research_artifact_lifecycle_placeholders() -> list[ResearchArtifactLifecyclePlaceholder]:
    return [
        ResearchArtifactLifecyclePlaceholder(
            lifecycle_id="research-artifact-placeholder-lifecycle-v1",
            artifact_id="research-artifact-paper-reference-placeholder-v1",
            status=ResearchArtifactLifecycleStatus.PLACEHOLDER,
            allowed_next_statuses=[
                ResearchArtifactLifecycleStatus.REFERENCED,
                ResearchArtifactLifecycleStatus.REVIEW_REQUIRED,
                ResearchArtifactLifecycleStatus.BLOCKED,
            ],
            blocked_reason="Active ingestion, parsing, strategy generation, and execution remain forbidden.",
        ),
        ResearchArtifactLifecyclePlaceholder(
            lifecycle_id="research-artifact-draft-lifecycle-v1",
            artifact_id="research-artifact-hypothesis-reference-placeholder-v1",
            status=ResearchArtifactLifecycleStatus.DRAFT,
            allowed_next_statuses=[
                ResearchArtifactLifecycleStatus.REVIEW_REQUIRED,
                ResearchArtifactLifecycleStatus.DEFERRED,
                ResearchArtifactLifecycleStatus.BLOCKED,
            ],
            blocked_reason="Hypotheses remain planning placeholders, not generated strategies.",
        ),
        ResearchArtifactLifecyclePlaceholder(
            lifecycle_id="research-artifact-blocked-lifecycle-v1",
            artifact_id="research-artifact-backtest-reference-placeholder-v1",
            status=ResearchArtifactLifecycleStatus.BLOCKED,
            allowed_next_statuses=[
                ResearchArtifactLifecycleStatus.DEFERRED,
                ResearchArtifactLifecycleStatus.REVIEW_REQUIRED,
            ],
            blocked_reason="Backtest placeholders cannot become results in Prompt 70.",
        ),
    ]
