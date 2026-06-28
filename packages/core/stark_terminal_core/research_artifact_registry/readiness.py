from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactRegistryReadinessReport(BaseModel):
    registry_planning_ready: bool
    active_ingestion_enabled: bool = False
    persistent_storage_enabled: bool = False
    file_uploads_enabled: bool = False
    file_downloads_enabled: bool = False
    paper_parsing_enabled: bool = False
    strategy_generation_enabled: bool = False
    backtesting_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    next_allowed_phase: str = "api_contract_skeleton"
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("next_allowed_phase", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact registry readiness text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def readiness_must_be_planning_only(self) -> ResearchArtifactRegistryReadinessReport:
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
            raise ValueError(f"research artifact registry readiness cannot enable: {', '.join(enabled)}")
        if self.next_allowed_phase != "api_contract_skeleton":
            raise ValueError("Research Artifact Registry next phase must be api_contract_skeleton")
        return self


def research_artifact_registry_readiness(settings: object | None = None) -> ResearchArtifactRegistryReadinessReport:
    schema_version = getattr(settings, "research_artifact_registry_schema_version", "v1")
    return ResearchArtifactRegistryReadinessReport(
        registry_planning_ready=True,
        schema_version=schema_version,
    )

