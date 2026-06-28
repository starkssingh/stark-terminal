from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.types import ResearchArtifactKind
from stark_terminal_core.research_artifact_registry_display.cards import (
    ResearchArtifactCardPlaceholder,
    default_research_artifact_card_placeholder,
    default_research_artifact_metadata_card_placeholder,
    default_research_artifact_reference_card_placeholder,
)


def test_display_card_placeholders_validate() -> None:
    card = default_research_artifact_card_placeholder()
    metadata = default_research_artifact_metadata_card_placeholder()
    reference = default_research_artifact_reference_card_placeholder()

    for placeholder in [card, metadata, reference]:
        assert placeholder.display_contract_skeleton_only is True
        assert placeholder.active_ui is False
        assert placeholder.frontend_component is False
        assert placeholder.desktop_widget is False
        assert placeholder.file_content_preview is False
        assert placeholder.parsed_paper_content is False
        assert placeholder.generated_strategy_content is False
        assert placeholder.backtest_metrics_present is False
        assert placeholder.recommendation_fields_present is False
        assert placeholder.action_fields_present is False
        assert placeholder.confidence_fields_present is False
        assert placeholder.execution_controls_present is False


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui",
        "frontend_component",
        "desktop_widget",
        "file_content_preview",
        "parsed_paper_content",
        "generated_strategy_content",
        "backtest_metrics_present",
        "recommendation_fields_present",
        "action_fields_present",
        "confidence_fields_present",
        "execution_controls_present",
    ],
)
def test_display_card_rejects_active_or_generated_fields(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactCardPlaceholder(card_id="card", title="Card", **{field_name: True})


def test_display_card_rejects_unknown_artifact_kind() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactCardPlaceholder(
            card_id="card",
            title="Card",
            artifact_kind=ResearchArtifactKind.UNKNOWN,
        )


def test_display_card_has_no_content_preview_or_decision_fields() -> None:
    fields = set(ResearchArtifactCardPlaceholder.model_fields)

    assert "file_contents" not in fields
    assert "parsed_paper_text" not in fields
    assert "strategy_logic" not in fields
    assert "backtest_metrics" not in fields
    assert "recommendation_text" not in fields
    assert "confidence_score" not in fields
    assert "execution_control" not in fields
