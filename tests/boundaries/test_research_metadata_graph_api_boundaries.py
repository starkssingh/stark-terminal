from pydantic import ValidationError

from stark_terminal_core.research_metadata_graph_api.contracts import (
    ResearchMetadataGraphApiContract,
    default_research_metadata_graph_api_contract,
)
from stark_terminal_core.research_metadata_graph_api.health import (
    research_metadata_graph_api_health,
)
from stark_terminal_core.research_metadata_graph_api.references import (
    GraphApiReferencePlaceholder,
    default_graph_api_edge_reference_placeholder,
    default_graph_api_node_reference_placeholder,
    default_graph_api_provenance_reference_placeholder,
    default_graph_api_reference_placeholder,
)
from stark_terminal_core.research_metadata_graph_api.requests import (
    GraphNodeLookupRequestPlaceholder,
    default_graph_edge_lookup_request_placeholder,
    default_graph_node_lookup_request_placeholder,
    default_graph_provenance_request_placeholder,
    default_graph_relationship_request_placeholder,
    default_research_metadata_graph_request_placeholder,
)
from stark_terminal_core.research_metadata_graph_api.responses import (
    GraphNodeResponsePlaceholder,
    default_graph_edge_response_placeholder,
    default_graph_node_response_placeholder,
    default_graph_provenance_response_placeholder,
    default_graph_relationship_response_placeholder,
    default_research_metadata_graph_response_placeholder,
)
from stark_terminal_core.research_metadata_graph_api.safety import (
    assert_no_graph_api_backtesting_enabled,
    assert_no_graph_api_database_enabled,
    assert_no_graph_api_embeddings_enabled,
    assert_no_graph_api_execution_enabled,
    assert_no_graph_api_ingestion_enabled,
    assert_no_graph_api_paper_parsing_enabled,
    assert_no_graph_api_persistent_writes_enabled,
    assert_no_graph_api_ranking_enabled,
    assert_no_graph_api_recommendation_enabled,
    assert_no_graph_api_retrieval_enabled,
    assert_no_graph_api_search_enabled,
    assert_no_graph_api_strategy_generation_enabled,
    assert_no_graph_api_traversal_enabled,
    assert_no_graph_api_upload_download_preview_enabled,
    assert_no_graph_api_vector_store_enabled,
    research_metadata_graph_api_forbidden_actions,
)
from stark_terminal_core.research_metadata_graph_api.unavailable import (
    ResearchMetadataGraphApiUnavailableResponse,
    unavailable_graph_api_response_template,
)


def test_research_metadata_graph_api_contract_validates_and_blocks_dangerous_flags() -> None:
    contract = default_research_metadata_graph_api_contract()
    assert contract.service == "stark-terminal-research-metadata-graph-api"
    assert contract.stage == "api_contract_skeleton"
    assert contract.read_only is True
    assert contract.unavailable_by_default is True
    assert contract.api_contract_skeleton_only is True
    assert contract.graph_database_enabled is False
    assert contract.graph_traversal_enabled is False
    assert contract.graph_search_enabled is False
    assert contract.graph_ranking_enabled is False
    assert contract.graph_retrieval_enabled is False
    assert contract.embeddings_enabled is False
    assert contract.vector_store_enabled is False
    assert contract.execution_enabled is False

    try:
        ResearchMetadataGraphApiContract(
            contract_id="unsafe",
            graph_database_enabled=True,
        )
    except ValidationError as exc:
        assert "graph database" in str(exc).lower()
    else:
        raise AssertionError("graph database must be rejected")


