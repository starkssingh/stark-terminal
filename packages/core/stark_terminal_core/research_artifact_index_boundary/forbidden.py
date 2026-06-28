from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class ResearchArtifactIndexBoundarySeverity(StrEnum):
    BLOCKER = "BLOCKER"
    WARNING = "WARNING"
    INFO = "INFO"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactIndexForbiddenBehaviorKind(StrEnum):
    ACTIVE_UI = "ACTIVE_UI"
    FRONTEND_COMPONENTS = "FRONTEND_COMPONENTS"
    DESKTOP_COMPONENTS = "DESKTOP_COMPONENTS"
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
    FILE_UPLOAD = "FILE_UPLOAD"
    FILE_DOWNLOAD = "FILE_DOWNLOAD"
    FILE_PREVIEW = "FILE_PREVIEW"
    PAPER_PARSING = "PAPER_PARSING"
    PDF_PARSING = "PDF_PARSING"
    ARXIV_INGESTION = "ARXIV_INGESTION"
    LLM_PAPER_ANALYSIS = "LLM_PAPER_ANALYSIS"
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
    BROKER_CONTROLS = "BROKER_CONTROLS"
    APPROVALS = "APPROVALS"
    OVERRIDES = "OVERRIDES"
    EXECUTION = "EXECUTION"
    EXTERNAL_CALLS = "EXTERNAL_CALLS"
    UNKNOWN = "UNKNOWN"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


REQUIRED_RESEARCH_ARTIFACT_INDEX_FORBIDDEN_BEHAVIORS = {
    ResearchArtifactIndexForbiddenBehaviorKind.ACTIVE_UI,
    ResearchArtifactIndexForbiddenBehaviorKind.FRONTEND_COMPONENTS,
    ResearchArtifactIndexForbiddenBehaviorKind.DESKTOP_COMPONENTS,
    ResearchArtifactIndexForbiddenBehaviorKind.INDEXING_ENGINE,
    ResearchArtifactIndexForbiddenBehaviorKind.SEARCH_ENGINE,
    ResearchArtifactIndexForbiddenBehaviorKind.RANKING_ENGINE,
    ResearchArtifactIndexForbiddenBehaviorKind.RETRIEVAL_ENGINE,
    ResearchArtifactIndexForbiddenBehaviorKind.EMBEDDING_PIPELINE,
    ResearchArtifactIndexForbiddenBehaviorKind.VECTOR_STORE,
    ResearchArtifactIndexForbiddenBehaviorKind.SEMANTIC_SEARCH,
    ResearchArtifactIndexForbiddenBehaviorKind.KEYWORD_SEARCH,
    ResearchArtifactIndexForbiddenBehaviorKind.ACTIVE_INGESTION,
    ResearchArtifactIndexForbiddenBehaviorKind.PERSISTENT_STORAGE,
    ResearchArtifactIndexForbiddenBehaviorKind.FILE_UPLOAD,
    ResearchArtifactIndexForbiddenBehaviorKind.FILE_DOWNLOAD,
    ResearchArtifactIndexForbiddenBehaviorKind.FILE_PREVIEW,
    ResearchArtifactIndexForbiddenBehaviorKind.PAPER_PARSING,
    ResearchArtifactIndexForbiddenBehaviorKind.PDF_PARSING,
    ResearchArtifactIndexForbiddenBehaviorKind.ARXIV_INGESTION,
    ResearchArtifactIndexForbiddenBehaviorKind.LLM_PAPER_ANALYSIS,
    ResearchArtifactIndexForbiddenBehaviorKind.METHOD_EXTRACTION,
    ResearchArtifactIndexForbiddenBehaviorKind.STRATEGY_EXTRACTION,
    ResearchArtifactIndexForbiddenBehaviorKind.STRATEGY_GENERATION,
    ResearchArtifactIndexForbiddenBehaviorKind.STRATEGY_CODE_GENERATION,
    ResearchArtifactIndexForbiddenBehaviorKind.BACKTESTING,
    ResearchArtifactIndexForbiddenBehaviorKind.OPTIMIZATION,
    ResearchArtifactIndexForbiddenBehaviorKind.RECOMMENDATION_GENERATION,
    ResearchArtifactIndexForbiddenBehaviorKind.ACTION_GENERATION,
    ResearchArtifactIndexForbiddenBehaviorKind.CONFIDENCE_SCORING,
    ResearchArtifactIndexForbiddenBehaviorKind.DECISION_OBJECT_GENERATION,
    ResearchArtifactIndexForbiddenBehaviorKind.READINESS_TO_TRADE,
    ResearchArtifactIndexForbiddenBehaviorKind.BROKER_CONTROLS,
    ResearchArtifactIndexForbiddenBehaviorKind.APPROVALS,
    ResearchArtifactIndexForbiddenBehaviorKind.OVERRIDES,
    ResearchArtifactIndexForbiddenBehaviorKind.EXECUTION,
    ResearchArtifactIndexForbiddenBehaviorKind.EXTERNAL_CALLS,
}


