from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence_validation.contracts import (
    DecisionEvidenceValidationIssueKind,
    DecisionEvidenceValidationIssueSeverity,
)
from stark_terminal_core.decision_evidence_validation.issues import (
    DecisionEvidenceValidationIssue,
    create_missing_evidence_issue,
    create_missing_source_reference_issue,
    create_unsafe_flag_issue,
)


def test_decision_evidence_validation_issue_validates() -> None:
    issue = DecisionEvidenceValidationIssue(
        issue_id="validation-issue-test",
        kind=DecisionEvidenceValidationIssueKind.MISSING_EVIDENCE_ITEM,
        severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
        message="Missing evidence item.",
    )

    assert issue.blocks_decision_object_generation is True
    assert issue.blocks_recommendations is True
    assert issue.blocks_execution is True


@pytest.mark.parametrize(
    "override",
    [
        {"kind": DecisionEvidenceValidationIssueKind.UNKNOWN},
        {"severity": DecisionEvidenceValidationIssueSeverity.UNKNOWN},
        {"severity": DecisionEvidenceValidationIssueSeverity.ERROR, "blocks_recommendations": False},
        {"severity": DecisionEvidenceValidationIssueSeverity.BLOCKER, "blocks_decision_object_generation": False},
        {"severity": DecisionEvidenceValidationIssueSeverity.BLOCKER, "blocks_execution": False},
    ],
)
def test_decision_evidence_validation_issue_rejects_unknown_and_unblocked_errors(
    override: dict[str, object],
) -> None:
    kwargs = {
        "issue_id": "validation-issue-test",
        "kind": DecisionEvidenceValidationIssueKind.INVALID_EVIDENCE_ITEM,
        "severity": DecisionEvidenceValidationIssueSeverity.BLOCKER,
        "message": "Invalid evidence.",
    }
    kwargs.update(override)

    with pytest.raises(ValidationError):
        DecisionEvidenceValidationIssue(**kwargs)


def test_decision_evidence_validation_issue_helpers_create_blockers() -> None:
    missing_evidence = create_missing_evidence_issue("item-1")
    missing_source = create_missing_source_reference_issue("item-1")
    unsafe_flag = create_unsafe_flag_issue("item-1", "recommendation")

    assert missing_evidence.kind == DecisionEvidenceValidationIssueKind.MISSING_EVIDENCE_ITEM
    assert missing_source.kind == DecisionEvidenceValidationIssueKind.MISSING_SOURCE_REFERENCE
    assert unsafe_flag.kind == DecisionEvidenceValidationIssueKind.UNSAFE_GENERATED_OUTPUT_FLAG
    for issue in [missing_evidence, missing_source, unsafe_flag]:
        assert issue.severity == DecisionEvidenceValidationIssueSeverity.BLOCKER
        assert issue.blocks_recommendations is True
        assert issue.blocks_decision_object_generation is True
        assert issue.blocks_execution is True

