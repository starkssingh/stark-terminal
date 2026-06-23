from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard.sections import (
    RetailDashboardSectionKind,
    RetailDashboardSectionPlaceholder,
    default_retail_dashboard_section_placeholders,
)


def _section(**overrides: object) -> RetailDashboardSectionPlaceholder:
    data = {
        "section_id": "section-test",
        "section_kind": RetailDashboardSectionKind.OVERVIEW,
        "title": "Overview",
        "description": "Planning-only section.",
    }
    data.update(overrides)
    return RetailDashboardSectionPlaceholder(**data)


def test_valid_retail_dashboard_section_placeholder() -> None:
    section = _section()

    assert section.active_ui is False
    assert section.unavailable is True
    assert section.planning_only is True
    assert section.execution_allowed is False


def test_retail_dashboard_section_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _section(section_kind=RetailDashboardSectionKind.UNKNOWN)


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("active_ui", True),
        ("unavailable", False),
        ("planning_only", False),
        ("recommendations_allowed", True),
        ("action_generation_allowed", True),
        ("confidence_scoring_allowed", True),
        ("decision_object_generation_allowed", True),
        ("readiness_to_trade_allowed", True),
        ("broker_controls_allowed", True),
        ("execution_allowed", True),
    ],
)
def test_retail_dashboard_section_rejects_unsafe_flags(field_name: str, value: object) -> None:
    with pytest.raises(ValidationError):
        _section(**{field_name: value})


def test_default_retail_dashboard_sections_validate() -> None:
    sections = default_retail_dashboard_section_placeholders()

    assert sections
    assert all(section.active_ui is False for section in sections)
    assert all(section.unavailable is True for section in sections)
    assert all(section.planning_only is True for section in sections)
