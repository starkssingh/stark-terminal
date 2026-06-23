from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence.human_review import (
    DecisionEvidenceHumanReviewAttachment,
    DecisionEvidenceHumanReviewAttachmentSet,
    build_decision_evidence_human_review_attachment_set,
    default_decision_evidence_human_review_attachments,
)


def test_decision_evidence_human_review_attachment_blocks_outputs() -> None:
    attachment = DecisionEvidenceHumanReviewAttachment(
        attachment_id="review-1",
        title="Review",
        description="Review attachment.",
    )

    assert attachment.approval_granted is False
    assert attachment.blocks_recommendations is True
    assert attachment.blocks_action_generation is True
    assert attachment.blocks_confidence_scoring is True
    assert attachment.blocks_decision_object_generation is True
    assert attachment.blocks_execution is True


def test_decision_evidence_human_review_attachment_rejects_approval_or_bypass() -> None:
    base = {"attachment_id": "review-1", "title": "Review", "description": "Review attachment."}
    with pytest.raises(ValidationError):
        DecisionEvidenceHumanReviewAttachment(**{**base, "approval_granted": True})

    for field in [
        "blocks_recommendations",
        "blocks_action_generation",
        "blocks_confidence_scoring",
        "blocks_decision_object_generation",
        "blocks_execution",
    ]:
        with pytest.raises(ValidationError):
            DecisionEvidenceHumanReviewAttachment(**{**base, field: False})


def test_decision_evidence_human_review_attachment_set_remains_incomplete_until_reviewed() -> None:
    attachments = default_decision_evidence_human_review_attachments()
    attachment_set = build_decision_evidence_human_review_attachment_set(attachments=attachments)

    assert attachment_set.complete is False
    assert attachment_set.approval_granted is False
    assert attachment_set.decision_object_generation_allowed is False
    assert attachment_set.execution_allowed is False
    assert attachment_set.blockers

    with pytest.raises(ValidationError):
        DecisionEvidenceHumanReviewAttachmentSet(
            attachment_set_id="set-1",
            attachments=attachments,
            complete=True,
            blockers=["missing"],
        )
