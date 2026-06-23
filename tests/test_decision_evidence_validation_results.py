from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence_validation.contracts import (
    DecisionEvidenceValidationIssueKind,
    DecisionEvidenceValidationIssueSeverity,
)
from stark_terminal_core.decision_evidence_validation.issues import create_validation_issue
from stark_terminal_core.decision_evidence_validation.results import (
    DecisionEvidenceValidationResult,
    create_invalid_decision_evidence_validation_result,
    create_valid_decision_evidence_validation_result,
)


def _blocker_issue():
    return create_validation_issue(
        issue_id="blocker-issue",
        kind=DecisionEvidenceValidationIssueKind.MISSING_EVIDENCE_ITEM,
        severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
        message="Missing evidence.",
    )


def _warning_issue():
    return create_validation_issue(
        issue_id="warning-issue",
        kind=DecisionEvidenceValidationIssueKind.INVALID_SOURCE_REFERENCE,
        severity=DecisionEvidenceValidationIssueSeverity.WARNING,
        message="Warning.",
    )


def test_decision_evidence_validation_result_validates_counts() -> None:
    issues = [_blocker_issue(), _warning_issue()]
    result = DecisionEvidenceValidationResult(
        result_id="validation-result-test",
        request_id="request-test",
        valid=False,
        issues=issues,
        issue_count=2,
        blocker_count=1,
        warning_count=1,
        status="blocked_validation_only",
    )

    assert result.validation_only is True
    assert result.recommendations_allowed is False
    assert result.decision_object_generation_allowed is False
    assert result.readiness_to_trade is False


@pytest.mark.parametrize(
    "override",
    [
        {"issue_count": 1},
        {"blocker_count": 0},
        {"warning_count": 0},
        {"validation_only": False},
        {"recommendations_allowed": True},
        {"action_generation_allowed": True},
        {"confidence_scoring_allowed": True},
        {"decision_object_generation_allowed": True},
        {"execution_allowed": True},
        {"approval_granted": True},
        {"override_granted": True},
        {"readiness_to_trade": True},
    ],
)
def test_decision_evidence_validation_result_rejects_invalid_counts_and_dangerous_flags(
    override: dict[str, object],
) -> None:
    kwargs = {
        "result_id": "validation-result-test",
        "request_id": "request-test",
        "valid": False,
        "issues": [_blocker_issue(), _warning_issue()],
        "issue_count": 2,
        "blocker_count": 1,
        "warning_count": 1,
        "status": "blocked_validation_only",
    }
    kwargs.update(override)

    with pytest.raises(ValidationError):
        DecisionEvidenceValidationResult(**kwargs)


def test_decision_evidence_validation_result_helpers_work() -> None:
    valid = create_valid_decision_evidence_validation_result(request_id="request-test", bundle_id="bundle-test")
    invalid = create_invalid_decision_evidence_validation_result(
        request_id="request-test",
        bundle_id="bundle-test",
        issues=[_blocker_issue()],
    )

    assert valid.valid is True
    assert valid.decision_object_generation_allowed is False
    assert "not_decision_ready" in valid.status
    assert invalid.valid is False
    assert invalid.blocker_count == 1
    assert invalid.readiness_to_trade is False

