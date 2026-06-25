from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_display.contracts import (
    default_retail_trader_experience_display_contract_metadata,
)
from stark_terminal_core.retail_trader_experience_display.journeys import (
    RetailTraderExperienceDisplayJourneyPlaceholder,
    default_retail_trader_experience_display_journey_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.personas import (
    RetailTraderExperienceDisplayPersonaPlaceholder,
    default_retail_trader_experience_display_persona_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.safety import (
    RetailTraderExperienceDisplaySafetyPolicy,
    default_retail_trader_experience_display_safety_policy,
    evaluate_retail_trader_experience_display_contract_safety,
    evaluate_retail_trader_experience_display_journeys_safety,
    evaluate_retail_trader_experience_display_personas_safety,
    evaluate_retail_trader_experience_display_widgets_safety,
    reject_display_as_active_ui,
    reject_display_as_execution_surface,
    reject_display_as_recommendation,
    reject_display_as_suitability_profile,
)
from stark_terminal_core.retail_trader_experience_display.widgets import (
    RetailTraderExperienceDisplayWidgetPlaceholder,
    default_retail_trader_experience_display_widget_placeholders,
)


def test_default_retail_trader_experience_display_safety_policy_forbids_dangerous_flags() -> None:
    policy = default_retail_trader_experience_display_safety_policy()

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
    assert policy.require_display_contract_only is True


@pytest.mark.parametrize(
    "field",
    [
        "allow_active_ui",
        "allow_frontend_components",
        "allow_desktop_components",
        "allow_recommendations",
        "allow_action_generation",
        "allow_confidence_scoring",
        "allow_decision_object_generation",
        "allow_readiness_to_trade",
        "allow_broker_controls",
        "allow_execution",
        "allow_approval",
        "allow_override",
        "allow_suitability_profiling",
    ],
)
def test_retail_trader_experience_display_safety_policy_rejects_dangerous_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplaySafetyPolicy(
            policy_id="unsafe-policy",
            name="Unsafe policy",
            **{field: True},
        )


def test_retail_trader_experience_display_safety_evaluators_pass_defaults() -> None:
    policy = default_retail_trader_experience_display_safety_policy()

    assert evaluate_retail_trader_experience_display_contract_safety(
        default_retail_trader_experience_display_contract_metadata(),
        policy,
    ).safe is True
    assert evaluate_retail_trader_experience_display_personas_safety(
        default_retail_trader_experience_display_persona_placeholders(),
        policy,
    ).safe is True
    assert evaluate_retail_trader_experience_display_journeys_safety(
        default_retail_trader_experience_display_journey_placeholders(),
        policy,
    ).safe is True
    assert evaluate_retail_trader_experience_display_widgets_safety(
        default_retail_trader_experience_display_widget_placeholders(),
        policy,
    ).safe is True


def test_retail_trader_experience_display_safety_evaluators_block_unsafe_constructed_models() -> None:
    policy = default_retail_trader_experience_display_safety_policy()
    contract = default_retail_trader_experience_display_contract_metadata().model_copy(
        update={"active_ui_allowed": True}
    )
    persona = RetailTraderExperienceDisplayPersonaPlaceholder.model_construct(
        persona_id="unsafe-persona",
        active_ui=True,
        display_contract_only=True,
    )
    journey = RetailTraderExperienceDisplayJourneyPlaceholder.model_construct(
        journey_id="unsafe-journey",
        execution_journey=True,
        display_contract_only=True,
        unavailable=True,
    )
    widget = RetailTraderExperienceDisplayWidgetPlaceholder.model_construct(
        widget_id="unsafe-widget",
        recommendation_widget=True,
        display_contract_only=True,
        unavailable=True,
    )

    assert not evaluate_retail_trader_experience_display_contract_safety(contract, policy).safe
    assert not evaluate_retail_trader_experience_display_personas_safety([persona], policy).safe
    assert not evaluate_retail_trader_experience_display_journeys_safety([journey], policy).safe
    assert not evaluate_retail_trader_experience_display_widgets_safety([widget], policy).safe


def test_retail_trader_experience_display_reject_helpers_return_blocking_results() -> None:
    for result in [
        reject_display_as_active_ui(),
        reject_display_as_recommendation(),
        reject_display_as_execution_surface(),
        reject_display_as_suitability_profile(),
    ]:
        assert result.safe is False
        assert result.display_contract_only is True
        assert result.active_ui_allowed is False
        assert result.execution_allowed is False
        assert result.suitability_profiling_allowed is False
