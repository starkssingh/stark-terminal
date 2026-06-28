from pydantic import ValidationError

from stark_terminal_core.research_knowledge_map_api.contracts import (
    ResearchKnowledgeMapApiContract,
    default_research_knowledge_map_api_contract,
)
from stark_terminal_core.research_knowledge_map_api.health import (
    research_knowledge_map_api_health,
)
from stark_terminal_core.research_knowledge_map_api.references import (
    KnowledgeMapApiReferencePlaceholder,
    default_knowledge_map_api_reference_placeholder,
    default_knowledge_map_item_reference_placeholder,
    default_knowledge_map_provenance_reference_placeholder,
    default_knowledge_map_relationship_reference_placeholder,
)
from stark_terminal_core.research_knowledge_map_api.requests import (
    KnowledgeItemLookupRequestPlaceholder,
    default_knowledge_evidence_request_placeholder,
    default_knowledge_item_lookup_request_placeholder,
    default_knowledge_provenance_request_placeholder,
    default_knowledge_relationship_request_placeholder,
    default_research_knowledge_map_request_placeholder,
)
from stark_terminal_core.research_knowledge_map_api.responses import (
    KnowledgeItemResponsePlaceholder,
    default_knowledge_evidence_response_placeholder,
    default_knowledge_item_response_placeholder,
    default_knowledge_provenance_response_placeholder,
    default_knowledge_relationship_response_placeholder,
    default_research_knowledge_map_response_placeholder,
)
from stark_terminal_core.research_knowledge_map_api.safety import (
    assert_no_knowledge_map_api_backtesting_enabled,
    assert_no_knowledge_map_api_database_enabled,
    assert_no_knowledge_map_api_embeddings_enabled,
    assert_no_knowledge_map_api_execution_enabled,
    assert_no_knowledge_map_api_paper_parsing_enabled,
    assert_no_knowledge_map_api_persistent_writes_enabled,
    assert_no_knowledge_map_api_ranking_enabled,
    assert_no_knowledge_map_api_recommendation_enabled,
    assert_no_knowledge_map_api_retrieval_enabled,
    assert_no_knowledge_map_api_search_enabled,
    assert_no_knowledge_map_api_strategy_generation_enabled,
    assert_no_knowledge_map_api_traversal_enabled,
    assert_no_knowledge_map_api_vector_store_enabled,
    research_knowledge_map_api_forbidden_actions,
)
from stark_terminal_core.research_knowledge_map_api.unavailable import (
    ResearchKnowledgeMapApiUnavailableResponse,
    unavailable_knowledge_map_api_response_template,
)


def test_research_knowledge_map_api_contract_validates_and_blocks_dangerous_flags() -> None:
    contract = default_research_knowledge_map_api_contract()
    assert contract.service == "stark-terminal-research-knowledge-map-api"
    assert contract.stage == "api_contract_skeleton"
    assert contract.api_contract_skeleton_only is True
    assert contract.read_only is True
    assert contract.unavailable_by_default is True
    assert contract.database_enabled is False
    assert contract.persistent_writes_enabled is False
    assert contract.traversal_enabled is False
    assert contract.search_enabled is False
    assert contract.ranking_enabled is False
    assert contract.retrieval_enabled is False
    assert contract.embeddings_enabled is False
    assert contract.vector_store_enabled is False
    assert contract.execution_enabled is False

    try:
        ResearchKnowledgeMapApiContract(
            contract_id="unsafe",
            database_enabled=True,
        )
    except ValidationError as exc:
        assert "database" in str(exc).lower()
    else:
        raise AssertionError("database must be rejected")


def test_research_knowledge_map_api_request_placeholders_validate_without_active_behavior() -> None:
    requests = [
        default_research_knowledge_map_request_placeholder(),
        default_knowledge_item_lookup_request_placeholder(),
        default_knowledge_relationship_request_placeholder(),
        default_knowledge_evidence_request_placeholder(),
        default_knowledge_provenance_request_placeholder(),
    ]

    assert all(item.metadata_only and item.read_only for item in requests)
    assert all(not item.lookup_trigger_enabled for item in requests)
    assert all(not item.traversal_trigger_enabled for item in requests)
    assert all(not item.search_trigger_enabled for item in requests)
    assert all(not item.retrieval_trigger_enabled for item in requests)
    assert all(not item.accepts_file_bytes for item in requests)
    assert all(not item.accepts_raw_paper_content for item in requests)
    assert all(not item.accepts_market_data_for_recommendations for item in requests)
    assert all(not item.accepts_strategy_generation_instructions for item in requests)

    try:
        KnowledgeItemLookupRequestPlaceholder(
            request_id="unsafe-request",
            lookup_trigger_enabled=True,
        )
    except ValidationError as exc:
        assert "lookup trigger" in str(exc).lower()
    else:
        raise AssertionError("lookup trigger must be rejected")


