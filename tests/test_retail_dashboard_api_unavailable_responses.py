from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_api.requests import RetailDashboardAPIUnavailableReason
from stark_terminal_core.retail_dashboard_api.unavailable import (
    RetailDashboardAPIUnavailableResponse,
    default_retail_dashboard_api_unavailable_response,
)


def _unavailable(**overrides: object) -> RetailDashboardAPIUnavailableResponse:
    data = {
        "response_id": "retail-dashboard-api-unavailable-test",
        "reason": RetailDashboardAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
        "message": "Retail Dashboard API unavailable by default.",
    }
    data.update(overrides)
    return RetailDashboardAPIUnavailableResponse(**data)


def test_retail_dashboard_api_unavailable_response_validates() -> None:
    response = default_retail_dashboard_api_unavailable_response()

    assert response.unavailable is True
    assert response.api_contract_skeleton_only is True
    assert response.reason == RetailDashboardAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY
    assert response.active_ui_allowed is False
    assert response.execution_allowed is False


def test_retail_dashboard_api_unavailable_response_rejects_unknown_reason() -> None:
    with pytest.raises(ValidationError):
        _unavailable(reason=RetailDashboardAPIUnavailableReason.UNKNOWN)


@pytest.mark.parametrize("field_name", ["unavailable", "api_contract_skeleton_only"])
def test_retail_dashboard_api_unavailable_response_enforces_true_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _unavailable(**{field_name: False})


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
def test_retail_dashboard_api_unavailable_response_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _unavailable(**{field_name: True})
