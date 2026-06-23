from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_api.references import (
    default_retail_dashboard_api_data_reference,
    default_retail_dashboard_api_decision_reference,
    default_retail_dashboard_api_safety_reference,
)
from stark_terminal_core.retail_dashboard_api.responses import (
    RetailDashboardAPIResponsePlaceholder,
    default_retail_dashboard_api_response_placeholder,
)
from stark_terminal_core.retail_dashboard_api.unavailable import (
    default_retail_dashboard_api_unavailable_response,
)


def _response(**overrides: object) -> RetailDashboardAPIResponsePlaceholder:
    data = {
        "response_id": "retail-dashboard-api-response-test",
        "data_reference": default_retail_dashboard_api_data_reference(),
        "decision_reference": default_retail_dashboard_api_decision_reference(),
        "safety_reference": default_retail_dashboard_api_safety_reference(),
        "unavailable_response": default_retail_dashboard_api_unavailable_response(),
    }
    data.update(overrides)
    return RetailDashboardAPIResponsePlaceholder(**data)


def test_retail_dashboard_api_response_placeholder_validates() -> None:
    response = default_retail_dashboard_api_response_placeholder(request_id="request-test")

    assert response.request_id == "request-test"
    assert response.api_contract_skeleton_only is True
    assert response.active_ui_generated is False
    assert response.recommendation_generated is False
    assert response.action_generated is False
    assert response.confidence_generated is False
    assert response.decision_object_generated is False
    assert response.readiness_to_trade_generated is False
    assert response.broker_control_generated is False
    assert response.execution_ready is False
    assert response.approval_granted is False
    assert response.override_granted is False


def test_retail_dashboard_api_response_placeholder_requires_references() -> None:
    with pytest.raises(ValidationError):
        RetailDashboardAPIResponsePlaceholder(response_id="missing-references")


def test_retail_dashboard_api_response_placeholder_enforces_contract_skeleton_only() -> None:
    with pytest.raises(ValidationError):
        _response(api_contract_skeleton_only=False)


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui_generated",
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "broker_control_generated",
        "execution_ready",
        "approval_granted",
        "override_granted",
    ],
)
def test_retail_dashboard_api_response_placeholder_rejects_generated_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _response(**{field_name: True})
