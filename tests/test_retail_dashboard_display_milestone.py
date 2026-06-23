from __future__ import annotations

from stark_terminal_core.retail_dashboard_display.badges import default_retail_dashboard_display_badges
from stark_terminal_core.retail_dashboard_display.contracts import (
    default_retail_dashboard_display_contract_metadata,
)
from stark_terminal_core.retail_dashboard_display.layouts import (
    default_retail_dashboard_layout_placeholders,
)
from stark_terminal_core.retail_dashboard_display.sections import (
    default_retail_dashboard_visual_section_placeholders,
)
from stark_terminal_core.retail_dashboard_display.widgets import (
    default_retail_dashboard_widget_placeholders,
)


def test_retail_dashboard_display_remains_contract_skeleton_only() -> None:
    metadata = default_retail_dashboard_display_contract_metadata()

    assert metadata.stage.value.lower() == "display_contract_skeleton"
    assert metadata.returns_unavailable_by_default is True
    assert metadata.active_ui_allowed is False
    assert metadata.recommendations_allowed is False
    assert metadata.action_generation_allowed is False
    assert metadata.confidence_scoring_allowed is False
    assert metadata.decision_object_generation_allowed is False
    assert metadata.readiness_to_trade_allowed is False
    assert metadata.broker_controls_allowed is False
    assert metadata.execution_allowed is False


def test_layout_widget_section_and_badge_placeholders_are_not_rendered_ui() -> None:
    for layout in default_retail_dashboard_layout_placeholders():
        assert layout.active_ui is False
        assert layout.rendered_now is False
        assert layout.unavailable is True
        assert layout.display_contract_only is True
        assert layout.execution_allowed is False

    for widget in default_retail_dashboard_widget_placeholders():
        assert widget.active_ui is False
        assert widget.rendered_now is False
        assert widget.unavailable is True
        assert widget.display_contract_only is True
        assert widget.recommendation_widget is False
        assert widget.action_widget is False
        assert widget.confidence_widget is False
        assert widget.decision_object_widget is False
        assert widget.readiness_to_trade_widget is False
        assert widget.broker_control_widget is False
        assert widget.execution_widget is False

    for section in default_retail_dashboard_visual_section_placeholders():
        assert section.active_ui is False
        assert section.rendered_now is False
        assert section.unavailable is True
        assert section.display_contract_only is True
        assert section.execution_allowed is False

    for badge in default_retail_dashboard_display_badges():
        assert badge.active_ui is False
        assert badge.unavailable is True
        assert badge.recommendation is False
        assert badge.action_signal is False
        assert badge.confidence_signal is False
        assert badge.decision_object_signal is False
        assert badge.readiness_to_trade is False
        assert badge.broker_control is False
        assert badge.execution_ready is False
