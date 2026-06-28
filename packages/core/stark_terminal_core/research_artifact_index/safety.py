from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.research_artifact_index.interactions import (
    ResearchArtifactIndexForbiddenInteraction,
    default_research_artifact_index_forbidden_interactions,
)
from stark_terminal_core.research_artifact_index.types import (
    ResearchArtifactIndexSafetyLabel,
    non_empty_text,
    normalize_datetime,
    sanitize_text_list,
    utc_now,
)


class ResearchArtifactIndexSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_indexing_engine: bool = False
    allow_search_engine: bool = False
    allow_ranking_engine: bool = False
    allow_retrieval_engine: bool = False
    allow_embeddings: bool = False
    allow_vector_store: bool = False
    allow_active_ingestion: bool = False
    allow_persistent_storage: bool = False
    allow_file_uploads: bool = False
    allow_file_downloads: bool = False
    allow_file_previews: bool = False
    allow_paper_parsing: bool = False
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
        return non_empty_text(value, "research artifact index safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> ResearchArtifactIndexSafetyPolicy:
        dangerous_flags = {
            "indexing engine": self.allow_indexing_engine,
            "search engine": self.allow_search_engine,
            "ranking engine": self.allow_ranking_engine,
            "retrieval engine": self.allow_retrieval_engine,
            "embeddings": self.allow_embeddings,
            "vector store": self.allow_vector_store,
            "active ingestion": self.allow_active_ingestion,
            "persistent storage": self.allow_persistent_storage,
            "file uploads": self.allow_file_uploads,
            "file downloads": self.allow_file_downloads,
            "file previews": self.allow_file_previews,
            "paper parsing": self.allow_paper_parsing,
            "strategy generation": self.allow_strategy_generation,
            "backtesting": self.allow_backtesting,
            "recommendations": self.allow_recommendations,
            "execution": self.allow_execution,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact index safety policy cannot allow: {', '.join(enabled)}")
        if not self.require_planning_only:
            raise ValueError("research artifact index safety policy must require planning-only posture")
        return self


class ResearchArtifactIndexSafetyResult(BaseModel):
    result_id: str
    safe: bool
    reasons: list[str]
    safety_label: ResearchArtifactIndexSafetyLabel = ResearchArtifactIndexSafetyLabel.PLANNING_ONLY
    planning_only: bool = True
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
        return non_empty_text(value, "research artifact index safety result text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def result_must_fail_closed(self) -> ResearchArtifactIndexSafetyResult:
        if not self.reasons:
            raise ValueError("research artifact index safety result requires reasons")
        if not self.planning_only:
            raise ValueError("research artifact index safety result must remain planning-only")
        if self.safety_label == ResearchArtifactIndexSafetyLabel.UNKNOWN:
            raise ValueError("research artifact index safety label cannot be UNKNOWN")
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
            raise ValueError(f"research artifact index safety result cannot enable: {', '.join(enabled)}")
        return self


class ResearchArtifactIndexUnavailableResponse(BaseModel):
    response_id: str
    unavailable: bool = True
    message: str
    planning_only: bool = True
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
    broker_controls_enabled: bool = False
    readiness_to_trade_enabled: bool = False
    active_decision_objects_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research artifact index unavailable response text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> ResearchArtifactIndexUnavailableResponse:
        if not self.unavailable:
            raise ValueError("research artifact index unavailable response must remain unavailable")
        if not self.planning_only:
            raise ValueError("research artifact index unavailable response must remain planning-only")
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
            "broker controls": self.broker_controls_enabled,
            "readiness-to-trade": self.readiness_to_trade_enabled,
            "active DecisionObjects": self.active_decision_objects_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError(f"research artifact index unavailable response cannot enable: {', '.join(enabled)}")
        return self


def default_research_artifact_index_safety_policy(settings: object | None = None) -> ResearchArtifactIndexSafetyPolicy:
    schema_version = getattr(settings, "research_artifact_index_schema_version", "v1")
    return ResearchArtifactIndexSafetyPolicy(
        policy_id="research-artifact-index-safety-policy-v1",
        name="Research Artifact Index planning-only safety policy",
        schema_version=schema_version,
        notes=[
            "No indexing, search, ranking, retrieval, embeddings, vector store, ingestion, storage, parsing, recommendations, or execution.",
        ],
    )


def forbidden_interactions() -> list[ResearchArtifactIndexForbiddenInteraction]:
    return default_research_artifact_index_forbidden_interactions()


def unavailable_response_template() -> ResearchArtifactIndexUnavailableResponse:
    return ResearchArtifactIndexUnavailableResponse(
        response_id="research-artifact-index-unavailable-template-v1",
        message=(
            "Research Artifact Index is planning-only; indexing, search, ranking, retrieval, "
            "embeddings, vector stores, ingestion, storage, parsing, recommendations, and execution are unavailable."
        ),
        notes=["Prompt 77 returns unavailable placeholder metadata only."],
    )


def _reject(result_id: str, label: str) -> ResearchArtifactIndexSafetyResult:
    return ResearchArtifactIndexSafetyResult(
        result_id=result_id,
        safe=False,
        safety_label=ResearchArtifactIndexSafetyLabel.BLOCKED,
        reasons=[f"{label} is forbidden for Research Artifact Index planning."],
    )


def evaluate_research_artifact_index_safety(
    policy: ResearchArtifactIndexSafetyPolicy | None = None,
) -> ResearchArtifactIndexSafetyResult:
    policy = policy or default_research_artifact_index_safety_policy()
    return ResearchArtifactIndexSafetyResult(
        result_id="research-artifact-index-safety-evaluation-v1",
        safe=True,
        reasons=[f"{policy.name} remains fail-closed and planning-only."],
    )


def reject_indexing_engine() -> ResearchArtifactIndexSafetyResult:
    return _reject("research-artifact-index-indexing-engine-blocked-v1", "indexing engine")


def reject_search_engine() -> ResearchArtifactIndexSafetyResult:
    return _reject("research-artifact-index-search-engine-blocked-v1", "search engine")


def reject_ranking_engine() -> ResearchArtifactIndexSafetyResult:
    return _reject("research-artifact-index-ranking-engine-blocked-v1", "ranking engine")


def reject_embeddings_vector_store() -> ResearchArtifactIndexSafetyResult:
    return _reject("research-artifact-index-embeddings-vector-store-blocked-v1", "embeddings/vector store")


def reject_index_ingestion_storage() -> ResearchArtifactIndexSafetyResult:
    return _reject("research-artifact-index-ingestion-storage-blocked-v1", "ingestion/storage")


def reject_index_paper_parsing() -> ResearchArtifactIndexSafetyResult:
    return _reject("research-artifact-index-paper-parsing-blocked-v1", "paper parsing")


def reject_index_strategy_generation() -> ResearchArtifactIndexSafetyResult:
    return _reject("research-artifact-index-strategy-generation-blocked-v1", "strategy generation")


def reject_index_backtesting() -> ResearchArtifactIndexSafetyResult:
    return _reject("research-artifact-index-backtesting-blocked-v1", "backtesting")


def reject_index_recommendation_execution() -> ResearchArtifactIndexSafetyResult:
    return _reject("research-artifact-index-recommendation-execution-blocked-v1", "recommendation/execution")
