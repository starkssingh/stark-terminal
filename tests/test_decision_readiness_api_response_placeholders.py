from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_readiness_api.references import (
    default_decision_readiness_blocked_output_reference,
    default_decision_readiness_evidence_reference,
    default_decision_readiness_human_review_reference,
    default_decision_readiness_safety_reference,
)
from stark_terminal_core.decision_readiness_api.responses import (
    DecisionReadinessResponsePlaceholder,
    default_decision_readiness_response_placeholder,
)
from stark_terminal_core.decision_readiness_api.unavailable import (
    default_decision_readiness_unavailable_response,
)


def _valid_response_kwargs() -> dict[str, object]:
    return {
        "response_id": "readiness-response-1",
        "evidence_reference": default_decision_readiness_evidence_reference(),
        "safety_reference": default_decision_readiness_safety_reference(),
        "human_review_reference": default_decision_readiness_human_review_reference(),
        "blocked_output_reference": default_decision_readiness_blocked_output_reference(),
        "unavailable_response": default_decision_readiness_unavailable_response(),
    }


def test_valid_decision_readiness_response_placeholder() -> None:
    response = DecisionReadinessResponsePlaceholder(**_valid_response_kwargs(), notes=[" contract ", ""])

    assert response.planning_only is True
    assert response.notes == ["contract"]
    assert response.readiness_status_generated is False
    assert response.recommendation_generated is False
    assert response.action_generated is False
    assert response.confidence_generated is False
    assert response.decision_object_generated is False
    assert response.approval_granted is False
    assert response.override_granted is False
    assert response.execution_ready is False


def test_readiness_response_placeholder_requires_nested_placeholders() -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessResponsePlaceholder(response_id="readiness-response-1")


def test_readiness_response_placeholder_enforces_planning_only() -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessResponsePlaceholder(**_valid_response_kwargs(), planning_only=False)


@pytest.mark.parametrize(
    "field",
    [
        "readiness_status_generated",
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "approval_granted",
        "override_granted",
        "execution_ready",
    ],
)
def test_readiness_response_placeholder_rejects_generated_outputs(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessResponsePlaceholder(**_valid_response_kwargs(), **{field: True})


def test_default_readiness_response_placeholder_validates() -> None:
    response = default_decision_readiness_response_placeholder()

    assert response.evidence_reference.required is True
    assert response.safety_reference.passed is False
    assert response.human_review_reference.approval_granted is False
    assert response.blocked_output_reference.execution_blocked is True
    assert response.unavailable_response.unavailable is True
    assert response.decision_object_generated is False
