from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_display.contracts import RetailDashboardVisualSectionKind
from stark_terminal_core.retail_dashboard_display.sections import (
    RetailDashboardVisualSectionPlaceholder,
    default_retail_dashboard_visual_section_placeholders,
)


def _section(**overrides: object) -> RetailDashboardVisualSectionPlaceholder:
    data = {
        "section_id": "retail-dashboard-display-section-test",
        "section_kind": RetailDashboardVisualSectionKind.OVERVIEW,
        "title": "Section test",
        "description": "Display contract placeholder section.",
    }
    data.update(overrides)
    return RetailDashboardVisualSectionPlaceholder(**data)


def test_retail_dashboard_display_visual_section_placeholder_validates() -> None:
    section = _section()

    assert section.active_ui is False
    assert section.rendered_now is False
    assert section.unavailable is True
    assert section.display_contract_only is True


def test_retail_dashboard_display_visual_section_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _section(section_kind=RetailDashboardVisualSectionKind.UNKNOWN)


@pytest.mark.parametrize("field_name", ["active_ui", "rendered_now"])
def test_retail_dashboard_display_visual_section_enforces_false_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _section(**{field_name: True})


@pytest.mark.parametrize("field_name", ["unavailable", "display_contract_only"])
def test_retail_dashboard_display_visual_section_enforces_true_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _section(**{field_name: False})


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
def test_retail_dashboard_display_visual_section_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _section(**{field_name: True})


def test_default_retail_dashboard_display_visual_sections_validate() -> None:
    sections = default_retail_dashboard_visual_section_placeholders()

    assert sections
    assert all(section.active_ui is False for section in sections)
    assert all(section.rendered_now is False for section in sections)
    assert all(section.unavailable is True for section in sections)
