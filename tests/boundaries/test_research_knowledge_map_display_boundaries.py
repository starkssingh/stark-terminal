from pydantic import ValidationError

from stark_terminal_core.research_knowledge_map_display.contracts import (
    ResearchKnowledgeMapDisplayContract,
    default_research_knowledge_map_display_contract,
)
from stark_terminal_core.research_knowledge_map_display.evidence import (
    KnowledgeMapEvidenceDisplayPlaceholder,
    default_knowledge_map_evidence_display_placeholder,
    default_knowledge_map_evidence_reference_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.health import (
    research_knowledge_map_display_health,
)
from stark_terminal_core.research_knowledge_map_display.items import (
    KnowledgeMapItemDisplayPlaceholder,
    default_knowledge_map_item_display_placeholders,
    default_research_knowledge_map_item_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.lifecycle import (
    KnowledgeMapLifecycleDisplayPlaceholder,
    default_knowledge_map_lifecycle_badge_placeholder,
    default_knowledge_map_lifecycle_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.provenance import (
    KnowledgeMapProvenanceDisplayPlaceholder,
    default_knowledge_map_audit_display_placeholder,
    default_knowledge_map_provenance_display_placeholder,
    default_knowledge_map_source_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.relationships import (
    KnowledgeMapRelationshipDisplayPlaceholder,
    default_knowledge_map_relationship_display_placeholders,
    default_research_knowledge_map_relationship_display_placeholder,
)
from stark_terminal_core.research_knowledge_map_display.safety import (
    assert_no_knowledge_map_display_active_ui_enabled,
    assert_no_knowledge_map_display_backtesting_enabled,
    assert_no_knowledge_map_display_database_enabled,
    assert_no_knowledge_map_display_desktop_components_enabled,
    assert_no_knowledge_map_display_embeddings_enabled,
    assert_no_knowledge_map_display_execution_enabled,
    assert_no_knowledge_map_display_frontend_components_enabled,
    assert_no_knowledge_map_display_paper_parsing_enabled,
    assert_no_knowledge_map_display_persistent_writes_enabled,
    assert_no_knowledge_map_display_ranking_enabled,
    assert_no_knowledge_map_display_recommendation_enabled,
    assert_no_knowledge_map_display_retrieval_enabled,
    assert_no_knowledge_map_display_search_enabled,
    assert_no_knowledge_map_display_strategy_generation_enabled,
    assert_no_knowledge_map_display_traversal_enabled,
    assert_no_knowledge_map_display_vector_store_enabled,
    research_knowledge_map_display_forbidden_actions,
)
from stark_terminal_core.research_knowledge_map_display.unavailable import (
    ResearchKnowledgeMapDisplayUnavailableResponse,
    unavailable_knowledge_map_display_response_template,
)


def test_research_knowledge_map_display_contract_validates_and_blocks_dangerous_flags() -> None:
    contract = default_research_knowledge_map_display_contract()
    assert contract.service == "stark-terminal-research-knowledge-map-display"
    assert contract.stage == "display_contract_skeleton"
    assert contract.display_contract_skeleton_only is True
    assert contract.read_only is True
    assert contract.unavailable_by_default is True
    assert contract.active_ui_enabled is False
    assert contract.frontend_components_enabled is False
    assert contract.desktop_components_enabled is False
    assert contract.active_map_enabled is False
    assert contract.database_enabled is False
    assert contract.traversal_enabled is False
    assert contract.search_enabled is False
    assert contract.ranking_enabled is False
    assert contract.retrieval_enabled is False
    assert contract.embeddings_enabled is False
    assert contract.vector_store_enabled is False
    assert contract.execution_enabled is False

    try:
        ResearchKnowledgeMapDisplayContract(
            contract_id="unsafe",
            active_ui_enabled=True,
        )
    except ValidationError as exc:
        assert "active ui" in str(exc).lower()
    else:
        raise AssertionError("active UI must be rejected")


def test_research_knowledge_map_display_item_placeholders_validate_without_active_ui_or_retrieval() -> None:
    placeholders = [
        default_research_knowledge_map_item_display_placeholder(),
        *default_knowledge_map_item_display_placeholders().values(),
    ]
    assert all(item.display_metadata_only for item in placeholders)
    assert all(not item.active_ui_rendering_enabled for item in placeholders)
    assert all(not item.database_query_enabled for item in placeholders)
    assert all(not item.knowledge_map_data_retrieval_enabled for item in placeholders)
    assert all(not item.search_results_display_enabled for item in placeholders)
    assert all(not item.rankings_display_enabled for item in placeholders)
    assert all(not item.embeddings_display_enabled for item in placeholders)
    assert all(not item.recommendations_display_enabled for item in placeholders)
    assert all(not item.execution_controls_display_enabled for item in placeholders)

    try:
        KnowledgeMapItemDisplayPlaceholder(
            placeholder_id="unsafe-item",
            item_kind="UNSAFE",
            display_label="Unsafe",
            knowledge_map_data_retrieval_enabled=True,
        )
    except ValidationError as exc:
        assert "retrieval" in str(exc).lower()
    else:
        raise AssertionError("retrieval display must be rejected")


def test_research_knowledge_map_display_relationship_placeholders_validate_without_traversal_or_ranking() -> None:
    placeholders = [
        default_research_knowledge_map_relationship_display_placeholder(),
        *default_knowledge_map_relationship_display_placeholders().values(),
    ]
    assert all(item.descriptive_only for item in placeholders)
    assert all(not item.traversal_enabled for item in placeholders)
    assert all(not item.relationship_ranking_enabled for item in placeholders)
    assert all(not item.artifact_retrieval_enabled for item in placeholders)
    assert all(not item.strategy_quality_inference_enabled for item in placeholders)
    assert all(not item.recommendation_implied for item in placeholders)

    try:
        KnowledgeMapRelationshipDisplayPlaceholder(
            placeholder_id="unsafe-relationship",
            relationship_kind="UNSAFE",
            display_label="Unsafe",
            relationship_ranking_enabled=True,
        )
    except ValidationError as exc:
        assert "ranking" in str(exc).lower()
    else:
        raise AssertionError("relationship ranking must be rejected")


def test_research_knowledge_map_display_evidence_provenance_lifecycle_unavailable_validate() -> None:
    evidence = default_knowledge_map_evidence_display_placeholder()
    evidence_reference = default_knowledge_map_evidence_reference_display_placeholder()
    provenance = default_knowledge_map_provenance_display_placeholder()
    source = default_knowledge_map_source_display_placeholder()
    audit = default_knowledge_map_audit_display_placeholder()
    lifecycle = default_knowledge_map_lifecycle_display_placeholder()
    badge = default_knowledge_map_lifecycle_badge_placeholder()
    unavailable = unavailable_knowledge_map_display_response_template()

    assert evidence.descriptive_only and evidence_reference.descriptive_only
    assert not evidence.truth_validation_enabled
    assert not evidence.research_approval_enabled
    assert not evidence.trade_readiness_enabled
    assert not evidence.decision_generation_enabled
    assert provenance.descriptive_only and source.descriptive_only and audit.descriptive_only
    assert not provenance.external_fetch_enabled
    assert not provenance.local_file_read_enabled
    assert not provenance.source_validation_enabled
    assert not provenance.trusted_research_status_implied
    assert lifecycle.descriptive_only and badge.descriptive_only
    assert not lifecycle.searchable
    assert not lifecycle.retrieved
    assert not lifecycle.recommended
    assert not lifecycle.ready_to_trade
    assert unavailable.unavailable is True
    assert unavailable.allowed_stage == "display_contract_skeleton"
    assert unavailable.active_ui_enabled is False
    assert unavailable.execution_enabled is False

    for model, kwargs, expected in [
        (KnowledgeMapEvidenceDisplayPlaceholder, {"truth_validation_enabled": True}, "truth validation"),
        (KnowledgeMapProvenanceDisplayPlaceholder, {"external_fetch_enabled": True}, "external fetch"),
        (KnowledgeMapLifecycleDisplayPlaceholder, {"ready_to_trade": True}, "ready-to-trade"),
        (ResearchKnowledgeMapDisplayUnavailableResponse, {"execution_enabled": True}, "execution"),
    ]:
        try:
            if model is KnowledgeMapLifecycleDisplayPlaceholder:
                model(
                    lifecycle_display_id="unsafe-lifecycle",
                    state="PLANNED",
                    display_label="Unsafe",
                    **kwargs,
                )
            elif model is ResearchKnowledgeMapDisplayUnavailableResponse:
                model(reason="unsafe", **kwargs)
            elif model is KnowledgeMapEvidenceDisplayPlaceholder:
                model(evidence_display_id="unsafe-evidence", display_label="Unsafe", **kwargs)
            else:
                model(provenance_display_id="unsafe-provenance", display_label="Unsafe", **kwargs)
        except ValidationError as exc:
            assert expected in str(exc).lower()
        else:
            raise AssertionError(f"{expected} must be rejected")


def test_research_knowledge_map_display_safety_and_health_are_fail_closed() -> None:
    forbidden = research_knowledge_map_display_forbidden_actions()
    for phrase in [
        "active UI",
        "frontend components",
        "desktop components",
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
        assert_no_knowledge_map_display_active_ui_enabled,
        assert_no_knowledge_map_display_frontend_components_enabled,
        assert_no_knowledge_map_display_desktop_components_enabled,
        assert_no_knowledge_map_display_database_enabled,
        assert_no_knowledge_map_display_persistent_writes_enabled,
        assert_no_knowledge_map_display_traversal_enabled,
        assert_no_knowledge_map_display_search_enabled,
        assert_no_knowledge_map_display_ranking_enabled,
        assert_no_knowledge_map_display_retrieval_enabled,
        assert_no_knowledge_map_display_embeddings_enabled,
        assert_no_knowledge_map_display_vector_store_enabled,
        assert_no_knowledge_map_display_paper_parsing_enabled,
        assert_no_knowledge_map_display_strategy_generation_enabled,
        assert_no_knowledge_map_display_backtesting_enabled,
        assert_no_knowledge_map_display_recommendation_enabled,
        assert_no_knowledge_map_display_execution_enabled,
    ]
    for helper in helpers:
        result = helper(True)
        assert result.blocked is True
        assert result.safe is False
        assert result.allowed is False

    health = research_knowledge_map_display_health()
    assert health.service == "stark-terminal-research-knowledge-map-display"
    assert health.stage == "display_contract_skeleton"
    assert health.display_contract_skeleton_only is True
    assert health.read_only is True
    assert health.unavailable_by_default is True
    assert health.active_ui_enabled is False
    assert health.frontend_components_enabled is False
    assert health.desktop_components_enabled is False
    assert health.active_map_enabled is False
    assert health.database_enabled is False
    assert health.traversal_enabled is False
    assert health.search_enabled is False
    assert health.ranking_enabled is False
    assert health.retrieval_enabled is False
    assert health.embeddings_enabled is False
    assert health.vector_store_enabled is False
    assert health.execution_enabled is False
