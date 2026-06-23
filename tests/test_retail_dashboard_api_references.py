from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_api.references import (
    RetailDashboardAPIDataReference,
    RetailDashboardAPIDecisionReference,
    RetailDashboardAPISafetyReference,
    default_retail_dashboard_api_data_reference,
    default_retail_dashboard_api_decision_reference,
    default_retail_dashboard_api_safety_reference,
)


def test_retail_dashboard_api_data_reference_validates() -> None:
    reference = default_retail_dashboard_api_data_reference()

    assert reference.required is True
    assert reference.real_market_data is False
    assert reference.live_data is False
    assert reference.display_ready is False


@pytest.mark.parametrize("field_name", ["real_market_data", "live_data", "display_ready"])
def test_retail_dashboard_api_data_reference_rejects_unsafe_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailDashboardAPIDataReference(
            reference_id="data-reference-test",
            source_name="source-placeholder",
            **{field_name: True},
        )


def test_retail_dashboard_api_decision_reference_validates() -> None:
    reference = default_retail_dashboard_api_decision_reference()

    assert reference.required is False
    assert reference.active_decision_object is False
    assert reference.recommendation_available is False
    assert reference.action_available is False
    assert reference.confidence_available is False
    assert reference.readiness_to_trade_available is False
    assert reference.display_ready is False


@pytest.mark.parametrize(
    "field_name",
    [
        "active_decision_object",
        "recommendation_available",
        "action_available",
        "confidence_available",
        "readiness_to_trade_available",
        "display_ready",
    ],
)
def test_retail_dashboard_api_decision_reference_rejects_unsafe_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailDashboardAPIDecisionReference(reference_id="decision-reference-test", **{field_name: True})


def test_retail_dashboard_api_safety_reference_validates() -> None:
    reference = default_retail_dashboard_api_safety_reference()

    assert reference.required is True
    assert reference.safety_passed is False
    assert reference.approval_granted is False
    assert reference.override_granted is False
    assert reference.execution_allowed is False
    assert reference.broker_controls_allowed is False


@pytest.mark.parametrize(
    "field_name",
    [
        "safety_passed",
        "approval_granted",
        "override_granted",
        "execution_allowed",
        "broker_controls_allowed",
    ],
)
def test_retail_dashboard_api_safety_reference_rejects_unsafe_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailDashboardAPISafetyReference(reference_id="safety-reference-test", **{field_name: True})
