from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_api.responses import (
    DecisionDeskResponsePlaceholder,
    default_decision_desk_response_placeholder,
)
from stark_terminal_core.decision_api.references import (
    default_decision_safety_reference_placeholder,
    default_evidence_bundle_reference_placeholder,
)
from stark_terminal_core.decision_api.unavailable import default_decision_desk_unavailable_response


def _valid_response_kwargs() -> dict[str, object]:
    return {
        "response_id": "response-1",
        "evidence_reference": default_evidence_bundle_reference_placeholder(),
        "safety_reference": default_decision_safety_reference_placeholder(),
        "unavailable_response": default_decision_desk_unavailable_response(),
    }


def test_valid_decision_desk_response_placeholder() -> None:
    response = DecisionDeskResponsePlaceholder(**_valid_response_kwargs(), notes=[" contract ", ""])

    assert response.planning_only is True
    assert response.notes == ["contract"]
    assert response.recommendation_generated is False
    assert response.action_generated is False
    assert response.confidence_generated is False
    assert response.decision_object_generated is False
    assert response.execution_ready is False


def test_response_placeholder_requires_nested_placeholders() -> None:
    with pytest.raises(ValidationError):
        DecisionDeskResponsePlaceholder(response_id="response-1")


@pytest.mark.parametrize(
    "field",
    [
        "planning_only",
    ],
)
def test_response_placeholder_enforces_planning_only(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionDeskResponsePlaceholder(**_valid_response_kwargs(), **{field: False})


@pytest.mark.parametrize(
    "field",
    [
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "execution_ready",
    ],
)
def test_response_placeholder_rejects_generated_outputs(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionDeskResponsePlaceholder(**_valid_response_kwargs(), **{field: True})


def test_default_response_placeholder_validates() -> None:
    response = default_decision_desk_response_placeholder()

    assert response.evidence_reference.required is True
    assert response.safety_reference.passed is False
    assert response.unavailable_response.unavailable is True
    assert response.decision_object_generated is False

