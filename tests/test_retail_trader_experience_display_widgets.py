from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplayWidgetKind,
)
from stark_terminal_core.retail_trader_experience_display.widgets import (
    RetailTraderExperienceDisplayWidgetPlaceholder,
    default_retail_trader_experience_display_widget_placeholders,
)


def _widget_kwargs(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "widget_id": "widget-test",
        "widget_kind": RetailTraderExperienceDisplayWidgetKind.PLACEHOLDER,
        "title": "Widget test",
        "description": "Display placeholder only.",
    }
    values.update(overrides)
    return values


def test_retail_trader_experience_display_widget_placeholder_validates() -> None:
    widget = RetailTraderExperienceDisplayWidgetPlaceholder(**_widget_kwargs())

    assert widget.display_contract_only is True
    assert widget.active_ui is False
    assert widget.rendered_now is False
    assert widget.unavailable is True
    assert widget.execution_widget is False


@pytest.mark.parametrize(
    "field",
    [
        "active_ui",
        "rendered_now",
        "unavailable",
        "display_contract_only",
        "recommendation_widget",
        "action_widget",
        "confidence_widget",
        "decision_object_widget",
        "readiness_to_trade_widget",
        "broker_control_widget",
        "execution_widget",
        "approval_widget",
        "override_widget",
        "suitability_profile_widget",
    ],
)
def test_retail_trader_experience_display_widget_rejects_unsafe_flags(field: str) -> None:
    value = False if field in {"display_contract_only", "unavailable"} else True
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayWidgetPlaceholder(**_widget_kwargs(**{field: value}))


def test_retail_trader_experience_display_widget_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayWidgetPlaceholder(
            **_widget_kwargs(widget_kind=RetailTraderExperienceDisplayWidgetKind.UNKNOWN)
        )


def test_default_retail_trader_experience_display_widgets_validate() -> None:
    widgets = default_retail_trader_experience_display_widget_placeholders()

    assert len(widgets) >= 10
    assert all(widget.display_contract_only for widget in widgets)
    assert all(widget.unavailable for widget in widgets)
