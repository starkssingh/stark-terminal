from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum


class ResearchArtifactIndexStage(StrEnum):
    PLANNING_AND_GUARDRAILS = "planning_and_guardrails"
    API_CONTRACT_SKELETON = "api_contract_skeleton"
    DISPLAY_CONTRACT_SKELETON = "display_contract_skeleton"
    AUDIT_ONLY = "audit_only"
    BLOCKED = "blocked"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactIndexKind(StrEnum):
    METADATA_INDEX_PLACEHOLDER = "METADATA_INDEX_PLACEHOLDER"
    KEY_INDEX_PLACEHOLDER = "KEY_INDEX_PLACEHOLDER"
    TAG_INDEX_PLACEHOLDER = "TAG_INDEX_PLACEHOLDER"
    REFERENCE_INDEX_PLACEHOLDER = "REFERENCE_INDEX_PLACEHOLDER"
    PROVENANCE_INDEX_PLACEHOLDER = "PROVENANCE_INDEX_PLACEHOLDER"
    LIFECYCLE_INDEX_PLACEHOLDER = "LIFECYCLE_INDEX_PLACEHOLDER"
    REGISTRY_REFERENCE_PLACEHOLDER = "REGISTRY_REFERENCE_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactIndexKeyKind(StrEnum):
    ARTIFACT_ID = "ARTIFACT_ID"
    REGISTRY_ID = "REGISTRY_ID"
    REFERENCE_ID = "REFERENCE_ID"
    PROVENANCE_ID = "PROVENANCE_ID"
    TAG = "TAG"
    CATEGORY = "CATEGORY"
    SOURCE_LABEL = "SOURCE_LABEL"
    LIFECYCLE_STATUS = "LIFECYCLE_STATUS"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactIndexTagKind(StrEnum):
    TOPIC = "TOPIC"
    ASSET_CLASS = "ASSET_CLASS"
    MARKET = "MARKET"
    METHOD = "METHOD"
    DATASET = "DATASET"
    PAPER_REFERENCE = "PAPER_REFERENCE"
    EXPERIMENT = "EXPERIMENT"
    STATUS = "STATUS"
    SAFETY = "SAFETY"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactIndexLifecycleStatus(StrEnum):
    PLACEHOLDER = "PLACEHOLDER"
    REFERENCED = "REFERENCED"
    DRAFT = "DRAFT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactIndexForbiddenInteractionKind(StrEnum):
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
    BROKER_CONTROL = "BROKER_CONTROL"
    EXECUTION = "EXECUTION"
    UNKNOWN = "UNKNOWN"


class ResearchArtifactIndexSafetyLabel(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
    NOT_AN_INDEXING_ENGINE = "NOT_AN_INDEXING_ENGINE"
    NOT_A_SEARCH_ENGINE = "NOT_A_SEARCH_ENGINE"
    NOT_A_RANKING_ENGINE = "NOT_A_RANKING_ENGINE"
    NOT_AN_EMBEDDING_PIPELINE = "NOT_AN_EMBEDDING_PIPELINE"
    NOT_A_VECTOR_STORE = "NOT_A_VECTOR_STORE"
    NOT_INGESTION = "NOT_INGESTION"
    NOT_PERSISTENT_STORAGE = "NOT_PERSISTENT_STORAGE"
    NOT_A_PAPER_PARSER = "NOT_A_PAPER_PARSER"
    NOT_A_STRATEGY = "NOT_A_STRATEGY"
    NOT_A_BACKTEST = "NOT_A_BACKTEST"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NO_EXECUTION = "NO_EXECUTION"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


SAFE_INDEX_LIFECYCLE_STATUSES = {
    ResearchArtifactIndexLifecycleStatus.PLACEHOLDER,
    ResearchArtifactIndexLifecycleStatus.REFERENCED,
    ResearchArtifactIndexLifecycleStatus.DRAFT,
    ResearchArtifactIndexLifecycleStatus.REVIEW_REQUIRED,
    ResearchArtifactIndexLifecycleStatus.BLOCKED,
    ResearchArtifactIndexLifecycleStatus.DEFERRED,
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def sanitize_text_list(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized
