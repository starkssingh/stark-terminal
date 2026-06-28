from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactIndexDisplayForbiddenAction(StrEnum):
    ACTIVE_UI = "ACTIVE_UI"
    FRONTEND_COMPONENT = "FRONTEND_COMPONENT"
    DESKTOP_COMPONENT = "DESKTOP_COMPONENT"
    INDEXING_ENGINE = "INDEXING_ENGINE"
    SEARCH_ENGINE = "SEARCH_ENGINE"
    RANKING_ENGINE = "RANKING_ENGINE"
    RETRIEVAL_ENGINE = "RETRIEVAL_ENGINE"
    EMBEDDING_PIPELINE = "EMBEDDING_PIPELINE"
    VECTOR_STORE = "VECTOR_STORE"
    SEMANTIC_SEARCH = "SEMANTIC_SEARCH"
    KEYWORD_SEARCH = "KEYWORD_SEARCH"
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


class ResearchArtifactIndexDisplaySafetyResult(BaseModel):
    result_id: str
    safe: bool
    reasons: list[str]
    display_contract_skeleton_only: bool = True
    active_ui_enabled: bool = False
    frontend_components_enabled: bool = False
    desktop_components_enabled: bool = False
    indexing_engine_enabled: bool = False
    search_engine_enabled: bool = False
    ranking_engine_enabled: bool = False
    retrieval_engine_enabled: bool = False
    embeddings_enabled: bool = False
    vector_store_enabled: bool = False
    active_ingestion_enabled: bool = False
    persistent_storage_enabled: bool = False
    file_uploads_enabled: bool = False
    file_downloads_enabled: bool = False
    file_previews_enabled: bool = False
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
        return non_empty_text(value, "research artifact index display safety result text fields")

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
    def safety_result_must_fail_closed(self) -> ResearchArtifactIndexDisplaySafetyResult:
        if not self.display_contract_skeleton_only:
            raise ValueError("display safety result must remain display-contract-skeleton-only")
        dangerous_flags = {
            "active UI": self.active_ui_enabled,
            "frontend components": self.frontend_components_enabled,
            "desktop components": self.desktop_components_enabled,
            "indexing engine": self.indexing_engine_enabled,
            "search engine": self.search_engine_enabled,
            "ranking engine": self.ranking_engine_enabled,
            "retrieval engine": self.retrieval_engine_enabled,
            "embeddings": self.embeddings_enabled,
            "vector store": self.vector_store_enabled,
            "active ingestion": self.active_ingestion_enabled,
            "persistent storage": self.persistent_storage_enabled,
            "file uploads": self.file_uploads_enabled,
            "file downloads": self.file_downloads_enabled,
            "file previews": self.file_previews_enabled,
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


def research_artifact_index_display_forbidden_actions() -> list[ResearchArtifactIndexDisplayForbiddenAction]:
    return list(ResearchArtifactIndexDisplayForbiddenAction)


def _assert_disabled(result_id: str, label: str, enabled: bool) -> ResearchArtifactIndexDisplaySafetyResult:
    if enabled:
        return ResearchArtifactIndexDisplaySafetyResult(
            result_id=result_id,
            safe=False,
            reasons=[f"{label} is forbidden for Research Artifact Index Display contract skeleton."],
        )
    return ResearchArtifactIndexDisplaySafetyResult(
        result_id=result_id,
        safe=True,
        reasons=[f"{label} remains disabled for Research Artifact Index Display contract skeleton."],
    )


def assert_no_index_display_active_ui_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-active-ui-v1", "active UI", enabled)


def assert_no_index_display_frontend_components_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-frontend-components-v1", "frontend components", enabled)


def assert_no_index_display_desktop_components_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-desktop-components-v1", "desktop components", enabled)


def assert_no_index_display_indexing_engine_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-indexing-engine-v1", "indexing engine", enabled)


def assert_no_index_display_search_engine_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-search-engine-v1", "search engine", enabled)


def assert_no_index_display_ranking_engine_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-ranking-engine-v1", "ranking engine", enabled)


def assert_no_index_display_retrieval_engine_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-retrieval-engine-v1", "retrieval engine", enabled)


def assert_no_index_display_embeddings_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-embeddings-v1", "embeddings", enabled)


def assert_no_index_display_vector_store_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-vector-store-v1", "vector store", enabled)


def assert_no_index_display_ingestion_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-ingestion-v1", "active artifact ingestion", enabled)


def assert_no_index_display_file_uploads_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-file-uploads-v1", "file uploads", enabled)


def assert_no_index_display_file_downloads_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-file-downloads-v1", "file downloads", enabled)


def assert_no_index_display_file_previews_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-file-previews-v1", "file previews", enabled)


def assert_no_index_display_paper_parsing_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-paper-parsing-v1", "paper parsing", enabled)


def assert_no_index_display_strategy_generation_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-strategy-generation-v1", "strategy generation", enabled)


def assert_no_index_display_backtesting_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-backtesting-v1", "backtesting", enabled)


def assert_no_index_display_recommendation_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-recommendation-v1", "recommendations", enabled)


def assert_no_index_display_execution_enabled(enabled: bool = False) -> ResearchArtifactIndexDisplaySafetyResult:
    return _assert_disabled("research-artifact-index-display-no-execution-v1", "execution", enabled)

