from __future__ import annotations

from pydantic import ValidationError
import pytest

from stark_terminal_core.retail_trader_experience.cards import default_retail_trader_experience_card_placeholders
from stark_terminal_core.retail_trader_experience.journeys import default_retail_trader_journey_placeholders
from stark_terminal_core.retail_trader_experience.personas import default_retail_trader_persona_placeholders
from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperiencePlanningContract,
    default_retail_trader_experience_planning_contract,
)
from stark_terminal_core.retail_trader_experience.safety import (
    RetailTraderExperienceSafetyPolicy,
    default_retail_trader_experience_safety_policy,
    evaluate_retail_trader_experience_cards_safety,
    evaluate_retail_trader_experience_journeys_safety,
    evaluate_retail_trader_experience_personas_safety,
    evaluate_retail_trader_experience_plan_safety,
    reject_experience_as_active_ui,
    reject_experience_as_execution_surface,
    reject_experience_as_recommendation,
    reject_experience_as_suitability_profile,
)


def test_default_retail_trader_experience_safety_policy_forbids_dangerous_behavior() -> None:
    policy = default_retail_trader_experience_safety_policy()
    assert policy.allow_active_ui is False
    assert policy.allow_frontend_components is False
    assert policy.allow_desktop_components is False
    assert policy.allow_recommendations is False
    assert policy.allow_action_generation is False
    assert policy.allow_confidence_scoring is False
    assert policy.allow_decision_object_generation is False
    assert policy.allow_readiness_to_trade is False
    assert policy.allow_broker_controls is False
    assert policy.allow_execution is False
    assert policy.allow_approval is False
    assert policy.allow_override is False
    assert policy.allow_suitability_profiling is False
    assert policy.require_planning_only is True


def test_retail_trader_experience_safety_policy_rejects_unsafe_flags() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceSafetyPolicy(
            policy_id="unsafe",
            name="Unsafe",
            allow_suitability_profiling=True,
        )


def test_retail_trader_experience_plan_safety_rejects_unsafe_constructed_plan() -> None:
    plan = default_retail_trader_experience_planning_contract()
    unsafe_plan = RetailTraderExperiencePlanningContract.model_construct(
        **{**plan.model_dump(), "recommendations_allowed": True}
    )
    result = evaluate_retail_trader_experience_plan_safety(
        unsafe_plan,
        default_retail_trader_experience_safety_policy(),
    )
    assert result.safe is False
    assert result.planning_only is True
    assert result.recommendations_allowed is False


def test_retail_trader_experience_persona_journey_and_card_safety_reject_unsafe_constructed_items() -> None:
    policy = default_retail_trader_experience_safety_policy()
    persona = default_retail_trader_persona_placeholders()[0]
    unsafe_persona = persona.model_construct(**{**persona.model_dump(), "suitability_profile": True})
    assert evaluate_retail_trader_experience_personas_safety([unsafe_persona], policy).safe is False

    journey = default_retail_trader_journey_placeholders()[0]
    unsafe_journey = journey.model_construct(**{**journey.model_dump(), "execution_journey": True})
    assert evaluate_retail_trader_experience_journeys_safety([unsafe_journey], policy).safe is False

    card = default_retail_trader_experience_card_placeholders()[0]
    unsafe_card = card.model_construct(**{**card.model_dump(), "recommendation_card": True})
    assert evaluate_retail_trader_experience_cards_safety([unsafe_card], policy).safe is False


def test_retail_trader_experience_reject_helpers_return_blocking_results() -> None:
    helpers = [
        reject_experience_as_active_ui,
        reject_experience_as_recommendation,
        reject_experience_as_execution_surface,
        reject_experience_as_suitability_profile,
    ]
    for helper in helpers:
        result = helper()
        assert result.safe is False
        assert result.planning_only is True
        assert result.active_ui_allowed is False
        assert result.execution_allowed is False
        assert result.suitability_profiling_allowed is False
