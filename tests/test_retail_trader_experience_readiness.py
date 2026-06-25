from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience.cards import default_retail_trader_experience_card_placeholders
from stark_terminal_core.retail_trader_experience.interactions import (
    default_retail_trader_experience_forbidden_interactions,
)
from stark_terminal_core.retail_trader_experience.journeys import default_retail_trader_journey_placeholders
from stark_terminal_core.retail_trader_experience.personas import default_retail_trader_persona_placeholders
from stark_terminal_core.retail_trader_experience.planning import default_retail_trader_experience_planning_contract
from stark_terminal_core.retail_trader_experience.readiness import (
    RetailTraderExperienceReadinessReport,
    build_retail_trader_experience_readiness_report,
    retail_trader_experience_ready_for_active_ui,
    retail_trader_experience_ready_for_execution,
    retail_trader_experience_ready_for_recommendations,
    retail_trader_experience_ready_for_suitability_profiling,
)
from stark_terminal_core.retail_trader_experience.safety import (
    default_retail_trader_experience_safety_policy,
    evaluate_retail_trader_experience_plan_safety,
)
from stark_terminal_core.retail_trader_experience.sections import (
    default_retail_trader_experience_section_placeholders,
)


def _default_report() -> RetailTraderExperienceReadinessReport:
    plan = default_retail_trader_experience_planning_contract()
    safety_result = evaluate_retail_trader_experience_plan_safety(
        plan,
        default_retail_trader_experience_safety_policy(),
    )
    return build_retail_trader_experience_readiness_report(
        plan,
        default_retail_trader_persona_placeholders(),
        default_retail_trader_journey_placeholders(),
        default_retail_trader_experience_section_placeholders(),
        default_retail_trader_experience_card_placeholders(),
        default_retail_trader_experience_forbidden_interactions(),
        safety_result,
    )


def test_retail_trader_experience_readiness_report_defaults_are_safe() -> None:
    report = _default_report()
    assert report.persona_count > 0
    assert report.journey_count > 0
    assert report.section_count > 0
    assert report.card_count > 0
    assert report.ready_for_api_contract_skeleton is True
    assert report.ready_for_display_contract_skeleton is True
    assert report.ready_for_active_ui is False
    assert report.ready_for_recommendations is False
    assert report.ready_for_execution is False
    assert report.ready_for_broker_controls is False
    assert report.ready_for_readiness_to_trade is False
    assert report.ready_for_suitability_profiling is False
    assert retail_trader_experience_ready_for_active_ui(report) is False
    assert retail_trader_experience_ready_for_recommendations(report) is False
    assert retail_trader_experience_ready_for_execution(report) is False
    assert retail_trader_experience_ready_for_suitability_profiling(report) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_active_ui",
        "ready_for_recommendations",
        "ready_for_action_generation",
        "ready_for_confidence_scoring",
        "ready_for_decision_objects",
        "ready_for_readiness_to_trade",
        "ready_for_broker_controls",
        "ready_for_execution",
        "ready_for_suitability_profiling",
    ],
)
def test_retail_trader_experience_readiness_report_rejects_dangerous_readiness(field_name: str) -> None:
    data = _default_report().model_dump()
    data[field_name] = True
    with pytest.raises(ValidationError):
        RetailTraderExperienceReadinessReport(**data)
