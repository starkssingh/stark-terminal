from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactRegistryDisplayContract(BaseModel):
    contract_id: str
    service: str = "stark-terminal-research-artifact-registry-display"
    stage: str = "display_contract_skeleton"
    schema_version: str = "v1"
    read_only: bool = True
    unavailable_by_default: bool = True
    active_ui_enabled: bool = False
    frontend_components_enabled: bool = False
    desktop_components_enabled: bool = False
    active_ingestion_enabled: bool = False
    persistent_storage_enabled: bool = False
    file_uploads_enabled: bool = False
    file_downloads_enabled: bool = False
    paper_parsing_enabled: bool = False
    strategy_generation_enabled: bool = False
    backtesting_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("contract_id", "service", "stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact registry display contract text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def contract_must_fail_closed(self) -> ResearchArtifactRegistryDisplayContract:
        if self.stage != "display_contract_skeleton":
            raise ValueError("Research Artifact Registry Display contract stage must be display_contract_skeleton")
        if not self.read_only:
            raise ValueError("Research Artifact Registry Display contract must be read-only")
        if not self.unavailable_by_default:
            raise ValueError("Research Artifact Registry Display contract must be unavailable by default")
        dangerous_flags = {
            "active UI": self.active_ui_enabled,
            "frontend components": self.frontend_components_enabled,
            "desktop components": self.desktop_components_enabled,
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
            raise ValueError(f"Research Artifact Registry Display contract cannot enable: {', '.join(enabled)}")
        return self


def default_research_artifact_registry_display_contract() -> ResearchArtifactRegistryDisplayContract:
    return ResearchArtifactRegistryDisplayContract(
        contract_id="research-artifact-registry-display-contract-v1",
    )
