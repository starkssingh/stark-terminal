from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplaySectionKind,
)
from stark_terminal_core.retail_trader_experience_display.sections import (
    RetailTraderExperienceDisplaySectionPlaceholder,
    default_retail_trader_experience_display_section_placeholders,
)


def _section_kwargs(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "section_id": "section-test",
        "section_kind": RetailTraderExperienceDisplaySectionKind.OVERVIEW,
        "title": "Section test",
        "description": "Display placeholder only.",
    }
    values.update(overrides)
    return values


def test_retail_trader_experience_display_section_placeholder_validates() -> None:
    section = RetailTraderExperienceDisplaySectionPlaceholder(**_section_kwargs())

    assert section.display_contract_only is True
    assert section.active_ui is False
    assert section.rendered_now is False
    assert section.unavailable is True
    assert section.suitability_profiling_allowed is False


@pytest.mark.parametrize(
    "field",
    [
        "active_ui",
        "rendered_now",
        "unavailable",
        "display_contract_only",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "suitability_profiling_allowed",
    ],
)
def test_retail_trader_experience_display_section_rejects_unsafe_flags(field: str) -> None:
    value = False if field in {"display_contract_only", "unavailable"} else True
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplaySectionPlaceholder(**_section_kwargs(**{field: value}))


def test_retail_trader_experience_display_section_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplaySectionPlaceholder(
            **_section_kwargs(section_kind=RetailTraderExperienceDisplaySectionKind.UNKNOWN)
        )


def test_default_retail_trader_experience_display_sections_validate() -> None:
    sections = default_retail_trader_experience_display_section_placeholders()

    assert len(sections) >= 10
    assert all(section.display_contract_only for section in sections)
    assert all(section.unavailable for section in sections)
