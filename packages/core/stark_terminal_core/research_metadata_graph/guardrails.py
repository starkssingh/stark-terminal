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


class ResearchMetadataGraphGuardrailResult(BaseModel):
    guardrail_id: str
    blocked: bool
    safe: bool
    reason: str
    allowed: bool = False

    @field_validator("guardrail_id", "reason")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "research metadata graph guardrail result text")


def research_metadata_graph_forbidden_actions() -> tuple[str, ...]:
    return FORBIDDEN_ACTIONS


def _guardrail_result(action: str, enabled: bool) -> ResearchMetadataGraphGuardrailResult:
    return ResearchMetadataGraphGuardrailResult(
        guardrail_id=f"research-metadata-graph-no-{action.replace(' ', '-').replace('/', '-')}-v1",
        blocked=enabled,
        safe=not enabled,
        reason=(
            f"{action} is forbidden for Research Metadata Graph planning."
            if enabled
            else f"{action} remains disabled for Research Metadata Graph planning."
        ),
    )


def assert_no_graph_database_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("graph database", enabled)


def assert_no_graph_persistent_writes_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("persistent graph writes", enabled)


def assert_no_graph_traversal_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("graph traversal", enabled)


def assert_no_graph_search_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("graph search", enabled)


def assert_no_graph_ranking_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("graph ranking", enabled)


def assert_no_graph_retrieval_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("graph retrieval", enabled)


def assert_no_graph_embeddings_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("embeddings", enabled)


def assert_no_graph_vector_store_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("vector store", enabled)


def assert_no_graph_ingestion_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("active ingestion", enabled)


def assert_no_graph_upload_download_preview_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("file upload/download/preview", enabled)


def assert_no_graph_paper_parsing_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("paper parsing", enabled)


def assert_no_graph_strategy_generation_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("strategy generation", enabled)


def assert_no_graph_backtesting_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("backtesting", enabled)


def assert_no_graph_recommendation_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("recommendation generation", enabled)


def assert_no_graph_execution_enabled(enabled: bool = False) -> ResearchMetadataGraphGuardrailResult:
    return _guardrail_result("execution", enabled)
