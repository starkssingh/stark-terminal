from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactRegistryApiUnavailableResponse(BaseModel):
    unavailable: bool = True
    reason: str
    allowed_stage: str = "api_contract_skeleton"
    active_ingestion_enabled: bool = False
    persistent_storage_enabled: bool = False
    file_uploads_enabled: bool = False
    file_downloads_enabled: bool = False
    paper_parsing_enabled: bool = False
    strategy_generation_enabled: bool = False
    backtesting_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("reason", "allowed_stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact registry API unavailable response text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> ResearchArtifactRegistryApiUnavailableResponse:
        if not self.unavailable:
            raise ValueError("Research Artifact Registry API unavailable response must remain unavailable")
        if self.allowed_stage != "api_contract_skeleton":
            raise ValueError("Research Artifact Registry API unavailable response stage must be api_contract_skeleton")
        dangerous_flags = {
            "active ingestion": self.active_ingestion_enabled,
            "persistent storage": self.persistent_storage_enabled,
            "file uploads": self.file_uploads_enabled,
            "file downloads": self.file_downloads_enabled,
            "paper parsing": self.paper_parsing_enabled,
            "strategy generation": self.strategy_generation_enabled,
            "backtesting": self.backtesting_enabled,
            "recommendations": self.recommendations_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"Research Artifact Registry API unavailable response cannot enable: {', '.join(enabled)}")
        return self


def unavailable_response_template() -> ResearchArtifactRegistryApiUnavailableResponse:
    return ResearchArtifactRegistryApiUnavailableResponse(
        reason=(
            "Research Artifact Registry API is a read-only contract skeleton; ingestion, storage, "
            "upload/download, parsing, strategy generation, backtesting, recommendations, and execution are unavailable."
        ),
    )
