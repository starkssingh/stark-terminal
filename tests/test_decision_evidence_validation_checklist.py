from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence.items import DecisionEvidenceItemKind
from stark_terminal_core.decision_evidence.validation import (
    DecisionEvidenceValidationChecklist,
    DecisionEvidenceValidationRequirement,
    build_decision_evidence_validation_checklist,
    default_decision_evidence_validation_requirements,
)


def test_decision_evidence_validation_requirement_enforces_checks() -> None:
    requirement = DecisionEvidenceValidationRequirement(
        requirement_id="req-1",
        item_kind=DecisionEvidenceItemKind.DATA_QUALITY,
        description="Validate data quality.",
    )

    assert requirement.source_reference_required is True
    assert requirement.data_quality_required is True
    assert requirement.human_review_required is True
    assert requirement.blocks_decision_object_generation is True

    with pytest.raises(ValidationError):
        DecisionEvidenceValidationRequirement(
            requirement_id="req-1",
            item_kind=DecisionEvidenceItemKind.UNKNOWN,
            description="Invalid.",
        )


def test_decision_evidence_validation_checklist_blocks_generation_flags() -> None:
    requirements = default_decision_evidence_validation_requirements()
    assert requirements

    for field in [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
    ]:
        with pytest.raises(ValidationError):
            DecisionEvidenceValidationChecklist(
                checklist_id="checklist-1",
                requirements=requirements,
                **{field: True},
            )


def test_decision_evidence_validation_checklist_complete_cannot_have_blockers() -> None:
    requirements = default_decision_evidence_validation_requirements()
    checklist = build_decision_evidence_validation_checklist(requirements=requirements)
    assert checklist.complete is False
    assert checklist.blockers

    with pytest.raises(ValidationError):
        DecisionEvidenceValidationChecklist(
            checklist_id="checklist-1",
            requirements=requirements,
            complete=True,
            blockers=["missing"],
        )
