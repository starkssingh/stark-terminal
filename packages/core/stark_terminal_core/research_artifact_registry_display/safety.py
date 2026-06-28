from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactRegistryDisplayForbiddenAction(StrEnum):
    ACTIVE_UI = "ACTIVE_UI"
    FRONTEND_COMPONENT = "FRONTEND_COMPONENT"
    DESKTOP_COMPONENT = "DESKTOP_COMPONENT"
    ACTIVE_INGESTION = "ACTIVE_INGESTION"
    PERSISTENT_STORAGE = "PERSISTENT_STORAGE"
    FILE_PREVIEW = "FILE_PREVIEW"
    FILE_UPLOAD = "FILE_UPLOAD"
    FILE_DOWNLOAD = "FILE_DOWNLOAD"
    PAPER_INGESTION = "PAPER_INGESTION"
    PAPER_PARSING = "PAPER_PARSING"
    PDF_PARSING = "PDF_PARSING"
    ARXIV_INGESTION = "ARXIV_INGESTION"
    LLM_ANALYSIS = "LLM_ANALYSIS"
    METHOD_EXTRACTION = "METHOD_EXTRACTION"
    STRATEGY_EXTRACTION = "STRATEGY_EXTRACTION"
    STRATEGY_GENERATION = "STRATEGY_GENERATION"
    STRATEGY_CODE_GENERATION = "STRATEGY_CODE_GENERATION"
    BACKTESTING = "BACKTESTING"
    OPTIMIZATION = "OPTIMIZATION"
    RECOMMENDATION_GENERATION = "RECOMMENDATION_GENERATION"
    ACTION_GENERATION = "ACTION_GENERATION"
    CONFIDENCE_SCORING = "CONFIDENCE_SCORING"
    DECISION_OBJECT_GENERATION = "DECISION_OBJECT_GENERATION"
    READINESS_TO_TRADE = "READINESS_TO_TRADE"
    BROKER_CONTROL = "BROKER_CONTROL"
    EXECUTION = "EXECUTION"


class ResearchArtifactRegistryDisplaySafetyResult(BaseModel):
    result_id: str
    safe: bool
    reasons: list[str]
    display_contract_skeleton_only: bool = True
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
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("result_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact registry display safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("display safety result requires reasons")
        return value

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def safety_result_must_fail_closed(self) -> ResearchArtifactRegistryDisplaySafetyResult:
        if not self.display_contract_skeleton_only:
            raise ValueError("display safety result must remain display-contract-skeleton-only")
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
            raise ValueError(f"display safety result cannot enable: {', '.join(enabled)}")
        return self


def research_artifact_registry_display_forbidden_actions() -> list[ResearchArtifactRegistryDisplayForbiddenAction]:
    return [
        ResearchArtifactRegistryDisplayForbiddenAction.ACTIVE_UI,
        ResearchArtifactRegistryDisplayForbiddenAction.FRONTEND_COMPONENT,
        ResearchArtifactRegistryDisplayForbiddenAction.DESKTOP_COMPONENT,
        ResearchArtifactRegistryDisplayForbiddenAction.ACTIVE_INGESTION,
        ResearchArtifactRegistryDisplayForbiddenAction.PERSISTENT_STORAGE,
        ResearchArtifactRegistryDisplayForbiddenAction.FILE_PREVIEW,
        ResearchArtifactRegistryDisplayForbiddenAction.FILE_UPLOAD,
        ResearchArtifactRegistryDisplayForbiddenAction.FILE_DOWNLOAD,
        ResearchArtifactRegistryDisplayForbiddenAction.PAPER_INGESTION,
        ResearchArtifactRegistryDisplayForbiddenAction.PAPER_PARSING,
        ResearchArtifactRegistryDisplayForbiddenAction.PDF_PARSING,
        ResearchArtifactRegistryDisplayForbiddenAction.ARXIV_INGESTION,
        ResearchArtifactRegistryDisplayForbiddenAction.LLM_ANALYSIS,
        ResearchArtifactRegistryDisplayForbiddenAction.METHOD_EXTRACTION,
        ResearchArtifactRegistryDisplayForbiddenAction.STRATEGY_EXTRACTION,
        ResearchArtifactRegistryDisplayForbiddenAction.STRATEGY_GENERATION,
        ResearchArtifactRegistryDisplayForbiddenAction.STRATEGY_CODE_GENERATION,
        ResearchArtifactRegistryDisplayForbiddenAction.BACKTESTING,
        ResearchArtifactRegistryDisplayForbiddenAction.OPTIMIZATION,
        ResearchArtifactRegistryDisplayForbiddenAction.RECOMMENDATION_GENERATION,
        ResearchArtifactRegistryDisplayForbiddenAction.ACTION_GENERATION,
        ResearchArtifactRegistryDisplayForbiddenAction.CONFIDENCE_SCORING,
        ResearchArtifactRegistryDisplayForbiddenAction.DECISION_OBJECT_GENERATION,
        ResearchArtifactRegistryDisplayForbiddenAction.READINESS_TO_TRADE,
        ResearchArtifactRegistryDisplayForbiddenAction.BROKER_CONTROL,
        ResearchArtifactRegistryDisplayForbiddenAction.EXECUTION,
    ]


def _assert_disabled(result_id: str, label: str, enabled: bool) -> ResearchArtifactRegistryDisplaySafetyResult:
    if enabled:
        return ResearchArtifactRegistryDisplaySafetyResult(
            result_id=result_id,
            safe=False,
            reasons=[f"{label} is forbidden for Research Artifact Registry Display contract skeleton."],
        )
    return ResearchArtifactRegistryDisplaySafetyResult(
        result_id=result_id,
        safe=True,
        reasons=[f"{label} remains disabled for Research Artifact Registry Display contract skeleton."],
    )


def assert_no_display_active_ui_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-active-ui-v1", "active UI", enabled)


def assert_no_display_frontend_components_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-frontend-components-v1", "frontend components", enabled)


def assert_no_display_desktop_components_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-desktop-components-v1", "desktop components", enabled)


def assert_no_display_ingestion_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-ingestion-v1", "active artifact ingestion", enabled)


def assert_no_display_file_uploads_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-file-uploads-v1", "file uploads", enabled)


def assert_no_display_file_downloads_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-file-downloads-v1", "file downloads", enabled)


def assert_no_display_paper_parsing_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-paper-parsing-v1", "paper parsing", enabled)


def assert_no_display_strategy_generation_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-strategy-generation-v1", "strategy generation", enabled)


def assert_no_display_backtesting_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-backtesting-v1", "backtesting", enabled)


def assert_no_display_recommendation_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-recommendation-v1", "recommendations", enabled)


def assert_no_display_execution_enabled(enabled: bool = False) -> ResearchArtifactRegistryDisplaySafetyResult:
    return _assert_disabled("research-artifact-display-no-execution-v1", "execution", enabled)
