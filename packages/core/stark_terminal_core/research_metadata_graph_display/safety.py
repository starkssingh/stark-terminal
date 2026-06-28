from __future__ import annotations

from pydantic import BaseModel, field_validator

from stark_terminal_core.research_metadata_graph.planning import non_empty_text


FORBIDDEN_ACTIONS = (
    "active UI",
    "frontend components",
    "desktop components",
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


class ResearchMetadataGraphDisplaySafetyResult(BaseModel):
    safety_id: str
    blocked: bool
    safe: bool
    reason: str
    allowed: bool = False

    @field_validator("safety_id", "reason")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph display safety result text")


def research_metadata_graph_display_forbidden_actions() -> tuple[str, ...]:
    return FORBIDDEN_ACTIONS


def _safety_result(action: str, enabled: bool) -> ResearchMetadataGraphDisplaySafetyResult:
    return ResearchMetadataGraphDisplaySafetyResult(
        safety_id=f"research-metadata-graph-display-no-{action.replace(' ', '-').replace('/', '-')}-v1",
        blocked=enabled,
        safe=not enabled,
        reason=(
            f"{action} is forbidden for Research Metadata Graph Display contract skeleton."
            if enabled
            else f"{action} remains disabled for Research Metadata Graph Display contract skeleton."
        ),
    )


def assert_no_graph_display_active_ui_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("active UI", enabled)


def assert_no_graph_display_frontend_components_enabled(
    enabled: bool = False,
) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("frontend components", enabled)


def assert_no_graph_display_desktop_components_enabled(
    enabled: bool = False,
) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("desktop components", enabled)


def assert_no_graph_display_database_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("graph database", enabled)


def assert_no_graph_display_persistent_writes_enabled(
    enabled: bool = False,
) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("persistent graph writes", enabled)


def assert_no_graph_display_traversal_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("graph traversal", enabled)


def assert_no_graph_display_search_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("graph search", enabled)


def assert_no_graph_display_ranking_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("graph ranking", enabled)


def assert_no_graph_display_retrieval_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("graph retrieval", enabled)


def assert_no_graph_display_embeddings_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("embeddings", enabled)


def assert_no_graph_display_vector_store_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("vector store", enabled)


def assert_no_graph_display_ingestion_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("active ingestion", enabled)


def assert_no_graph_display_upload_download_preview_enabled(
    enabled: bool = False,
) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("file upload/download/preview", enabled)


def assert_no_graph_display_paper_parsing_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("paper parsing", enabled)


def assert_no_graph_display_strategy_generation_enabled(
    enabled: bool = False,
) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("strategy generation", enabled)


def assert_no_graph_display_backtesting_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("backtesting", enabled)


def assert_no_graph_display_recommendation_enabled(
    enabled: bool = False,
) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("recommendation generation", enabled)


def assert_no_graph_display_execution_enabled(enabled: bool = False) -> ResearchMetadataGraphDisplaySafetyResult:
    return _safety_result("execution", enabled)
