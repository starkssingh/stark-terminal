from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_display.contracts import (
    RetailDashboardDisplayBadgeKind,
    RetailDashboardDisplayContractMetadata,
    RetailDashboardLayoutKind,
    RetailDashboardVisualSectionKind,
    RetailDashboardWidgetKind,
    default_retail_dashboard_display_contract_metadata,
)


def _metadata(**overrides: object) -> RetailDashboardDisplayContractMetadata:
    data = {
        "contract_id": "retail-dashboard-display-contract-test",
        "layout_kinds": [RetailDashboardLayoutKind.RETAIL_OVERVIEW_PLACEHOLDER],
        "widget_kinds": [RetailDashboardWidgetKind.PLACEHOLDER],
        "section_kinds": [RetailDashboardVisualSectionKind.OVERVIEW],
        "badge_kinds": [RetailDashboardDisplayBadgeKind.PLANNING_ONLY],
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
    return RetailDashboardDisplayContractMetadata(**data)


def test_default_retail_dashboard_display_contract_metadata_validates() -> None:
    metadata = default_retail_dashboard_display_contract_metadata()

    assert metadata.service_name == "stark-terminal-retail-dashboard-display"
    assert metadata.returns_unavailable_by_default is True
    assert RetailDashboardLayoutKind.RETAIL_OVERVIEW_PLACEHOLDER in metadata.layout_kinds
    assert RetailDashboardWidgetKind.PLACEHOLDER in metadata.widget_kinds
    assert RetailDashboardVisualSectionKind.OVERVIEW in metadata.section_kinds
    assert RetailDashboardDisplayBadgeKind.PLANNING_ONLY in metadata.badge_kinds


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
def test_retail_dashboard_display_contract_metadata_rejects_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _metadata(**{field_name: True})


def test_retail_dashboard_display_contract_metadata_enforces_unavailable_by_default() -> None:
    with pytest.raises(ValidationError):
        _metadata(returns_unavailable_by_default=False)


def test_retail_dashboard_display_contract_metadata_requires_forbidden_outputs() -> None:
    with pytest.raises(ValidationError):
        _metadata(forbidden_outputs=["execution"])


def test_retail_dashboard_display_contract_metadata_rejects_unknown_kinds() -> None:
    with pytest.raises(ValidationError):
        _metadata(layout_kinds=[RetailDashboardLayoutKind.UNKNOWN])
    with pytest.raises(ValidationError):
        _metadata(widget_kinds=[RetailDashboardWidgetKind.UNKNOWN])
    with pytest.raises(ValidationError):
        _metadata(section_kinds=[RetailDashboardVisualSectionKind.UNKNOWN])
    with pytest.raises(ValidationError):
        _metadata(badge_kinds=[RetailDashboardDisplayBadgeKind.UNKNOWN])
