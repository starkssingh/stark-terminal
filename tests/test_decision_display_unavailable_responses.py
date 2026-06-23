from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_display.unavailable import (
    DecisionDisplayUnavailableResponse,
    default_decision_display_unavailable_response,
)


def test_decision_display_unavailable_response_validates() -> None:
    response = default_decision_display_unavailable_response()

    assert response.unavailable is True
    assert response.planning_only is True
    assert response.display_contract_only is True
    assert response.recommendations_allowed is False


@pytest.mark.parametrize(
    "override",
    [
        {"unavailable": False},
        {"planning_only": False},
        {"display_contract_only": False},
        {"recommendations_allowed": True},
        {"action_generation_allowed": True},
        {"confidence_scoring_allowed": True},
        {"decision_object_generation_allowed": True},
        {"readiness_to_trade_allowed": True},
        {"execution_allowed": True},
        {"approval_granted": True},
        {"override_granted": True},
    ],
)
def test_decision_display_unavailable_response_rejects_unsafe_values(override: dict[str, object]) -> None:
    kwargs = {
        "response_id": "display-unavailable-test",
        "message": "Unavailable display response.",
    }
    kwargs.update(override)

    with pytest.raises(ValidationError):
        DecisionDisplayUnavailableResponse(**kwargs)

