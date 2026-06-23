from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_display.contracts import RetailDashboardWidgetKind
from stark_terminal_core.retail_dashboard_display.widgets import (
    RetailDashboardWidgetPlaceholder,
    default_retail_dashboard_widget_placeholders,
)


def _widget(**overrides: object) -> RetailDashboardWidgetPlaceholder:
    data = {
        "widget_id": "retail-dashboard-display-widget-test",
        "widget_kind": RetailDashboardWidgetKind.PLACEHOLDER,
        "title": "Widget test",
        "description": "Display contract placeholder widget.",
    }
    data.update(overrides)
    return RetailDashboardWidgetPlaceholder(**data)


def test_retail_dashboard_display_widget_placeholder_validates() -> None:
    widget = _widget()

    assert widget.active_ui is False
    assert widget.rendered_now is False
    assert widget.unavailable is True
    assert widget.display_contract_only is True
    assert widget.recommendation_widget is False


def test_retail_dashboard_display_widget_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _widget(widget_kind=RetailDashboardWidgetKind.UNKNOWN)


@pytest.mark.parametrize("field_name", ["active_ui", "rendered_now"])
def test_retail_dashboard_display_widget_enforces_false_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _widget(**{field_name: True})


@pytest.mark.parametrize("field_name", ["unavailable", "display_contract_only"])
def test_retail_dashboard_display_widget_enforces_true_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _widget(**{field_name: False})


@pytest.mark.parametrize(
    "field_name",
    [
        "recommendation_widget",
        "action_widget",
        "confidence_widget",
        "decision_object_widget",
        "readiness_to_trade_widget",
        "broker_control_widget",
        "execution_widget",
        "approval_widget",
        "override_widget",
    ],
)
def test_retail_dashboard_display_widget_rejects_dangerous_widget_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _widget(**{field_name: True})


def test_default_retail_dashboard_display_widgets_validate() -> None:
    widgets = default_retail_dashboard_widget_placeholders()

    assert widgets
    assert all(widget.active_ui is False for widget in widgets)
    assert all(widget.rendered_now is False for widget in widgets)
    assert all(widget.unavailable is True for widget in widgets)
