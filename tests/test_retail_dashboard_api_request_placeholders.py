from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_api.requests import (
    RetailDashboardAPIRequestKind,
    RetailDashboardAPIRequestPlaceholder,
    default_retail_dashboard_api_request_placeholder,
)


def _request(**overrides: object) -> RetailDashboardAPIRequestPlaceholder:
    data = {
        "request_id": "retail-dashboard-api-request-test",
        "request_kind": RetailDashboardAPIRequestKind.DASHBOARD_OVERVIEW_REQUEST,
    }
    data.update(overrides)
    return RetailDashboardAPIRequestPlaceholder(**data)


def test_retail_dashboard_api_request_placeholder_validates() -> None:
    request = _request(requested_sections=[" overview "], requested_cards=[" card "], notes=[" keep ", " "])

    assert request.request_id == "retail-dashboard-api-request-test"
    assert request.request_kind == RetailDashboardAPIRequestKind.DASHBOARD_OVERVIEW_REQUEST
    assert request.requested_sections == ["overview"]
    assert request.requested_cards == ["card"]
    assert request.data_reference_required is True
    assert request.decision_reference_required is False
    assert request.safety_reference_required is True
    assert request.notes == ["keep"]


def test_retail_dashboard_api_request_placeholder_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _request(request_kind=RetailDashboardAPIRequestKind.UNKNOWN)


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
        "approval_allowed",
        "override_allowed",
    ],
)
def test_retail_dashboard_api_request_placeholder_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _request(**{field_name: True})


def test_retail_dashboard_api_request_placeholder_requires_data_and_safety_references() -> None:
    with pytest.raises(ValidationError):
        _request(data_reference_required=False)
    with pytest.raises(ValidationError):
        _request(safety_reference_required=False)


def test_default_retail_dashboard_api_request_placeholder_validates() -> None:
    request = default_retail_dashboard_api_request_placeholder()

    assert request.data_reference_required is True
    assert request.decision_reference_required is False
    assert request.safety_reference_required is True
    assert request.active_ui_allowed is False
    assert request.recommendations_allowed is False
