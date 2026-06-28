from __future__ import annotations

from pydantic import BaseModel, field_validator

from stark_terminal_core.research_knowledge_map.planning import non_empty_text


FORBIDDEN_ACTIONS = (
    "active knowledge map",
    "database",
    "persistent writes",
    "graph traversal",
    "query engine",
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


class ResearchKnowledgeMapGuardrailResult(BaseModel):
    guardrail_id: str
    blocked: bool
    safe: bool
    reason: str
    allowed: bool = False

    @field_validator("guardrail_id", "reason")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research knowledge map guardrail result text")


def research_knowledge_map_forbidden_actions() -> tuple[str, ...]:
    return FORBIDDEN_ACTIONS


def _guardrail_result(action: str, enabled: bool) -> ResearchKnowledgeMapGuardrailResult:
    return ResearchKnowledgeMapGuardrailResult(
        guardrail_id=f"research-knowledge-map-no-{action.replace(' ', '-').replace('/', '-')}-v1",
        blocked=enabled,
        safe=not enabled,
        reason=(
            f"{action} is forbidden for Research Knowledge Map planning."
            if enabled
            else f"{action} remains disabled for Research Knowledge Map planning."
        ),
    )


def assert_no_knowledge_map_database_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("database", enabled)


def assert_no_knowledge_map_persistent_writes_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("persistent writes", enabled)


def assert_no_knowledge_map_traversal_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("graph traversal", enabled)


def assert_no_knowledge_map_search_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("search", enabled)


def assert_no_knowledge_map_ranking_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("ranking", enabled)


def assert_no_knowledge_map_retrieval_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("retrieval", enabled)


def assert_no_knowledge_map_embeddings_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("embeddings", enabled)


def assert_no_knowledge_map_vector_store_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("vector store", enabled)


def assert_no_knowledge_map_paper_parsing_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("paper parsing", enabled)


def assert_no_knowledge_map_strategy_generation_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("strategy generation", enabled)


def assert_no_knowledge_map_backtesting_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("backtesting", enabled)


def assert_no_knowledge_map_recommendation_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("recommendation generation", enabled)


def assert_no_knowledge_map_execution_enabled(enabled: bool = False) -> ResearchKnowledgeMapGuardrailResult:
    return _guardrail_result("execution", enabled)
