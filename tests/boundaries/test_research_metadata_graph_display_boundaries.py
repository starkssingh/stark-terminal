from pydantic import ValidationError

from stark_terminal_core.research_metadata_graph_display.contracts import (
    ResearchMetadataGraphDisplayContract,
    default_research_metadata_graph_display_contract,
)
from stark_terminal_core.research_metadata_graph_display.edges import (
    ResearchMetadataGraphEdgeDisplayPlaceholder,
    default_graph_edge_display_placeholders,
    default_research_metadata_graph_edge_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.health import (
    research_metadata_graph_display_health,
)
from stark_terminal_core.research_metadata_graph_display.lifecycle import (
    GraphLifecycleDisplayPlaceholder,
    default_graph_lifecycle_badge_placeholder,
    default_graph_lifecycle_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.nodes import (
    ResearchMetadataGraphNodeDisplayPlaceholder,
    default_graph_node_display_placeholders,
    default_research_metadata_graph_node_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.provenance import (
    GraphProvenanceDisplayPlaceholder,
    default_graph_audit_display_placeholder,
    default_graph_provenance_display_placeholder,
    default_graph_source_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.references import (
    GraphReferenceDisplayPlaceholder,
    default_graph_dependency_reference_display_placeholder,
    default_graph_reference_display_placeholder,
    default_graph_relationship_reference_display_placeholder,
)
from stark_terminal_core.research_metadata_graph_display.safety import (
    assert_no_graph_display_active_ui_enabled,
    assert_no_graph_display_backtesting_enabled,
    assert_no_graph_display_database_enabled,
    assert_no_graph_display_desktop_components_enabled,
    assert_no_graph_display_embeddings_enabled,
    assert_no_graph_display_execution_enabled,
    assert_no_graph_display_frontend_components_enabled,
    assert_no_graph_display_ingestion_enabled,
    assert_no_graph_display_paper_parsing_enabled,
    assert_no_graph_display_persistent_writes_enabled,
    assert_no_graph_display_ranking_enabled,
    assert_no_graph_display_recommendation_enabled,
    assert_no_graph_display_retrieval_enabled,
    assert_no_graph_display_search_enabled,
    assert_no_graph_display_strategy_generation_enabled,
    assert_no_graph_display_traversal_enabled,
    assert_no_graph_display_upload_download_preview_enabled,
    assert_no_graph_display_vector_store_enabled,
    research_metadata_graph_display_forbidden_actions,
)
from stark_terminal_core.research_metadata_graph_display.unavailable import (
    ResearchMetadataGraphDisplayUnavailableResponse,
    unavailable_graph_display_response_template,
)


def test_research_metadata_graph_display_contract_validates_and_blocks_dangerous_flags() -> None:
    contract = default_research_metadata_graph_display_contract()
    assert contract.service == "stark-terminal-research-metadata-graph-display"
    assert contract.stage == "display_contract_skeleton"
    assert contract.read_only is True
    assert contract.unavailable_by_default is True
    assert contract.display_contract_skeleton_only is True
    assert contract.active_ui_enabled is False
    assert contract.frontend_components_enabled is False
    assert contract.desktop_components_enabled is False
    assert contract.graph_database_enabled is False
    assert contract.graph_traversal_enabled is False
    assert contract.graph_search_enabled is False
    assert contract.graph_ranking_enabled is False
    assert contract.graph_retrieval_enabled is False
    assert contract.embeddings_enabled is False
    assert contract.vector_store_enabled is False
    assert contract.execution_enabled is False

    try:
        ResearchMetadataGraphDisplayContract(
            contract_id="unsafe",
            active_ui_enabled=True,
        )
    except ValidationError as exc:
        assert "active ui" in str(exc).lower()
    else:
        raise AssertionError("active UI must be rejected")


def test_research_metadata_graph_display_placeholders_validate_without_active_outputs() -> None:
    node = default_research_metadata_graph_node_display_placeholder()
    nodes = list(default_graph_node_display_placeholders().values())
    edge = default_research_metadata_graph_edge_display_placeholder()
    edges = list(default_graph_edge_display_placeholders().values())

    assert node.display_metadata_only is True
    assert all(item.display_metadata_only for item in nodes)
    assert all(not item.active_ui_rendering_enabled for item in [node, *nodes])
    assert all(not item.graph_database_query_enabled for item in [node, *nodes])
    assert all(not item.graph_data_retrieval_enabled for item in [node, *nodes])
    assert all(not item.search_results_display_enabled for item in [node, *nodes])
    assert all(not item.rankings_display_enabled for item in [node, *nodes])
    assert all(not item.embeddings_display_enabled for item in [node, *nodes])
    assert all(not item.parsed_paper_content_display_enabled for item in [node, *nodes])
    assert all(not item.generated_strategy_display_enabled for item in [node, *nodes])
    assert all(not item.backtest_results_display_enabled for item in [node, *nodes])
    assert all(not item.recommendations_display_enabled for item in [node, *nodes])
    assert all(not item.execution_controls_display_enabled for item in [node, *nodes])

    assert edge.descriptive_only is True
    assert all(item.descriptive_only for item in edges)
    assert all(not item.traversal_enabled for item in [edge, *edges])
    assert all(not item.relationship_ranking_enabled for item in [edge, *edges])
    assert all(not item.artifact_retrieval_enabled for item in [edge, *edges])
    assert all(not item.strategy_value_inference_enabled for item in [edge, *edges])
    assert all(not item.recommendation_implied for item in [edge, *edges])

    try:
        ResearchMetadataGraphNodeDisplayPlaceholder(
            placeholder_id="unsafe-node",
            node_kind="UNSAFE",
            display_label="Unsafe",
            graph_data_retrieval_enabled=True,
        )
    except ValidationError as exc:
        assert "graph data retrieval" in str(exc).lower()
    else:
        raise AssertionError("graph retrieval display must be rejected")

    try:
        ResearchMetadataGraphEdgeDisplayPlaceholder(
            placeholder_id="unsafe-edge",
            edge_kind="UNSAFE",
            display_label="Unsafe",
            relationship_ranking_enabled=True,
        )
    except ValidationError as exc:
        assert "relationship ranking" in str(exc).lower()
    else:
        raise AssertionError("relationship ranking must be rejected")


def test_research_metadata_graph_display_provenance_lifecycle_reference_and_unavailable_validate() -> None:
    provenance_items = [
        default_graph_provenance_display_placeholder(),
        default_graph_source_display_placeholder(),
        default_graph_audit_display_placeholder(),
    ]
    lifecycle = default_graph_lifecycle_display_placeholder()
    badge = default_graph_lifecycle_badge_placeholder()
    references = [
        default_graph_reference_display_placeholder(),
        default_graph_dependency_reference_display_placeholder(),
        default_graph_relationship_reference_display_placeholder(),
    ]
    unavailable = unavailable_graph_display_response_template()

    assert all(item.descriptive_only for item in provenance_items)
    assert all(not item.external_fetch_enabled for item in provenance_items)
    assert all(not item.local_file_read_enabled for item in provenance_items)
    assert lifecycle.descriptive_only is True
    assert lifecycle.ready_to_trade is False
    assert lifecycle.executable is False
    assert badge.descriptive_only is True
    assert all(item.descriptive_only for item in references)
    assert all(not item.lookup_enabled for item in references)
    assert all(not item.retrieval_enabled for item in references)
    assert all(not item.traversal_enabled for item in references)
    assert all(not item.search_enabled for item in references)
    assert all(not item.ranking_enabled for item in references)
    assert all(not item.file_access_enabled for item in references)
    assert all(not item.external_fetch_enabled for item in references)
    assert unavailable.unavailable is True
    assert unavailable.allowed_stage == "display_contract_skeleton"
    assert unavailable.active_ui_enabled is False
    assert unavailable.graph_retrieval_enabled is False
    assert unavailable.execution_enabled is False

    try:
        GraphProvenanceDisplayPlaceholder(
            placeholder_id="unsafe-provenance",
            provenance_kind="UNSAFE",
            display_label="Unsafe",
            external_fetch_enabled=True,
        )
    except ValidationError as exc:
        assert "external fetch" in str(exc).lower()
    else:
        raise AssertionError("external fetch must be rejected")

    try:
        GraphLifecycleDisplayPlaceholder(
            placeholder_id="unsafe-lifecycle",
            state="PLANNED",
            display_label="Unsafe",
            recommended=True,
        )
    except ValidationError as exc:
        assert "recommended" in str(exc).lower()
    else:
        raise AssertionError("recommended lifecycle meaning must be rejected")

    try:
        GraphReferenceDisplayPlaceholder(
            placeholder_id="unsafe-reference",
            reference_kind="UNSAFE",
            display_label="Unsafe",
            file_access_enabled=True,
        )
    except ValidationError as exc:
        assert "file access" in str(exc).lower()
    else:
        raise AssertionError("file access must be rejected")

    try:
        ResearchMetadataGraphDisplayUnavailableResponse(
            reason="unsafe",
            execution_enabled=True,
        )
    except ValidationError as exc:
        assert "execution" in str(exc).lower()
    else:
        raise AssertionError("execution must be rejected")


def test_research_metadata_graph_display_safety_and_health_are_fail_closed() -> None:
    forbidden = research_metadata_graph_display_forbidden_actions()
    for phrase in [
        "active UI",
        "frontend components",
        "desktop components",
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
        assert_no_graph_display_active_ui_enabled,
        assert_no_graph_display_frontend_components_enabled,
        assert_no_graph_display_desktop_components_enabled,
        assert_no_graph_display_database_enabled,
        assert_no_graph_display_persistent_writes_enabled,
        assert_no_graph_display_traversal_enabled,
        assert_no_graph_display_search_enabled,
        assert_no_graph_display_ranking_enabled,
        assert_no_graph_display_retrieval_enabled,
        assert_no_graph_display_embeddings_enabled,
        assert_no_graph_display_vector_store_enabled,
        assert_no_graph_display_ingestion_enabled,
        assert_no_graph_display_upload_download_preview_enabled,
        assert_no_graph_display_paper_parsing_enabled,
        assert_no_graph_display_strategy_generation_enabled,
        assert_no_graph_display_backtesting_enabled,
        assert_no_graph_display_recommendation_enabled,
        assert_no_graph_display_execution_enabled,
    ]
    for helper in helpers:
        result = helper(True)
        assert result.blocked is True
        assert result.safe is False
        assert result.allowed is False

    health = research_metadata_graph_display_health()
    assert health.service == "stark-terminal-research-metadata-graph-display"
    assert health.stage == "display_contract_skeleton"
    assert health.display_contract_skeleton_only is True
    assert health.read_only is True
    assert health.unavailable_by_default is True
    assert health.active_ui_enabled is False
    assert health.frontend_components_enabled is False
    assert health.desktop_components_enabled is False
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
