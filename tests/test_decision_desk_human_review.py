import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_desk.human_review import (
    RetailHumanReviewChecklist,
    RetailHumanReviewRequirement,
    build_retail_human_review_checklist,
    default_retail_human_review_requirements,
    evaluate_retail_human_review_checklist,
)


def test_default_human_review_requirements_block_outputs() -> None:
    requirements = default_retail_human_review_requirements()

    assert requirements
    assert all(requirement.blocks_recommendations for requirement in requirements)
    assert all(requirement.blocks_decision_objects for requirement in requirements)
    assert all(requirement.blocks_execution for requirement in requirements)


@pytest.mark.parametrize(
    "override",
    [
        {"blocks_recommendations": False},
        {"blocks_decision_objects": False},
        {"blocks_execution": False},
    ],
)
def test_human_review_requirement_must_block_dangerous_outputs(override: dict[str, object]) -> None:
    kwargs = {
        "review_id": "review-test",
        "title": "Review",
        "description": "Human review.",
        **override,
    }

    with pytest.raises(ValidationError):
        RetailHumanReviewRequirement(**kwargs)


@pytest.mark.parametrize(
    "override",
    [
        {"recommendations_allowed": True},
        {"decision_objects_allowed": True},
        {"execution_allowed": True},
        {"complete": True, "blockers": ["blocked"]},
    ],
)
def test_human_review_checklist_cannot_allow_outputs(override: dict[str, object]) -> None:
    kwargs = {
        "checklist_id": "human-review-checklist",
        "requirements": default_retail_human_review_requirements(),
        **override,
    }

    with pytest.raises(ValidationError):
        RetailHumanReviewChecklist(**kwargs)


def test_incomplete_human_review_checklist_has_blockers() -> None:
    checklist = evaluate_retail_human_review_checklist(build_retail_human_review_checklist())

    assert checklist.complete is False
    assert checklist.blockers
    assert checklist.recommendations_allowed is False
    assert checklist.decision_objects_allowed is False
    assert checklist.execution_allowed is False
