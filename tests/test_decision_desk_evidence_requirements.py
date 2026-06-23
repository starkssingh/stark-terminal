import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_desk.evidence import (
    RetailDecisionEvidenceChecklist,
    RetailDecisionEvidenceRequirement,
    build_retail_decision_evidence_checklist,
    default_retail_decision_evidence_requirements,
    evaluate_retail_decision_evidence_checklist,
)
from stark_terminal_core.decision_desk.planning import RetailEvidenceKind


def test_default_evidence_requirements_exist_and_require_human_review() -> None:
    requirements = default_retail_decision_evidence_requirements()
    kinds = {requirement.evidence_kind for requirement in requirements}

    assert RetailEvidenceKind.INSTRUMENT_CONTEXT in kinds
    assert RetailEvidenceKind.DATA_QUALITY in kinds
    assert RetailEvidenceKind.HUMAN_REVIEW in kinds
    assert all(requirement.source_reference_required for requirement in requirements)
    assert all(requirement.validation_required for requirement in requirements)
    assert all(requirement.human_review_required for requirement in requirements)


@pytest.mark.parametrize(
    "override",
    [
        {"evidence_kind": RetailEvidenceKind.UNKNOWN},
        {"human_review_required": False},
    ],
)
def test_evidence_requirement_rejects_unknown_or_no_review(override: dict[str, object]) -> None:
    kwargs = {
        "requirement_id": "evidence-test",
        "evidence_kind": RetailEvidenceKind.DATA_QUALITY,
        "description": "Evidence requirement.",
        **override,
    }

    with pytest.raises(ValidationError):
        RetailDecisionEvidenceRequirement(**kwargs)


@pytest.mark.parametrize(
    "override",
    [
        {"recommendations_allowed": True},
        {"action_generation_allowed": True},
        {"decision_object_generation_allowed": True},
        {"complete": True, "blockers": ["blocked"]},
    ],
)
def test_evidence_checklist_rejects_unsafe_state(override: dict[str, object]) -> None:
    kwargs = {
        "checklist_id": "checklist-test",
        "requirements": default_retail_decision_evidence_requirements(),
        **override,
    }

    with pytest.raises(ValidationError):
        RetailDecisionEvidenceChecklist(**kwargs)


def test_evidence_checklist_with_missing_items_has_blockers() -> None:
    checklist = evaluate_retail_decision_evidence_checklist(build_retail_decision_evidence_checklist())

    assert checklist.complete is False
    assert checklist.blockers
    assert checklist.recommendations_allowed is False
    assert checklist.action_generation_allowed is False
    assert checklist.decision_object_generation_allowed is False