def test_research_knowledge_map_api_response_placeholders_validate_without_outputs() -> None:
    responses = [
        default_research_knowledge_map_response_placeholder(),
        default_knowledge_item_response_placeholder(),
        default_knowledge_relationship_response_placeholder(),
        default_knowledge_evidence_response_placeholder(),
        default_knowledge_provenance_response_placeholder(),
    ]

    assert all(item.unavailable_by_default and item.placeholder_only for item in responses)
    assert all(not item.retrieved_map_data_present for item in responses)
    assert all(not item.search_results_present for item in responses)
    assert all(not item.rankings_present for item in responses)
    assert all(not item.embeddings_present for item in responses)
    assert all(not item.parsed_paper_content_present for item in responses)
    assert all(not item.generated_strategies_present for item in responses)
    assert all(not item.backtest_results_present for item in responses)
    assert all(not item.recommendations_present for item in responses)
    assert all(not item.execution_controls_present for item in responses)

    try:
        KnowledgeItemResponsePlaceholder(
            response_id="unsafe-response",
            retrieved_map_data_present=True,
        )
    except ValidationError as exc:
        assert "retrieved map data" in str(exc).lower()
    else:
        raise AssertionError("retrieved map data must be rejected")


def test_research_knowledge_map_api_reference_and_unavailable_placeholders_validate() -> None:
    references = [
        default_knowledge_map_api_reference_placeholder(),
        default_knowledge_map_item_reference_placeholder(),
        default_knowledge_map_relationship_reference_placeholder(),
        default_knowledge_map_provenance_reference_placeholder(),
    ]
    unavailable = unavailable_knowledge_map_api_response_template()

    assert all(item.descriptive_only for item in references)
    assert all(not item.fetch_enabled for item in references)
    assert all(not item.retrieval_enabled for item in references)
    assert all(not item.source_truth_validation_enabled for item in references)
    assert all(not item.persistence_implied for item in references)
    assert unavailable.unavailable is True
    assert unavailable.allowed_stage == "api_contract_skeleton"
    assert unavailable.database_enabled is False
    assert unavailable.retrieval_enabled is False
    assert unavailable.execution_enabled is False

    try:
        KnowledgeMapApiReferencePlaceholder(
            reference_id="unsafe-reference",
            reference_kind="UNSAFE",
            fetch_enabled=True,
        )
    except ValidationError as exc:
        assert "fetch" in str(exc).lower()
    else:
        raise AssertionError("fetch must be rejected")

    try:
        ResearchKnowledgeMapApiUnavailableResponse(
            reason="unsafe",
            execution_enabled=True,
        )
    except ValidationError as exc:
        assert "execution" in str(exc).lower()
    else:
        raise AssertionError("execution must be rejected")


def test_research_knowledge_map_api_safety_and_health_are_fail_closed() -> None:
    forbidden = research_knowledge_map_api_forbidden_actions()
    for phrase in [
        "active knowledge map",
        "database",
        "persistent writes",
        "traversal",
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
        assert_no_knowledge_map_api_database_enabled,
        assert_no_knowledge_map_api_persistent_writes_enabled,
        assert_no_knowledge_map_api_traversal_enabled,
        assert_no_knowledge_map_api_search_enabled,
        assert_no_knowledge_map_api_ranking_enabled,
        assert_no_knowledge_map_api_retrieval_enabled,
        assert_no_knowledge_map_api_embeddings_enabled,
        assert_no_knowledge_map_api_vector_store_enabled,
        assert_no_knowledge_map_api_paper_parsing_enabled,
        assert_no_knowledge_map_api_strategy_generation_enabled,
        assert_no_knowledge_map_api_backtesting_enabled,
        assert_no_knowledge_map_api_recommendation_enabled,
        assert_no_knowledge_map_api_execution_enabled,
    ]
    for helper in helpers:
        result = helper(True)
        assert result.blocked is True
        assert result.safe is False
        assert result.allowed is False

    health = research_knowledge_map_api_health()
    assert health.service == "stark-terminal-research-knowledge-map-api"
    assert health.stage == "api_contract_skeleton"
    assert health.api_contract_skeleton_only is True
    assert health.read_only is True
    assert health.unavailable_by_default is True
    assert health.database_enabled is False
    assert health.persistent_writes_enabled is False
    assert health.traversal_enabled is False
    assert health.search_enabled is False
    assert health.ranking_enabled is False
    assert health.retrieval_enabled is False
    assert health.embeddings_enabled is False
    assert health.vector_store_enabled is False
    assert health.active_ingestion_enabled is False
    assert health.file_uploads_enabled is False
    assert health.file_downloads_enabled is False
    assert health.file_previews_enabled is False
    assert health.paper_parsing_enabled is False
    assert health.strategy_generation_enabled is False
    assert health.backtesting_enabled is False
    assert health.recommendations_enabled is False
    assert health.execution_enabled is False
