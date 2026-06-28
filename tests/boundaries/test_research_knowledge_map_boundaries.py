from pydantic import ValidationError

from stark_terminal_core.research_knowledge_map.evidence import (
    default_research_knowledge_map_evidence_placeholders,
)
from stark_terminal_core.research_knowledge_map.guardrails import (
    assert_no_knowledge_map_backtesting_enabled,
    assert_no_knowledge_map_database_enabled,
    assert_no_knowledge_map_embeddings_enabled,
    assert_no_knowledge_map_execution_enabled,
    assert_no_knowledge_map_paper_parsing_enabled,
    assert_no_knowledge_map_persistent_writes_enabled,
    assert_no_knowledge_map_ranking_enabled,
    assert_no_knowledge_map_recommendation_enabled,
    assert_no_knowledge_map_retrieval_enabled,
    assert_no_knowledge_map_search_enabled,
    assert_no_knowledge_map_strategy_generation_enabled,
    assert_no_knowledge_map_traversal_enabled,
    assert_no_knowledge_map_vector_store_enabled,
    research_knowledge_map_forbidden_actions,
)
from stark_terminal_core.research_knowledge_map.health import (
    research_knowledge_map_health,
)
from stark_terminal_core.research_knowledge_map.items import (
    KnowledgeMapItemKind,
    KnowledgeMapItemPlaceholder,
    default_research_knowledge_map_item_placeholders,
)
from stark_terminal_core.research_knowledge_map.lifecycle import (
    FORBIDDEN_LIFECYCLE_MEANINGS,
    KnowledgeMapLifecycleState,
    default_research_knowledge_map_lifecycle_placeholder,
)
from stark_terminal_core.research_knowledge_map.planning import (
    ResearchKnowledgeMapPlanningContract,
    default_research_knowledge_map_planning_contract,
)
from stark_terminal_core.research_knowledge_map.provenance import (
    default_research_knowledge_map_provenance_placeholders,
)
from stark_terminal_core.research_knowledge_map.readiness import (
    research_knowledge_map_readiness,
)
from stark_terminal_core.research_knowledge_map.relationships import (
    KnowledgeMapRelationshipKind,
    KnowledgeMapRelationshipPlaceholder,
    default_research_knowledge_map_relationship_placeholders,
)


def test_research_knowledge_map_planning_contract_validates_and_blocks_dangerous_flags() -> None:
    contract = default_research_knowledge_map_planning_contract()
    assert contract.service == "stark-terminal-research-knowledge-map"
    assert contract.stage == "planning_and_guardrails"
    assert contract.planning_only is True
    assert contract.read_only is True
    assert contract.unavailable_by_default is True
    assert contract.database_enabled is False
    assert contract.traversal_enabled is False
    assert contract.search_enabled is False
    assert contract.ranking_enabled is False
    assert contract.retrieval_enabled is False
    assert contract.embeddings_enabled is False
    assert contract.vector_store_enabled is False
    assert contract.execution_enabled is False

    try:
        ResearchKnowledgeMapPlanningContract(
            contract_id="unsafe",
            database_enabled=True,
        )
    except ValidationError as exc:
        assert "database" in str(exc).lower()
    else:
        raise AssertionError("database must be rejected")


def test_research_knowledge_map_placeholders_validate_without_active_behavior() -> None:
    items = default_research_knowledge_map_item_placeholders()
    relationships = default_research_knowledge_map_relationship_placeholders()
    evidence = default_research_knowledge_map_evidence_placeholders()
    provenance = default_research_knowledge_map_provenance_placeholders()
    lifecycle = default_research_knowledge_map_lifecycle_placeholder()

    assert {item.item_kind for item in items} == set(KnowledgeMapItemKind)
    assert {relationship.relationship_kind for relationship in relationships} == set(KnowledgeMapRelationshipKind)
    assert all(item.descriptive_only and item.read_only for item in items)
    assert all(not item.persisted for item in items)
    assert all(not item.database_query_enabled for item in items)
    assert all(not item.graph_query_enabled for item in items)
    assert all(not item.paper_parsing_enabled for item in items)
    assert all(not item.strategy_generation_enabled for item in items)
    assert all(not item.backtesting_enabled for item in items)
    assert all(not item.recommendations_enabled for item in items)
    assert all(relationship.descriptive_only and relationship.read_only for relationship in relationships)
    assert all(not relationship.persisted for relationship in relationships)
    assert all(not relationship.traversal_enabled for relationship in relationships)
    assert all(not relationship.relationship_ranking_enabled for relationship in relationships)
    assert all(not relationship.artifact_retrieval_enabled for relationship in relationships)
    assert all(item.descriptive_only for item in evidence)
    assert all(not item.validates_truth for item in evidence)
    assert all(not item.creates_trade_readiness for item in evidence)
    assert all(item.descriptive_only for item in provenance)
    assert all(not item.external_fetch_enabled for item in provenance)
    assert all(not item.local_file_read_enabled for item in provenance)
    assert lifecycle.state == KnowledgeMapLifecycleState.PLANNED
    assert not FORBIDDEN_LIFECYCLE_MEANINGS.intersection({state.value for state in KnowledgeMapLifecycleState})
    assert lifecycle.indexed is False
    assert lifecycle.searchable is False
    assert lifecycle.recommended is False
    assert lifecycle.executable is False


