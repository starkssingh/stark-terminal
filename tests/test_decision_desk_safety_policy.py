import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_desk.action_placeholders import (
    RetailActionPlaceholder,
    RetailActionPlaceholderContract,
    default_retail_action_placeholder_contracts,
)
from stark_terminal_core.decision_desk.planning import RetailDecisionDeskPlan, default_retail_decision_desk_plan
from stark_terminal_core.decision_desk.safety import (
    RetailDecisionDeskSafetyPolicy,
    default_retail_decision_desk_safety_policy,
    evaluate_action_placeholder_safety,
    evaluate_retail_decision_desk_plan_safety,
    reject_confidence_or_decision_object_generation,
    reject_recommendation_or_action_generation,
)


def test_default_safety_policy_forbids_decision_outputs() -> None:
    policy = default_retail_decision_desk_safety_policy()

    assert policy.allow_real_data is False
    assert policy.allow_recommendations is False
    assert policy.allow_action_generation is False
    assert policy.allow_confidence_scoring is False
    assert policy.allow_decision_objects is False
    assert policy.allow_execution is False
    assert policy.require_evidence is True
    assert policy.require_human_review is True


@pytest.mark.parametrize(
    "override",
    [
        {"allow_real_data": True},
        {"allow_recommendations": True},
        {"allow_action_generation": True},
        {"allow_confidence_scoring": True},
        {"allow_decision_objects": True},
        {"allow_execution": True},
        {"require_evidence": False},
        {"require_human_review": False},
    ],
)
def test_safety_policy_rejects_unsafe_flags(override: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        RetailDecisionDeskSafetyPolicy(policy_id="policy", name="Policy", **override)


def test_safe_plan_and_placeholders_pass_planning_safety() -> None:
    policy = default_retail_decision_desk_safety_policy()

    plan_result = evaluate_retail_decision_desk_plan_safety(default_retail_decision_desk_plan(), policy)
    placeholder_result = evaluate_action_placeholder_safety(default_retail_action_placeholder_contracts(), policy)

    assert plan_result.decision == "planning_allowed"
    assert placeholder_result.decision == "planning_allowed"


def test_unsafe_placeholder_blocks_safety() -> None:
    policy = default_retail_decision_desk_safety_policy()
    unsafe = RetailActionPlaceholderContract.model_construct(
        placeholder_id="unsafe-placeholder",
        action=RetailActionPlaceholder.WATCH,
        display_name="Unsafe",
        description="Unsafe construct for safety evaluator.",
        planning_only=True,
        generated_now=True,
        recommendation=False,
        trade_signal=False,
        decision_object_generated=False,
        execution_ready=False,
    )

    result = evaluate_action_placeholder_safety([unsafe], policy)

    assert result.decision == "blocked"
    assert any("action generation" in reason for reason in result.reasons)


def test_reject_helpers_block_recommendations_confidence_and_decision_objects() -> None:
    recommendation_result = reject_recommendation_or_action_generation()
    decision_result = reject_confidence_or_decision_object_generation()

    assert recommendation_result.decision == "blocked"
    assert decision_result.decision == "blocked"
    assert "recommendation" in recommendation_result.reasons[0]
    assert "DecisionObject" in decision_result.reasons[0]
