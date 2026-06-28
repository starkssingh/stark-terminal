from pydantic import ValidationError

from stark_terminal_core.research_metadata_graph.edges import (
    ResearchMetadataGraphEdgePlaceholder,
    ResearchMetadataGraphEdgeKind,
    default_research_metadata_graph_edge_placeholders,
)
from stark_terminal_core.research_metadata_graph.guardrails import (
    assert_no_graph_backtesting_enabled,
    assert_no_graph_database_enabled,
    assert_no_graph_embeddings_enabled,
    assert_no_graph_execution_enabled,
    assert_no_graph_ingestion_enabled,
    assert_no_graph_paper_parsing_enabled,
    assert_no_graph_persistent_writes_enabled,
    assert_no_graph_ranking_enabled,
    assert_no_graph_recommendation_enabled,
    assert_no_graph_retrieval_enabled,
    assert_no_graph_search_enabled,
    assert_no_graph_strategy_generation_enabled,
    assert_no_graph_traversal_enabled,
    assert_no_graph_upload_download_preview_enabled,
    assert_no_graph_vector_store_enabled,
    research_metadata_graph_forbidden_actions,
)
from stark_terminal_core.research_metadata_graph.lifecycle import (
    FORBIDDEN_LIFECYCLE_MEANINGS,
    GraphLifecycleState,
    default_graph_lifecycle_reference_placeholder,
)
from stark_terminal_core.research_metadata_graph.nodes import (
    ResearchMetadataGraphNodePlaceholder,
    ResearchMetadataGraphNodeKind,
    default_research_metadata_graph_node_placeholders,
)
from stark_terminal_core.research_metadata_graph.planning import (
    ResearchMetadataGraphPlanningContract,
    default_research_metadata_graph_planning_contract,
)
from stark_terminal_core.research_metadata_graph.provenance import (
    default_graph_provenance_reference_placeholders,
)
from stark_terminal_core.research_metadata_graph.readiness import (
    research_metadata_graph_readiness,
)
from stark_terminal_core.research_metadata_graph.references import (
    default_graph_reference_placeholders,
)


def test_research_metadata_graph_planning_contract_validates_and_blocks_dangerous_flags() -> None:
    contract = default_research_metadata_graph_planning_contract()
    assert contract.service == "stark-terminal-research-metadata-graph"
    assert contract.stage == "planning_and_guardrails"
    assert contract.read_only is True
    assert contract.unavailable_by_default is True
    assert contract.planning_only is True
    assert contract.graph_database_enabled is False
    assert contract.graph_traversal_enabled is False
    assert contract.graph_search_enabled is False
    assert contract.graph_retrieval_enabled is False
    assert contract.embeddings_enabled is False
    assert contract.vector_store_enabled is False
    assert contract.execution_enabled is False

    try:
        ResearchMetadataGraphPlanningContract(
            contract_id="unsafe",
            graph_database_enabled=True,
        )
    except ValidationError as exc:
        assert "graph database" in str(exc).lower()
    else:
        raise AssertionError("graph database must be rejected")


def test_research_metadata_graph_placeholders_validate_without_active_behavior() -> None:
    nodes = default_research_metadata_graph_node_placeholders()
    edges = default_research_metadata_graph_edge_placeholders()
    provenance = default_graph_provenance_reference_placeholders()
    lifecycle = default_graph_lifecycle_reference_placeholder()
    references = default_graph_reference_placeholders()

    assert {node.node_kind for node in nodes} == set(ResearchMetadataGraphNodeKind)
    assert {edge.edge_kind for edge in edges} == set(ResearchMetadataGraphEdgeKind)
    assert all(node.metadata_only and node.read_only for node in nodes)
    assert all(not node.persisted for node in nodes)
    assert all(not node.graph_database_query_enabled for node in nodes)
    assert all(not node.paper_content_parsing_enabled for node in nodes)
    assert all(edge.descriptive_only and edge.read_only for edge in edges)
    assert all(not edge.persisted for edge in edges)
    assert all(not edge.traversal_enabled for edge in edges)
    assert all(not edge.relationship_ranking_enabled for edge in edges)
    assert all(not edge.artifact_retrieval_enabled for edge in edges)
    assert all(item.descriptive_only for item in provenance)
    assert all(not item.external_fetch_enabled for item in provenance)
    assert all(not item.local_file_read_enabled for item in provenance)
    assert lifecycle.state == GraphLifecycleState.PLANNED
    assert not FORBIDDEN_LIFECYCLE_MEANINGS.intersection({state.value for state in GraphLifecycleState})
    assert lifecycle.indexed is False
    assert lifecycle.searchable is False
    assert lifecycle.recommended is False
    assert lifecycle.executable is False
    assert all(item.descriptive_only for item in references)
    assert all(not item.lookup_enabled for item in references)
    assert all(not item.graph_traversal_enabled for item in references)
    assert all(not item.graph_search_enabled for item in references)


def test_research_metadata_graph_placeholders_reject_active_behavior() -> None:
    try:
        ResearchMetadataGraphNodePlaceholder(
            node_id="unsafe-node",
            node_kind=ResearchMetadataGraphNodeKind.PAPER,
            label="Unsafe node",
            description="Unsafe node",
            paper_content_parsing_enabled=True,
        )
    except ValidationError as exc:
        assert "parse paper content" in str(exc).lower()
    else:
        raise AssertionError("paper parsing must be rejected")

    try:
        ResearchMetadataGraphEdgePlaceholder(
            edge_id="unsafe-edge",
            edge_kind=ResearchMetadataGraphEdgeKind.ARTIFACT_DEPENDENCY,
            label="Unsafe edge",
            description="Unsafe edge",
            traversal_enabled=True,
        )
    except ValidationError as exc:
        assert "traversal" in str(exc).lower()
    else:
        raise AssertionError("graph traversal must be rejected")


def test_research_metadata_graph_readiness_is_planning_only() -> None:
    readiness = research_metadata_graph_readiness()
    assert readiness.ready_for_planning is True
    assert readiness.ready_for_api_contract_skeleton is False
    assert readiness.ready_for_graph_database is False
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


def test_research_metadata_graph_guardrails_block_dangerous_behavior() -> None:
    forbidden = research_metadata_graph_forbidden_actions()
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
        assert_no_graph_database_enabled,
        assert_no_graph_persistent_writes_enabled,
        assert_no_graph_traversal_enabled,
        assert_no_graph_search_enabled,
        assert_no_graph_ranking_enabled,
        assert_no_graph_retrieval_enabled,
        assert_no_graph_embeddings_enabled,
        assert_no_graph_vector_store_enabled,
        assert_no_graph_ingestion_enabled,
        assert_no_graph_upload_download_preview_enabled,
        assert_no_graph_paper_parsing_enabled,
        assert_no_graph_strategy_generation_enabled,
        assert_no_graph_backtesting_enabled,
        assert_no_graph_recommendation_enabled,
        assert_no_graph_execution_enabled,
    ]
    for helper in helpers:
        result = helper(True)
        assert result.blocked is True
        assert result.safe is False
        assert result.allowed is False
