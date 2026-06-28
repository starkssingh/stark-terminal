from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexForbiddenInteractionKind,
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class ResearchArtifactIndexApiSafetyResult(BaseModel):
    result_id: str
    safe: bool
    reasons: list[str]
    api_contract_skeleton_only: bool = True
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
        return non_empty_text(value, "research artifact index API safety result text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def safety_result_must_fail_closed(self) -> ResearchArtifactIndexApiSafetyResult:
        if not self.reasons:
            raise ValueError("Research Artifact Index API safety result requires reasons")
        if not self.api_contract_skeleton_only:
            raise ValueError("Research Artifact Index API safety result must remain contract-skeleton-only")
        dangerous_flags = {
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
            raise ValueError(f"Research Artifact Index API safety result cannot enable: {', '.join(enabled)}")
        return self


def research_artifact_index_api_forbidden_actions() -> list[ResearchArtifactIndexForbiddenInteractionKind]:
    return [
        ResearchArtifactIndexForbiddenInteractionKind.INDEXING_ENGINE,
        ResearchArtifactIndexForbiddenInteractionKind.SEARCH_ENGINE,
        ResearchArtifactIndexForbiddenInteractionKind.RANKING_ENGINE,
        ResearchArtifactIndexForbiddenInteractionKind.RETRIEVAL_ENGINE,
        ResearchArtifactIndexForbiddenInteractionKind.EMBEDDING_PIPELINE,
        ResearchArtifactIndexForbiddenInteractionKind.VECTOR_STORE,
        ResearchArtifactIndexForbiddenInteractionKind.SEMANTIC_SEARCH,
        ResearchArtifactIndexForbiddenInteractionKind.KEYWORD_SEARCH,
        ResearchArtifactIndexForbiddenInteractionKind.ACTIVE_INGESTION,
        ResearchArtifactIndexForbiddenInteractionKind.PERSISTENT_STORAGE,
        ResearchArtifactIndexForbiddenInteractionKind.FILE_UPLOAD,
        ResearchArtifactIndexForbiddenInteractionKind.FILE_DOWNLOAD,
        ResearchArtifactIndexForbiddenInteractionKind.FILE_PREVIEW,
        ResearchArtifactIndexForbiddenInteractionKind.PAPER_PARSING,
        ResearchArtifactIndexForbiddenInteractionKind.PDF_PARSING,
        ResearchArtifactIndexForbiddenInteractionKind.ARXIV_INGESTION,
        ResearchArtifactIndexForbiddenInteractionKind.LLM_PAPER_ANALYSIS,
        ResearchArtifactIndexForbiddenInteractionKind.METHOD_EXTRACTION,
        ResearchArtifactIndexForbiddenInteractionKind.STRATEGY_EXTRACTION,
        ResearchArtifactIndexForbiddenInteractionKind.STRATEGY_GENERATION,
        ResearchArtifactIndexForbiddenInteractionKind.STRATEGY_CODE_GENERATION,
        ResearchArtifactIndexForbiddenInteractionKind.BACKTESTING,
        ResearchArtifactIndexForbiddenInteractionKind.OPTIMIZATION,
        ResearchArtifactIndexForbiddenInteractionKind.RECOMMENDATION_GENERATION,
        ResearchArtifactIndexForbiddenInteractionKind.ACTION_GENERATION,
        ResearchArtifactIndexForbiddenInteractionKind.CONFIDENCE_SCORING,
        ResearchArtifactIndexForbiddenInteractionKind.DECISION_OBJECT_GENERATION,
        ResearchArtifactIndexForbiddenInteractionKind.READINESS_TO_TRADE,
        ResearchArtifactIndexForbiddenInteractionKind.BROKER_CONTROL,
        ResearchArtifactIndexForbiddenInteractionKind.EXECUTION,
    ]


def _assert_disabled(result_id: str, label: str, enabled: bool) -> ResearchArtifactIndexApiSafetyResult:
    if enabled:
        return ResearchArtifactIndexApiSafetyResult(
            result_id=result_id,
            safe=False,
            reasons=[f"{label} is forbidden for Research Artifact Index API contract skeleton."],
        )
    return ResearchArtifactIndexApiSafetyResult(
        result_id=result_id,
        safe=True,
        reasons=[f"{label} remains disabled for Research Artifact Index API contract skeleton."],
    )


def assert_no_index_api_indexing_engine_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-indexing-engine-v1", "indexing engine", enabled)


def assert_no_index_api_search_engine_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-search-engine-v1", "search engine", enabled)


def assert_no_index_api_ranking_engine_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-ranking-engine-v1", "ranking engine", enabled)


def assert_no_index_api_retrieval_engine_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-retrieval-engine-v1", "retrieval engine", enabled)


def assert_no_index_api_embeddings_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-embeddings-v1", "embeddings", enabled)


def assert_no_index_api_vector_store_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-vector-store-v1", "vector store", enabled)


def assert_no_index_api_ingestion_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-ingestion-v1", "active artifact ingestion", enabled)


def assert_no_index_api_file_uploads_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-file-uploads-v1", "file uploads", enabled)


def assert_no_index_api_file_downloads_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-file-downloads-v1", "file downloads", enabled)


def assert_no_index_api_file_previews_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-file-previews-v1", "file previews", enabled)


def assert_no_index_api_paper_parsing_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-paper-parsing-v1", "paper parsing", enabled)


def assert_no_index_api_strategy_generation_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-strategy-generation-v1", "strategy generation", enabled)


def assert_no_index_api_backtesting_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-backtesting-v1", "backtesting", enabled)


def assert_no_index_api_recommendation_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-recommendation-v1", "recommendations", enabled)


def assert_no_index_api_execution_enabled(enabled: bool = False) -> ResearchArtifactIndexApiSafetyResult:
    return _assert_disabled("research-artifact-index-api-no-execution-v1", "execution", enabled)
