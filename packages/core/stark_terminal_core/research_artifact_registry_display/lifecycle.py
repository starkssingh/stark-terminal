from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactLifecycleStatus,
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactLifecycleDisplayPlaceholder(BaseModel):
    lifecycle_display_id: str
    artifact_id_placeholder: str = "artifact-id-placeholder"
    status: ResearchArtifactLifecycleStatus = ResearchArtifactLifecycleStatus.PLACEHOLDER
    display_contract_skeleton_only: bool = True
    validated_strategy: bool = False
    approved_strategy: bool = False
    recommended_strategy: bool = False
    backtested_strategy: bool = False
    readiness_to_trade: bool = False
    execution_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("lifecycle_display_id", "artifact_id_placeholder", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact lifecycle display placeholder text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def lifecycle_display_must_fail_closed(self) -> ResearchArtifactLifecycleDisplayPlaceholder:
        if self.status == ResearchArtifactLifecycleStatus.UNKNOWN:
            raise ValueError("UNKNOWN lifecycle status is not allowed in display placeholders")
        if not self.display_contract_skeleton_only:
            raise ValueError("lifecycle display must remain display-contract-skeleton-only")
        dangerous_flags = {
            "validated strategy": self.validated_strategy,
            "approved strategy": self.approved_strategy,
            "recommended strategy": self.recommended_strategy,
            "backtested strategy": self.backtested_strategy,
            "readiness-to-trade": self.readiness_to_trade,
            "execution-ready": self.execution_ready,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"lifecycle display placeholder cannot imply: {', '.join(enabled)}")
        return self


def default_research_artifact_lifecycle_display_placeholder() -> ResearchArtifactLifecycleDisplayPlaceholder:
    return ResearchArtifactLifecycleDisplayPlaceholder(
        lifecycle_display_id="research-artifact-lifecycle-display-placeholder-v1",
    )
