from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactForbiddenInteractionKind,
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactRegistryApiSafetyResult(BaseModel):
    result_id: str
    safe: bool
    reasons: list[str]
    api_contract_skeleton_only: bool = True
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
        return non_empty_text(value, "research artifact registry API safety result text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def safety_result_must_fail_closed(self) -> ResearchArtifactRegistryApiSafetyResult:
        if not self.reasons:
            raise ValueError("API safety result requires reasons")
        if not self.api_contract_skeleton_only:
            raise ValueError("API safety result must remain contract-skeleton-only")
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
            raise ValueError(f"API safety result cannot enable: {', '.join(enabled)}")
        return self


def research_artifact_registry_api_forbidden_actions() -> list[ResearchArtifactForbiddenInteractionKind]:
    return [
        ResearchArtifactForbiddenInteractionKind.ACTIVE_INGESTION,
        ResearchArtifactForbiddenInteractionKind.PERSISTENT_STORAGE,
        ResearchArtifactForbiddenInteractionKind.FILE_UPLOAD,
        ResearchArtifactForbiddenInteractionKind.FILE_DOWNLOAD,
        ResearchArtifactForbiddenInteractionKind.PAPER_INGESTION,
        ResearchArtifactForbiddenInteractionKind.PAPER_PARSING,
        ResearchArtifactForbiddenInteractionKind.PDF_PARSING,
        ResearchArtifactForbiddenInteractionKind.ARXIV_INGESTION,
        ResearchArtifactForbiddenInteractionKind.LLM_ANALYSIS,
        ResearchArtifactForbiddenInteractionKind.METHOD_EXTRACTION,
        ResearchArtifactForbiddenInteractionKind.STRATEGY_EXTRACTION,
        ResearchArtifactForbiddenInteractionKind.STRATEGY_GENERATION,
        ResearchArtifactForbiddenInteractionKind.STRATEGY_CODE_GENERATION,
        ResearchArtifactForbiddenInteractionKind.BACKTESTING,
        ResearchArtifactForbiddenInteractionKind.OPTIMIZATION,
        ResearchArtifactForbiddenInteractionKind.RECOMMENDATION_GENERATION,
        ResearchArtifactForbiddenInteractionKind.ACTION_GENERATION,
        ResearchArtifactForbiddenInteractionKind.CONFIDENCE_SCORING,
        ResearchArtifactForbiddenInteractionKind.DECISION_OBJECT_GENERATION,
        ResearchArtifactForbiddenInteractionKind.READINESS_TO_TRADE,
        ResearchArtifactForbiddenInteractionKind.BROKER_CONTROL,
        ResearchArtifactForbiddenInteractionKind.APPROVAL_CONTROL,
        ResearchArtifactForbiddenInteractionKind.OVERRIDE_CONTROL,
        ResearchArtifactForbiddenInteractionKind.EXECUTION,
        ResearchArtifactForbiddenInteractionKind.EXTERNAL_CALL,
        ResearchArtifactForbiddenInteractionKind.DATABASE_WRITE,
        ResearchArtifactForbiddenInteractionKind.OBJECT_STORAGE_WRITE,
    ]


def _assert_disabled(result_id: str, label: str, enabled: bool) -> ResearchArtifactRegistryApiSafetyResult:
    if enabled:
        return ResearchArtifactRegistryApiSafetyResult(
            result_id=result_id,
            safe=False,
            reasons=[f"{label} is forbidden for Research Artifact Registry API contract skeleton."],
        )
    return ResearchArtifactRegistryApiSafetyResult(
        result_id=result_id,
        safe=True,
        reasons=[f"{label} remains disabled for Research Artifact Registry API contract skeleton."],
    )


def assert_no_api_ingestion_enabled(enabled: bool = False) -> ResearchArtifactRegistryApiSafetyResult:
    return _assert_disabled("research-artifact-api-no-ingestion-v1", "active artifact ingestion", enabled)


def assert_no_api_file_uploads_enabled(enabled: bool = False) -> ResearchArtifactRegistryApiSafetyResult:
    return _assert_disabled("research-artifact-api-no-file-uploads-v1", "file uploads", enabled)


def assert_no_api_file_downloads_enabled(enabled: bool = False) -> ResearchArtifactRegistryApiSafetyResult:
    return _assert_disabled("research-artifact-api-no-file-downloads-v1", "file downloads", enabled)


def assert_no_api_paper_parsing_enabled(enabled: bool = False) -> ResearchArtifactRegistryApiSafetyResult:
    return _assert_disabled("research-artifact-api-no-paper-parsing-v1", "paper parsing", enabled)


def assert_no_api_strategy_generation_enabled(enabled: bool = False) -> ResearchArtifactRegistryApiSafetyResult:
    return _assert_disabled("research-artifact-api-no-strategy-generation-v1", "strategy generation", enabled)


def assert_no_api_backtesting_enabled(enabled: bool = False) -> ResearchArtifactRegistryApiSafetyResult:
    return _assert_disabled("research-artifact-api-no-backtesting-v1", "backtesting", enabled)


def assert_no_api_recommendation_enabled(enabled: bool = False) -> ResearchArtifactRegistryApiSafetyResult:
    return _assert_disabled("research-artifact-api-no-recommendation-v1", "recommendations", enabled)


def assert_no_api_execution_enabled(enabled: bool = False) -> ResearchArtifactRegistryApiSafetyResult:
    return _assert_disabled("research-artifact-api-no-execution-v1", "execution", enabled)
