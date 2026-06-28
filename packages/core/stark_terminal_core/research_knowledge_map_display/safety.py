from __future__ import annotations

from pydantic import BaseModel, field_validator

from stark_terminal_core.research_knowledge_map.planning import non_empty_text


FORBIDDEN_ACTIONS = (
    "active UI",
    "frontend components",
    "desktop components",
    "active knowledge map",
    "database",
    "persistent writes",
    "traversal",
    "query",
    "search",
    "ranking",
    "retrieval",
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
    "method extraction",
    "strategy extraction",
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


class ResearchKnowledgeMapDisplaySafetyResult(BaseModel):
    safety_id: str
    blocked: bool
    safe: bool
    reason: str
    allowed: bool = False

    @field_validator("safety_id", "reason")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map display safety result text")


def research_knowledge_map_display_forbidden_actions() -> tuple[str, ...]:
    return FORBIDDEN_ACTIONS


def _safety_result(action: str, enabled: bool) -> ResearchKnowledgeMapDisplaySafetyResult:
    return ResearchKnowledgeMapDisplaySafetyResult(
        safety_id=f"research-knowledge-map-display-no-{action.replace(' ', '-').replace('/', '-')}-v1",
        blocked=enabled,
        safe=not enabled,
        reason=(
            f"{action} is forbidden for Research Knowledge Map Display contract skeleton."
            if enabled
            else f"{action} remains disabled for Research Knowledge Map Display contract skeleton."
        ),
    )


def assert_no_knowledge_map_display_active_ui_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("active UI", enabled)


def assert_no_knowledge_map_display_frontend_components_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("frontend components", enabled)


def assert_no_knowledge_map_display_desktop_components_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("desktop components", enabled)


def assert_no_knowledge_map_display_database_enabled(enabled: bool = False) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("database", enabled)


def assert_no_knowledge_map_display_persistent_writes_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("persistent writes", enabled)


def assert_no_knowledge_map_display_traversal_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("traversal", enabled)


def assert_no_knowledge_map_display_search_enabled(enabled: bool = False) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("search", enabled)


def assert_no_knowledge_map_display_ranking_enabled(enabled: bool = False) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("ranking", enabled)


def assert_no_knowledge_map_display_retrieval_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("retrieval", enabled)


def assert_no_knowledge_map_display_embeddings_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("embeddings", enabled)


def assert_no_knowledge_map_display_vector_store_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("vector store", enabled)


def assert_no_knowledge_map_display_paper_parsing_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("paper parsing", enabled)


def assert_no_knowledge_map_display_strategy_generation_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("strategy generation", enabled)


def assert_no_knowledge_map_display_backtesting_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("backtesting", enabled)


def assert_no_knowledge_map_display_recommendation_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("recommendation generation", enabled)


def assert_no_knowledge_map_display_execution_enabled(enabled: bool = False) -> ResearchKnowledgeMapDisplaySafetyResult:
    return _safety_result("execution", enabled)
