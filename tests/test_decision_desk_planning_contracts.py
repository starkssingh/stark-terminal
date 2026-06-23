import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_desk.planning import (
    RetailDecisionDeskPlan,
    default_forbidden_decision_desk_outputs,
    default_retail_decision_desk_plan,
)


def _valid_plan_kwargs() -> dict[str, object]:
    return {
        "plan_id": "plan-test",
        "name": "Test Plan",
        "purpose": "Planning only test.",
        "planned_action_placeholders": ["BUY_BIAS", "WATCH"],
        "required_evidence_kinds": ["INSTRUMENT_CONTEXT", "HUMAN_REVIEW"],
        "forbidden_outputs": default_forbidden_decision_desk_outputs(),
    }


def test_valid_retail_decision_desk_plan() -> None:
    plan = RetailDecisionDeskPlan(**_valid_plan_kwargs())

    assert plan.recommendations_allowed is False
    assert plan.action_generation_allowed is False
    assert plan.confidence_scoring_allowed is False
    assert plan.decision_object_generation_allowed is False
    assert plan.execution_allowed is False
    assert plan.requires_human_review is True


@pytest.mark.parametrize(
    "override",
    [
        {"recommendations_allowed": True},
        {"action_generation_allowed": True},
        {"confidence_scoring_allowed": True},
        {"decision_object_generation_allowed": True},
        {"execution_allowed": True},
        {"requires_human_review": False},
        {"forbidden_outputs": ["execution_apis"]},
    ],
)
def test_retail_decision_desk_plan_rejects_unsafe_flags(override: dict[str, object]) -> None:
    kwargs = {**_valid_plan_kwargs(), **override}

    with pytest.raises(ValidationError):
        RetailDecisionDeskPlan(**kwargs)


def test_default_plan_validates_and_forbids_decision_outputs() -> None:
    plan = default_retail_decision_desk_plan()
    joined = " ".join(plan.forbidden_outputs).lower()

    assert "BUY_BIAS" in plan.planned_action_placeholders
    assert "recommendation" in joined
    assert "action" in joined
    assert "confidence" in joined
    assert "decisionobject" in joined
    assert "execution" in joined