class ResearchArtifactIndexForbiddenBehavior(BaseModel):
    behavior_id: str
    kind: ResearchArtifactIndexForbiddenBehaviorKind
    name: str
    reason: str
    severity: ResearchArtifactIndexBoundarySeverity = ResearchArtifactIndexBoundarySeverity.BLOCKER
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("behavior_id", "name", "reason", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "research artifact index forbidden behavior text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def behavior_must_fail_closed(self) -> ResearchArtifactIndexForbiddenBehavior:
        if self.kind == ResearchArtifactIndexForbiddenBehaviorKind.UNKNOWN:
            raise ValueError("UNKNOWN research artifact index forbidden behavior is not allowed")
        if self.severity != ResearchArtifactIndexBoundarySeverity.BLOCKER:
            raise ValueError("research artifact index forbidden behavior severity must be blocker")
        if not self.forbidden_now:
            raise ValueError("research artifact index forbidden behavior cannot be unlocked")
        if not self.requires_future_prompt:
            raise ValueError("research artifact index forbidden behavior requires a future prompt")
        if not self.requires_audit_before_unlock:
            raise ValueError("research artifact index forbidden behavior requires audit before unlock")
        return self


class ResearchArtifactIndexForbiddenBehaviorRegistry(BaseModel):
    registry_id: str
    behaviors: list[ResearchArtifactIndexForbiddenBehavior]
    complete: bool = True
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    indexing_engine_allowed: bool = False
    search_engine_allowed: bool = False
    ranking_engine_allowed: bool = False
    retrieval_engine_allowed: bool = False
    embeddings_allowed: bool = False
    vector_store_allowed: bool = False
    active_ingestion_allowed: bool = False
    persistent_storage_allowed: bool = False
    file_uploads_allowed: bool = False
    file_downloads_allowed: bool = False
    file_previews_allowed: bool = False
    paper_parsing_allowed: bool = False
    strategy_generation_allowed: bool = False
    backtesting_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    approvals_allowed: bool = False
    overrides_allowed: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("registry_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "research artifact index forbidden registry text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def registry_must_be_complete_and_safe(self) -> ResearchArtifactIndexForbiddenBehaviorRegistry:
        if not self.complete:
            raise ValueError("research artifact index forbidden registry must be complete")
        if not self.behaviors:
            raise ValueError("research artifact index forbidden registry requires behaviors")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "indexing engine": self.indexing_engine_allowed,
            "search engine": self.search_engine_allowed,
            "ranking engine": self.ranking_engine_allowed,
            "retrieval engine": self.retrieval_engine_allowed,
            "embeddings": self.embeddings_allowed,
            "vector store": self.vector_store_allowed,
            "active ingestion": self.active_ingestion_allowed,
            "persistent storage": self.persistent_storage_allowed,
            "file uploads": self.file_uploads_allowed,
            "file downloads": self.file_downloads_allowed,
            "file previews": self.file_previews_allowed,
            "paper parsing": self.paper_parsing_allowed,
            "strategy generation": self.strategy_generation_allowed,
            "backtesting": self.backtesting_allowed,
            "recommendations": self.recommendations_allowed,
            "action generation": self.action_generation_allowed,
            "confidence scoring": self.confidence_scoring_allowed,
            "DecisionObject generation": self.decision_object_generation_allowed,
            "readiness-to-trade": self.readiness_to_trade_allowed,
            "broker controls": self.broker_controls_allowed,
            "approvals": self.approvals_allowed,
            "overrides": self.overrides_allowed,
            "execution": self.execution_allowed,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("research artifact index boundary cannot allow: " + ", ".join(enabled))
        present = {behavior.kind for behavior in self.behaviors}
        missing = sorted(kind.value for kind in REQUIRED_RESEARCH_ARTIFACT_INDEX_FORBIDDEN_BEHAVIORS - present)
        if missing:
            raise ValueError(
                "research artifact index forbidden registry missing required kinds: " + ", ".join(missing)
            )
        return self


def default_research_artifact_index_forbidden_behaviors() -> list[
    ResearchArtifactIndexForbiddenBehavior
]:
    specs = [
        (ResearchArtifactIndexForbiddenBehaviorKind.ACTIVE_UI, "Active UI"),
        (ResearchArtifactIndexForbiddenBehaviorKind.FRONTEND_COMPONENTS, "Frontend components"),
        (ResearchArtifactIndexForbiddenBehaviorKind.DESKTOP_COMPONENTS, "Desktop components"),
        (ResearchArtifactIndexForbiddenBehaviorKind.INDEXING_ENGINE, "Indexing engine"),
        (ResearchArtifactIndexForbiddenBehaviorKind.SEARCH_ENGINE, "Search engine"),
        (ResearchArtifactIndexForbiddenBehaviorKind.RANKING_ENGINE, "Ranking engine"),
        (ResearchArtifactIndexForbiddenBehaviorKind.RETRIEVAL_ENGINE, "Retrieval engine"),
        (ResearchArtifactIndexForbiddenBehaviorKind.EMBEDDING_PIPELINE, "Embedding pipeline"),
        (ResearchArtifactIndexForbiddenBehaviorKind.VECTOR_STORE, "Vector store"),
        (ResearchArtifactIndexForbiddenBehaviorKind.SEMANTIC_SEARCH, "Semantic search"),
        (ResearchArtifactIndexForbiddenBehaviorKind.KEYWORD_SEARCH, "Keyword search"),
        (ResearchArtifactIndexForbiddenBehaviorKind.ACTIVE_INGESTION, "Active ingestion"),
        (ResearchArtifactIndexForbiddenBehaviorKind.PERSISTENT_STORAGE, "Persistent storage"),
        (ResearchArtifactIndexForbiddenBehaviorKind.FILE_UPLOAD, "File upload"),
        (ResearchArtifactIndexForbiddenBehaviorKind.FILE_DOWNLOAD, "File download"),
        (ResearchArtifactIndexForbiddenBehaviorKind.FILE_PREVIEW, "File preview"),
        (ResearchArtifactIndexForbiddenBehaviorKind.PAPER_PARSING, "Paper parsing"),
        (ResearchArtifactIndexForbiddenBehaviorKind.PDF_PARSING, "PDF parsing"),
        (ResearchArtifactIndexForbiddenBehaviorKind.ARXIV_INGESTION, "arXiv ingestion"),
        (ResearchArtifactIndexForbiddenBehaviorKind.LLM_PAPER_ANALYSIS, "LLM paper analysis"),
        (ResearchArtifactIndexForbiddenBehaviorKind.METHOD_EXTRACTION, "Method extraction"),
        (ResearchArtifactIndexForbiddenBehaviorKind.STRATEGY_EXTRACTION, "Strategy extraction"),
        (ResearchArtifactIndexForbiddenBehaviorKind.STRATEGY_GENERATION, "Strategy generation"),
        (ResearchArtifactIndexForbiddenBehaviorKind.STRATEGY_CODE_GENERATION, "Strategy code generation"),
        (ResearchArtifactIndexForbiddenBehaviorKind.BACKTESTING, "Backtesting"),
        (ResearchArtifactIndexForbiddenBehaviorKind.OPTIMIZATION, "Optimization"),
        (ResearchArtifactIndexForbiddenBehaviorKind.RECOMMENDATION_GENERATION, "Recommendation generation"),
        (ResearchArtifactIndexForbiddenBehaviorKind.ACTION_GENERATION, "Action generation"),
        (ResearchArtifactIndexForbiddenBehaviorKind.CONFIDENCE_SCORING, "Confidence scoring"),
        (ResearchArtifactIndexForbiddenBehaviorKind.DECISION_OBJECT_GENERATION, "DecisionObject generation"),
        (ResearchArtifactIndexForbiddenBehaviorKind.READINESS_TO_TRADE, "Readiness-to-trade"),
        (ResearchArtifactIndexForbiddenBehaviorKind.BROKER_CONTROLS, "Broker controls"),
        (ResearchArtifactIndexForbiddenBehaviorKind.APPROVALS, "Approvals"),
        (ResearchArtifactIndexForbiddenBehaviorKind.OVERRIDES, "Overrides"),
        (ResearchArtifactIndexForbiddenBehaviorKind.EXECUTION, "Execution"),
        (ResearchArtifactIndexForbiddenBehaviorKind.EXTERNAL_CALLS, "External calls"),
    ]
    return [
        ResearchArtifactIndexForbiddenBehavior(
            behavior_id=f"research-artifact-index-{kind.value.lower().replace('_', '-')}-forbidden-v1",
            kind=kind,
            name=name,
            reason=f"{name} remains forbidden by the Prompt 82 system boundary layer.",
        )
        for kind, name in specs
    ]


def default_research_artifact_index_forbidden_behavior_registry() -> (
    ResearchArtifactIndexForbiddenBehaviorRegistry
):
    return ResearchArtifactIndexForbiddenBehaviorRegistry(
        registry_id="research-artifact-index-forbidden-behavior-registry-v1",
        behaviors=default_research_artifact_index_forbidden_behaviors(),
    )

