from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard.planning import (
    REQUIRED_FORBIDDEN_INTERACTIONS,
    RetailDashboardCardKind,
    RetailDashboardForbiddenInteractionKind,
    RetailDashboardPlanningContract,
    RetailDashboardSectionKind,
    default_retail_dashboard_planning_contract,
)


def test_valid_retail_dashboard_planning_contract() -> None:
    contract = default_retail_dashboard_planning_contract()

    assert contract.plan_id
    assert contract.planned_sections
    assert contract.planned_cards
    assert REQUIRED_FORBIDDEN_INTERACTIONS.issubset(set(contract.forbidden_interactions))
    assert contract.active_ui_allowed is False
    assert contract.recommendations_allowed is False
    assert contract.execution_allowed is False


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
def test_retail_dashboard_planning_rejects_dangerous_flags(field_name: str) -> None:
    data = default_retail_dashboard_planning_contract().model_dump()
    data[field_name] = True

    with pytest.raises(ValidationError):
        RetailDashboardPlanningContract(**data)


def test_retail_dashboard_planning_enforces_unavailable_by_default() -> None:
    data = default_retail_dashboard_planning_contract().model_dump()
    data["returns_unavailable_by_default"] = False

    with pytest.raises(ValidationError):
        RetailDashboardPlanningContract(**data)


def test_retail_dashboard_planning_requires_sections_cards_and_forbidden_interactions() -> None:
    data = default_retail_dashboard_planning_contract().model_dump()
    data["planned_sections"] = []
    with pytest.raises(ValidationError):
        RetailDashboardPlanningContract(**data)

    data = default_retail_dashboard_planning_contract().model_dump()
    data["planned_cards"] = []
    with pytest.raises(ValidationError):
        RetailDashboardPlanningContract(**data)

    data = default_retail_dashboard_planning_contract().model_dump()
    data["planned_sections"] = [RetailDashboardSectionKind.UNKNOWN]
    with pytest.raises(ValidationError):
        RetailDashboardPlanningContract(**data)

    data = default_retail_dashboard_planning_contract().model_dump()
    data["planned_cards"] = [RetailDashboardCardKind.UNKNOWN]
    with pytest.raises(ValidationError):
        RetailDashboardPlanningContract(**data)

    data = default_retail_dashboard_planning_contract().model_dump()
    data["forbidden_interactions"] = [RetailDashboardForbiddenInteractionKind.RECOMMENDATION_CARD]
    with pytest.raises(ValidationError):
        RetailDashboardPlanningContract(**data)
