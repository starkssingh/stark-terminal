from __future__ import annotations

from pydantic import BaseModel, field_validator

from stark_terminal_core.research_knowledge_map.planning import non_empty_text


FORBIDDEN_ACTIONS = (
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


class ResearchKnowledgeMapApiSafetyResult(BaseModel):
    safety_id: str
    blocked: bool
    safe: bool
    reason: str
    allowed: bool = False

    @field_validator("safety_id", "reason")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map API safety result text")


def research_knowledge_map_api_forbidden_actions() -> tuple[str, ...]:
    return FORBIDDEN_ACTIONS


def _safety_result(action: str, enabled: bool) -> ResearchKnowledgeMapApiSafetyResult:
    return ResearchKnowledgeMapApiSafetyResult(
        safety_id=f"research-knowledge-map-api-no-{action.replace(' ', '-').replace('/', '-')}-v1",
        blocked=enabled,
        safe=not enabled,
        reason=(
            f"{action} is forbidden for Research Knowledge Map API contract skeleton."
            if enabled
            else f"{action} remains disabled for Research Knowledge Map API contract skeleton."
        ),
    )


def assert_no_knowledge_map_api_database_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("database", enabled)


def assert_no_knowledge_map_api_persistent_writes_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("persistent writes", enabled)


def assert_no_knowledge_map_api_traversal_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("traversal", enabled)


def assert_no_knowledge_map_api_search_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("search", enabled)


def assert_no_knowledge_map_api_ranking_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("ranking", enabled)


def assert_no_knowledge_map_api_retrieval_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("retrieval", enabled)


def assert_no_knowledge_map_api_embeddings_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("embeddings", enabled)


def assert_no_knowledge_map_api_vector_store_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("vector store", enabled)


def assert_no_knowledge_map_api_paper_parsing_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("paper parsing", enabled)


def assert_no_knowledge_map_api_strategy_generation_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("strategy generation", enabled)


def assert_no_knowledge_map_api_backtesting_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("backtesting", enabled)


def assert_no_knowledge_map_api_recommendation_enabled(
    enabled: bool = False,
) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("recommendation generation", enabled)


def assert_no_knowledge_map_api_execution_enabled(enabled: bool = False) -> ResearchKnowledgeMapApiSafetyResult:
    return _safety_result("execution", enabled)
