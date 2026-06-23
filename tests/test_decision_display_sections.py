from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_display.cards import default_decision_display_card_placeholders
from stark_terminal_core.decision_display.contracts import DecisionDisplaySectionKind
from stark_terminal_core.decision_display.sections import (
    DecisionDisplaySectionPlaceholder,
    default_decision_display_section_placeholders,
)


def _valid_section_kwargs() -> dict[str, object]:
    return {
        "section_id": "display-section-test",
        "section_kind": DecisionDisplaySectionKind.HEADER,
        "title": "Display Section",
        "description": "Display section placeholder.",
        "cards": [default_decision_display_card_placeholders()[0]],
    }


def test_decision_display_section_placeholder_validates() -> None:
    section = DecisionDisplaySectionPlaceholder(**_valid_section_kwargs())

    assert section.unavailable is True
    assert section.planning_only is True
    assert section.cards


@pytest.mark.parametrize(
    "override",
    [
        {"section_kind": DecisionDisplaySectionKind.UNKNOWN},
        {"cards": []},
        {"unavailable": False},
        {"planning_only": False},
        {"recommendation_generated": True},
        {"action_generated": True},
        {"confidence_generated": True},
        {"decision_object_generated": True},
        {"readiness_to_trade_generated": True},
        {"execution_ready": True},
    ],
)
def test_decision_display_section_placeholder_rejects_unsafe_values(override: dict[str, object]) -> None:
    kwargs = _valid_section_kwargs()
    kwargs.update(override)

    with pytest.raises(ValidationError):
        DecisionDisplaySectionPlaceholder(**kwargs)


def test_default_decision_display_sections_validate() -> None:
    sections = default_decision_display_section_placeholders()

    assert sections
    assert all(section.cards for section in sections)
    assert all(section.unavailable for section in sections)
    assert all(not section.decision_object_generated for section in sections)

