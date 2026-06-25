from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience.planning import RetailTraderExperienceSectionKind
from stark_terminal_core.retail_trader_experience.sections import (
    RetailTraderExperienceSectionPlaceholder,
    default_retail_trader_experience_section_placeholders,
)


def test_retail_trader_experience_section_placeholders_default_validate() -> None:
    sections = default_retail_trader_experience_section_placeholders()
    assert sections
    for section in sections:
        assert section.active_ui is False
        assert section.unavailable is True
        assert section.planning_only is True
        assert section.suitability_profiling_allowed is False
        assert section.execution_allowed is False


def test_retail_trader_experience_section_rejects_unknown_kind() -> None:
    data = default_retail_trader_experience_section_placeholders()[0].model_dump()
    data["section_kind"] = RetailTraderExperienceSectionKind.UNKNOWN
    with pytest.raises(ValidationError):
        RetailTraderExperienceSectionPlaceholder(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui",
        "unavailable",
        "planning_only",
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
def test_retail_trader_experience_section_enforces_safe_flags(field_name: str) -> None:
    data = default_retail_trader_experience_section_placeholders()[0].model_dump()
    data[field_name] = False if field_name in {"unavailable", "planning_only"} else True
    with pytest.raises(ValidationError):
        RetailTraderExperienceSectionPlaceholder(**data)
