from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_registry.interactions import (
    ResearchArtifactForbiddenInteraction,
    default_research_artifact_forbidden_interactions,
)
from stark_terminal_core.research_artifact_registry.types import (
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


class ResearchArtifactRegistrySafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_active_ingestion: bool = False
    allow_persistent_storage: bool = False
    allow_file_uploads: bool = False
    allow_file_downloads: bool = False
    allow_paper_parsing: bool = False
    allow_pdf_parsing: bool = False
    allow_arxiv_ingestion: bool = False
    allow_llm_analysis: bool = False
    allow_strategy_generation: bool = False
    allow_backtesting: bool = False
    allow_recommendations: bool = False
    allow_execution: bool = False
    require_planning_only: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact registry safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> ResearchArtifactRegistrySafetyPolicy:
        dangerous_flags = {
            "active ingestion": self.allow_active_ingestion,
            "persistent storage": self.allow_persistent_storage,
            "file uploads": self.allow_file_uploads,
            "file downloads": self.allow_file_downloads,
            "paper parsing": self.allow_paper_parsing,
            "PDF parsing": self.allow_pdf_parsing,
            "arXiv ingestion": self.allow_arxiv_ingestion,
            "LLM analysis": self.allow_llm_analysis,
            "strategy generation": self.allow_strategy_generation,
            "backtesting": self.allow_backtesting,
            "recommendations": self.allow_recommendations,
            "execution": self.allow_execution,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact registry safety policy cannot allow: {', '.join(enabled)}")
        if not self.require_planning_only:
            raise ValueError("research artifact registry safety policy must require planning-only posture")
        return self


class ResearchArtifactRegistrySafetyResult(BaseModel):
    result_id: str
    safe: bool
    reasons: list[str]
    planning_only: bool = True
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
        return non_empty_text(value, "research artifact registry safety result text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def result_must_fail_closed(self) -> ResearchArtifactRegistrySafetyResult:
        if not self.reasons:
            raise ValueError("research artifact registry safety result requires reasons")
        if not self.planning_only:
            raise ValueError("research artifact registry safety result must remain planning-only")
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
            raise ValueError(f"research artifact registry safety result cannot enable: {', '.join(enabled)}")
        return self


class ResearchArtifactRegistryUnavailableResponse(BaseModel):
    response_id: str
    unavailable: bool = True
    message: str
    planning_only: bool = True
    active_ingestion_enabled: bool = False
    persistent_storage_enabled: bool = False
    file_uploads_enabled: bool = False
    file_downloads_enabled: bool = False
    paper_parsing_enabled: bool = False
    strategy_generation_enabled: bool = False
    backtesting_enabled: bool = False
    recommendations_enabled: bool = False
    execution_enabled: bool = False
    broker_controls_enabled: bool = False
    readiness_to_trade_enabled: bool = False
    active_decision_objects_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact unavailable response text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> ResearchArtifactRegistryUnavailableResponse:
        if not self.unavailable:
            raise ValueError("research artifact unavailable response must remain unavailable")
        if not self.planning_only:
            raise ValueError("research artifact unavailable response must remain planning-only")
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
            "broker controls": self.broker_controls_enabled,
            "readiness-to-trade": self.readiness_to_trade_enabled,
            "active DecisionObjects": self.active_decision_objects_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact unavailable response cannot enable: {', '.join(enabled)}")
        return self


def default_research_artifact_registry_safety_policy(settings: object | None = None) -> ResearchArtifactRegistrySafetyPolicy:
    schema_version = getattr(settings, "research_artifact_registry_schema_version", "v1")
    return ResearchArtifactRegistrySafetyPolicy(
        policy_id="research-artifact-registry-safety-policy-v1",
        name="Research Artifact Registry planning-only safety policy",
        schema_version=schema_version,
        notes=[
            "No active ingestion, storage, parsing, strategy generation, backtesting, recommendations, or execution.",
        ],
    )


def forbidden_interactions() -> list[ResearchArtifactForbiddenInteraction]:
    return default_research_artifact_forbidden_interactions()


def unavailable_response_template() -> ResearchArtifactRegistryUnavailableResponse:
    return ResearchArtifactRegistryUnavailableResponse(
        response_id="research-artifact-registry-unavailable-template-v1",
        message=(
            "Research Artifact Registry is planning-only; ingestion, storage, parsing, "
            "strategy generation, backtesting, recommendations, and execution are unavailable."
        ),
        notes=["Prompt 70 returns unavailable placeholder metadata only."],
    )


def _assert_disabled(result_id: str, label: str, enabled: bool) -> ResearchArtifactRegistrySafetyResult:
    if enabled:
        return ResearchArtifactRegistrySafetyResult(
            result_id=result_id,
            safe=False,
            reasons=[f"{label} is forbidden for Research Artifact Registry planning."],
        )
    return ResearchArtifactRegistrySafetyResult(
        result_id=result_id,
        safe=True,
        reasons=[f"{label} remains disabled for Research Artifact Registry planning."],
    )


def assert_no_artifact_ingestion_enabled(enabled: bool = False) -> ResearchArtifactRegistrySafetyResult:
    return _assert_disabled("research-artifact-no-active-ingestion-v1", "active artifact ingestion", enabled)


def assert_no_paper_parsing_enabled(enabled: bool = False) -> ResearchArtifactRegistrySafetyResult:
    return _assert_disabled("research-artifact-no-paper-parsing-v1", "paper parsing", enabled)


def assert_no_strategy_generation_enabled(enabled: bool = False) -> ResearchArtifactRegistrySafetyResult:
    return _assert_disabled("research-artifact-no-strategy-generation-v1", "strategy generation", enabled)


def assert_no_backtesting_enabled(enabled: bool = False) -> ResearchArtifactRegistrySafetyResult:
    return _assert_disabled("research-artifact-no-backtesting-v1", "backtesting", enabled)


def assert_no_recommendation_enabled(enabled: bool = False) -> ResearchArtifactRegistrySafetyResult:
    return _assert_disabled("research-artifact-no-recommendation-v1", "recommendations", enabled)


def assert_no_execution_enabled(enabled: bool = False) -> ResearchArtifactRegistrySafetyResult:
    return _assert_disabled("research-artifact-no-execution-v1", "execution", enabled)

