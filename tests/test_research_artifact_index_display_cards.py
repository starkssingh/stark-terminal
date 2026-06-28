from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.types import ResearchArtifactIndexKind
from stark_terminal_core.research_artifact_index_display.cards import (
    ResearchArtifactIndexCardPlaceholder,
    default_research_artifact_index_card_placeholder,
    default_research_artifact_index_metadata_card_placeholder,
    default_research_artifact_index_reference_card_placeholder,
    default_research_artifact_index_tag_card_placeholder,
)


def test_research_artifact_index_display_card_placeholders_validate() -> None:
    for placeholder in [
        default_research_artifact_index_card_placeholder(),
        default_research_artifact_index_metadata_card_placeholder(),
        default_research_artifact_index_reference_card_placeholder(),
        default_research_artifact_index_tag_card_placeholder(),
    ]:
        assert placeholder.display_contract_skeleton_only is True
        for field_name in [
            "active_ui",
            "frontend_component",
            "desktop_widget",
            "file_content_preview",
            "indexed_artifact_records_present",
            "search_results_present",
            "ranking_results_present",
            "retrieval_results_present",
            "embeddings_present",
            "vector_ids_present",
            "parsed_paper_content",
            "generated_strategy_content",
            "backtest_metrics_present",
            "recommendation_fields_present",
            "action_fields_present",
            "confidence_fields_present",
            "execution_controls_present",
        ]:
            assert getattr(placeholder, field_name) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui",
        "frontend_component",
        "desktop_widget",
        "file_content_preview",
        "indexed_artifact_records_present",
        "search_results_present",
        "ranking_results_present",
        "retrieval_results_present",
        "embeddings_present",
        "vector_ids_present",
        "parsed_paper_content",
        "generated_strategy_content",
        "backtest_metrics_present",
        "recommendation_fields_present",
        "action_fields_present",
        "confidence_fields_present",
        "execution_controls_present",
    ],
)
def test_research_artifact_index_display_card_rejects_active_or_generated_fields(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexCardPlaceholder(card_id="card", title="Card", **{field_name: True})


def test_research_artifact_index_display_card_rejects_unknown_index_kind() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexCardPlaceholder(
            card_id="card",
            title="Card",
            index_kind=ResearchArtifactIndexKind.UNKNOWN,
        )


def test_research_artifact_index_display_card_has_no_active_content_fields() -> None:
    fields = set(ResearchArtifactIndexCardPlaceholder.model_fields)

    for forbidden in [
        "file_contents",
        "parsed_paper_text",
        "strategy_logic",
        "backtest_metrics",
        "recommendation_text",
        "confidence_score",
        "execution_control",
        "frontend_component_path",
        "desktop_widget_class",
    ]:
        assert forbidden not in fields
