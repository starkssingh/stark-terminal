from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_display.contracts import RetailDashboardLayoutKind
from stark_terminal_core.retail_dashboard_display.layouts import (
    RetailDashboardLayoutPlaceholder,
    default_retail_dashboard_layout_placeholders,
)


def _layout(**overrides: object) -> RetailDashboardLayoutPlaceholder:
    data = {
        "layout_id": "retail-dashboard-display-layout-test",
        "layout_kind": RetailDashboardLayoutKind.RETAIL_OVERVIEW_PLACEHOLDER,
        "title": "Layout test",
        "description": "Display contract placeholder layout.",
    }
    data.update(overrides)
    return RetailDashboardLayoutPlaceholder(**data)


def test_retail_dashboard_display_layout_placeholder_validates() -> None:
    layout = _layout()

    assert layout.active_ui is False
    assert layout.rendered_now is False
    assert layout.unavailable is True
    assert layout.display_contract_only is True


def test_retail_dashboard_display_layout_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _layout(layout_kind=RetailDashboardLayoutKind.UNKNOWN)


@pytest.mark.parametrize("field_name", ["active_ui", "rendered_now"])
def test_retail_dashboard_display_layout_enforces_false_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _layout(**{field_name: True})


@pytest.mark.parametrize("field_name", ["unavailable", "display_contract_only"])
def test_retail_dashboard_display_layout_enforces_true_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _layout(**{field_name: False})


@pytest.mark.parametrize(
    "field_name",
    [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
    ],
)
def test_retail_dashboard_display_layout_rejects_dangerous_allowed_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _layout(**{field_name: True})


def test_default_retail_dashboard_display_layouts_validate() -> None:
    layouts = default_retail_dashboard_layout_placeholders()

    assert layouts
    assert all(layout.active_ui is False for layout in layouts)
    assert all(layout.rendered_now is False for layout in layouts)
    assert all(layout.unavailable is True for layout in layouts)
