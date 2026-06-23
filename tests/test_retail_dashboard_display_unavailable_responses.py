from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_display.unavailable import (
    RetailDashboardDisplayUnavailableResponse,
    default_retail_dashboard_display_unavailable_response,
)


def _response(**overrides: object) -> RetailDashboardDisplayUnavailableResponse:
    data = {
        "response_id": "retail-dashboard-display-unavailable-test",
        "message": "Display contract skeleton unavailable response.",
    }
    data.update(overrides)
    return RetailDashboardDisplayUnavailableResponse(**data)


def test_retail_dashboard_display_unavailable_response_validates() -> None:
    response = _response()

    assert response.unavailable is True
    assert response.display_contract_only is True
    assert response.active_ui_allowed is False
    assert response.execution_allowed is False


@pytest.mark.parametrize("field_name", ["unavailable", "display_contract_only"])
def test_retail_dashboard_display_unavailable_response_enforces_true_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _response(**{field_name: False})


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_granted",
        "override_granted",
    ],
)
def test_retail_dashboard_display_unavailable_response_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _response(**{field_name: True})


def test_default_retail_dashboard_display_unavailable_response_validates() -> None:
    response = default_retail_dashboard_display_unavailable_response()

    assert response.unavailable is True
    assert response.display_contract_only is True
    assert "Prompt 51" in response.message
