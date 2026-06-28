from __future__ import annotations

from pydantic import BaseModel, field_validator

from stark_terminal_core.research_metadata_graph.planning import non_empty_text


FORBIDDEN_ACTIONS = (
    "graph database",
    "persistent graph writes",
    "graph traversal",
    "graph query",
    "graph search",
    "graph ranking",
    "graph retrieval",
    "embeddings",
    "vector store",
    "active ingestion",
    "active storage",
    "file upload",
    "file download",
    "file preview",
    "paper parsing",
    "PDF parsing",
    "arXiv ingestion",
    "LLM paper analysis",
    "strategy generation",
    "strategy code generation",
    "backtesting",
    "optimization",
    "recommendation generation",
    "action generation",
    "confidence scoring",
    "DecisionObject generation",
    "readiness-to-trade",
    "broker controls",
    "approvals",
    "overrides",
    "execution",
)


class ResearchMetadataGraphApiSafetyResult(BaseModel):
    safety_id: str
    blocked: bool
    safe: bool
    reason: str
    allowed: bool = False

    @field_validator("safety_id", "reason")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph API safety result text")


def research_metadata_graph_api_forbidden_actions() -> tuple[str, ...]:
    return FORBIDDEN_ACTIONS


def _safety_result(action: str, enabled: bool) -> ResearchMetadataGraphApiSafetyResult:
    return ResearchMetadataGraphApiSafetyResult(
        safety_id=f"research-metadata-graph-api-no-{action.replace(' ', '-').replace('/', '-')}-v1",
        blocked=enabled,
        safe=not enabled,
        reason=(
            f"{action} is forbidden for Research Metadata Graph API contract skeleton."
            if enabled
            else f"{action} remains disabled for Research Metadata Graph API contract skeleton."
        ),
    )


def assert_no_graph_api_database_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("graph database", enabled)


def assert_no_graph_api_persistent_writes_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("persistent graph writes", enabled)


def assert_no_graph_api_traversal_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("graph traversal", enabled)


def assert_no_graph_api_search_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("graph search", enabled)


def assert_no_graph_api_ranking_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("graph ranking", enabled)


def assert_no_graph_api_retrieval_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("graph retrieval", enabled)


def assert_no_graph_api_embeddings_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("embeddings", enabled)


def assert_no_graph_api_vector_store_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("vector store", enabled)


def assert_no_graph_api_ingestion_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("active ingestion", enabled)


def assert_no_graph_api_upload_download_preview_enabled(
    enabled: bool = False,
) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("file upload/download/preview", enabled)


def assert_no_graph_api_paper_parsing_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("paper parsing", enabled)


def assert_no_graph_api_strategy_generation_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("strategy generation", enabled)


def assert_no_graph_api_backtesting_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("backtesting", enabled)


def assert_no_graph_api_recommendation_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("recommendation generation", enabled)


def assert_no_graph_api_execution_enabled(enabled: bool = False) -> ResearchMetadataGraphApiSafetyResult:
    return _safety_result("execution", enabled)
