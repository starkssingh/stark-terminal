from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_api.contracts import (
    RetailDashboardAPIContractMetadata,
    default_retail_dashboard_api_contract_metadata,
)
from stark_terminal_core.retail_dashboard_api.requests import (
    RetailDashboardAPIRequestKind,
    RetailDashboardAPIUnavailableReason,
)


def _metadata(**overrides: object) -> RetailDashboardAPIContractMetadata:
    data = {
        "contract_id": "retail-dashboard-api-contract-test",
        "request_kinds": [RetailDashboardAPIRequestKind.DASHBOARD_OVERVIEW_REQUEST],
        "unavailable_reasons": [RetailDashboardAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY],
        "forbidden_outputs": [
            "active UI",
            "recommendation",
            "action",
            "confidence",
            "DecisionObject",
            "readiness-to-trade",
            "broker",
            "execution",
            "approval",
            "override",
        ],
    }
    data.update(overrides)
    return RetailDashboardAPIContractMetadata(**data)


def test_default_retail_dashboard_api_contract_metadata_validates() -> None:
    metadata = default_retail_dashboard_api_contract_metadata()

    assert metadata.service_name == "stark-terminal-retail-dashboard-api"
    assert metadata.returns_unavailable_by_default is True
    assert metadata.request_kinds
    assert metadata.unavailable_reasons
    assert RetailDashboardAPIRequestKind.DASHBOARD_OVERVIEW_REQUEST in metadata.request_kinds
    assert RetailDashboardAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY in metadata.unavailable_reasons


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
def test_retail_dashboard_api_contract_metadata_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _metadata(**{field_name: True})


def test_retail_dashboard_api_contract_metadata_enforces_unavailable_by_default() -> None:
    with pytest.raises(ValidationError):
        _metadata(returns_unavailable_by_default=False)


def test_retail_dashboard_api_contract_metadata_requires_forbidden_outputs() -> None:
    with pytest.raises(ValidationError):
        _metadata(forbidden_outputs=["execution"])


def test_retail_dashboard_api_contract_metadata_rejects_unknown_kinds() -> None:
    with pytest.raises(ValidationError):
        _metadata(request_kinds=[RetailDashboardAPIRequestKind.UNKNOWN])
    with pytest.raises(ValidationError):
        _metadata(unavailable_reasons=[RetailDashboardAPIUnavailableReason.UNKNOWN])
