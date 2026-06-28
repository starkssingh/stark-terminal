from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactDisplayBadgeMeaning(StrEnum):
    PLACEHOLDER = "PLACEHOLDER"
    REFERENCED = "REFERENCED"
    DRAFT = "DRAFT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class _BadgePlaceholderBase(BaseModel):
    badge_id: str
    meaning: ResearchArtifactDisplayBadgeMeaning = ResearchArtifactDisplayBadgeMeaning.PLACEHOLDER
    label: str
    display_contract_skeleton_only: bool = True
    active_ui: bool = False
    recommendation_ready: bool = False
    backtest_ready: bool = False
    readiness_to_trade: bool = False
    broker_control: bool = False
    execution_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("badge_id", "label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact display badge text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def badge_must_fail_closed(self) -> _BadgePlaceholderBase:
        if self.meaning == ResearchArtifactDisplayBadgeMeaning.UNKNOWN:
            raise ValueError("UNKNOWN badge meaning is not allowed in active display placeholders")
        if not self.display_contract_skeleton_only:
            raise ValueError("badge placeholder must remain display-contract-skeleton-only")
        dangerous_flags = {
            "active UI": self.active_ui,
            "recommendation-ready": self.recommendation_ready,
            "backtest-ready": self.backtest_ready,
            "readiness-to-trade": self.readiness_to_trade,
            "broker control": self.broker_control,
            "execution-ready": self.execution_ready,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"badge placeholder cannot imply: {', '.join(enabled)}")
        return self


class ResearchArtifactLifecycleBadgePlaceholder(_BadgePlaceholderBase):
    pass


class ResearchArtifactSafetyBadgePlaceholder(_BadgePlaceholderBase):
    unavailable: bool = True

    @model_validator(mode="after")
    def safety_badge_must_remain_unavailable(self) -> ResearchArtifactSafetyBadgePlaceholder:
        if not self.unavailable:
            raise ValueError("safety badge placeholder must remain unavailable")
        return self


def default_research_artifact_lifecycle_badge_placeholder() -> ResearchArtifactLifecycleBadgePlaceholder:
    return ResearchArtifactLifecycleBadgePlaceholder(
        badge_id="research-artifact-lifecycle-badge-placeholder-v1",
        label="Placeholder",
    )


def default_research_artifact_safety_badge_placeholder() -> ResearchArtifactSafetyBadgePlaceholder:
    return ResearchArtifactSafetyBadgePlaceholder(
        badge_id="research-artifact-safety-badge-placeholder-v1",
        label="Display contract only",
        meaning=ResearchArtifactDisplayBadgeMeaning.UNAVAILABLE,
    )