def test_research_metadata_graph_api_request_placeholders_validate_without_active_behavior() -> None:
    requests = [
        default_research_metadata_graph_request_placeholder(),
        default_graph_node_lookup_request_placeholder(),
        default_graph_edge_lookup_request_placeholder(),
        default_graph_relationship_request_placeholder(),
        default_graph_provenance_request_placeholder(),
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
        GraphNodeLookupRequestPlaceholder(
            request_id="unsafe-request",
            lookup_trigger_enabled=True,
        )
    except ValidationError as exc:
        assert "lookup trigger" in str(exc).lower()
    else:
        raise AssertionError("lookup trigger must be rejected")


def test_research_metadata_graph_api_response_placeholders_validate_without_outputs() -> None:
    responses = [
        default_research_metadata_graph_response_placeholder(),
        default_graph_node_response_placeholder(),
        default_graph_edge_response_placeholder(),
        default_graph_relationship_response_placeholder(),
        default_graph_provenance_response_placeholder(),
    ]

    assert all(item.unavailable_by_default and item.placeholder_only for item in responses)
    assert all(not item.retrieved_graph_data_present for item in responses)
    assert all(not item.search_results_present for item in responses)
    assert all(not item.rankings_present for item in responses)
    assert all(not item.embeddings_present for item in responses)
    assert all(not item.parsed_paper_content_present for item in responses)
    assert all(not item.generated_strategies_present for item in responses)
    assert all(not item.backtest_results_present for item in responses)
    assert all(not item.recommendations_present for item in responses)
    assert all(not item.execution_controls_present for item in responses)

    try:
        GraphNodeResponsePlaceholder(
            response_id="unsafe-response",
            retrieved_graph_data_present=True,
        )
    except ValidationError as exc:
        assert "retrieved graph data" in str(exc).lower()
    else:
        raise AssertionError("retrieved graph data must be rejected")


def test_research_metadata_graph_api_reference_and_unavailable_placeholders_validate() -> None:
    references = [
        default_graph_api_reference_placeholder(),
        default_graph_api_node_reference_placeholder(),
        default_graph_api_edge_reference_placeholder(),
        default_graph_api_provenance_reference_placeholder(),
    ]
    unavailable = unavailable_graph_api_response_template()

    assert all(item.descriptive_only for item in references)
    assert all(not item.fetch_enabled for item in references)
    assert all(not item.retrieval_enabled for item in references)
    assert all(not item.source_truth_validation_enabled for item in references)
    assert all(not item.graph_persistence_implied for item in references)
    assert unavailable.unavailable is True
    assert unavailable.allowed_stage == "api_contract_skeleton"
    assert unavailable.graph_database_enabled is False
    assert unavailable.graph_retrieval_enabled is False
    assert unavailable.execution_enabled is False

    try:
        GraphApiReferencePlaceholder(
            reference_id="unsafe-reference",
            reference_kind="UNSAFE",
            fetch_enabled=True,
        )
    except ValidationError as exc:
        assert "fetch" in str(exc).lower()
    else:
        raise AssertionError("fetch must be rejected")

    try:
        ResearchMetadataGraphApiUnavailableResponse(
            reason="unsafe",
            execution_enabled=True,
        )
    except ValidationError as exc:
        assert "execution" in str(exc).lower()
    else:
        raise AssertionError("execution must be rejected")


def test_research_metadata_graph_api_safety_and_health_are_fail_closed() -> None:
    forbidden = research_metadata_graph_api_forbidden_actions()
    for phrase in [
        "graph database",
        "persistent graph writes",
        "graph traversal",
        "graph search",
        "graph ranking",
        "graph retrieval",
        "embeddings",
        "vector store",
        "active ingestion",
        "file upload",
        "file download",
        "file preview",
        "paper parsing",
        "strategy generation",
        "backtesting",
        "recommendation generation",
        "execution",
    ]:
        assert phrase in forbidden

    helpers = [
        assert_no_graph_api_database_enabled,
        assert_no_graph_api_persistent_writes_enabled,
        assert_no_graph_api_traversal_enabled,
        assert_no_graph_api_search_enabled,
        assert_no_graph_api_ranking_enabled,
        assert_no_graph_api_retrieval_enabled,
        assert_no_graph_api_embeddings_enabled,
        assert_no_graph_api_vector_store_enabled,
        assert_no_graph_api_ingestion_enabled,
        assert_no_graph_api_upload_download_preview_enabled,
        assert_no_graph_api_paper_parsing_enabled,
        assert_no_graph_api_strategy_generation_enabled,
        assert_no_graph_api_backtesting_enabled,
        assert_no_graph_api_recommendation_enabled,
        assert_no_graph_api_execution_enabled,
    ]
    for helper in helpers:
        result = helper(True)
        assert result.blocked is True
        assert result.safe is False
        assert result.allowed is False

    health = research_metadata_graph_api_health()
    assert health.service == "stark-terminal-research-metadata-graph-api"
    assert health.stage == "api_contract_skeleton"
    assert health.api_contract_skeleton_only is True
    assert health.read_only is True
    assert health.unavailable_by_default is True
    assert health.graph_database_enabled is False
    assert health.graph_traversal_enabled is False
    assert health.graph_search_enabled is False
    assert health.graph_ranking_enabled is False
    assert health.graph_retrieval_enabled is False
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