def test_research_knowledge_map_placeholders_reject_active_behavior() -> None:
    try:
        KnowledgeMapItemPlaceholder(
            item_id="unsafe-paper",
            item_kind=KnowledgeMapItemKind.PAPER,
            label="Unsafe paper",
            description="Unsafe paper",
            paper_parsing_enabled=True,
        )
    except ValidationError as exc:
        assert "parse papers" in str(exc).lower()
    else:
        raise AssertionError("paper parsing must be rejected")

    try:
        KnowledgeMapRelationshipPlaceholder(
            relationship_id="unsafe-relationship",
            relationship_kind=KnowledgeMapRelationshipKind.DEPENDS_ON,
            label="Unsafe relationship",
            description="Unsafe relationship",
            traversal_enabled=True,
        )
    except ValidationError as exc:
        assert "traverse graph" in str(exc).lower()
    else:
        raise AssertionError("traversal must be rejected")


def test_research_knowledge_map_readiness_and_health_are_planning_only() -> None:
    readiness = research_knowledge_map_readiness()
    health = research_knowledge_map_health()

    assert readiness.ready_for_planning is True
    assert readiness.ready_for_api_contract_skeleton is False
    assert readiness.ready_for_active_map is False
    assert readiness.ready_for_database is False
    assert readiness.ready_for_traversal is False
    assert readiness.ready_for_search is False
    assert readiness.ready_for_ranking is False
    assert readiness.ready_for_retrieval is False
    assert readiness.ready_for_embeddings is False
    assert readiness.ready_for_vector_store is False
    assert readiness.ready_for_strategy_generation is False
    assert readiness.ready_for_backtesting is False
    assert readiness.ready_for_recommendations is False
    assert readiness.ready_for_execution is False
    assert health.planning_only is True
    assert health.read_only is True
    assert health.status == "healthy"
    assert health.database_enabled is False
    assert health.search_enabled is False
    assert health.retrieval_enabled is False
    assert health.execution_enabled is False


def test_research_knowledge_map_guardrails_block_dangerous_behavior() -> None:
    forbidden = research_knowledge_map_forbidden_actions()
    for phrase in [
        "active knowledge map",
        "database",
        "persistent writes",
        "graph traversal",
        "search",
        "ranking",
        "retrieval",
        "embeddings",
        "vector store",
        "paper parsing",
        "strategy generation",
        "backtesting",
        "recommendation generation",
        "execution",
    ]:
        assert phrase in forbidden

    helpers = [
        assert_no_knowledge_map_database_enabled,
        assert_no_knowledge_map_persistent_writes_enabled,
        assert_no_knowledge_map_traversal_enabled,
        assert_no_knowledge_map_search_enabled,
        assert_no_knowledge_map_ranking_enabled,
        assert_no_knowledge_map_retrieval_enabled,
        assert_no_knowledge_map_embeddings_enabled,
        assert_no_knowledge_map_vector_store_enabled,
        assert_no_knowledge_map_paper_parsing_enabled,
        assert_no_knowledge_map_strategy_generation_enabled,
        assert_no_knowledge_map_backtesting_enabled,
        assert_no_knowledge_map_recommendation_enabled,
        assert_no_knowledge_map_execution_enabled,
    ]
    for helper in helpers:
        result = helper(True)
        assert result.blocked is True
        assert result.safe is False
        assert result.allowed is False
