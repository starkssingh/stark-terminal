from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard.interactions import (
    RetailDashboardForbiddenInteraction,
    RetailDashboardForbiddenInteractionKind,
    default_retail_dashboard_forbidden_interactions,
)


REQUIRED_INTERACTIONS = {
    RetailDashboardForbiddenInteractionKind.RECOMMENDATION_CARD,
    RetailDashboardForbiddenInteractionKind.ACTION_BUTTON,
    RetailDashboardForbiddenInteractionKind.CONFIDENCE_SCORE,
    RetailDashboardForbiddenInteractionKind.DECISION_OBJECT_DISPLAY,
    RetailDashboardForbiddenInteractionKind.READINESS_TO_TRADE_BADGE,
    RetailDashboardForbiddenInteractionKind.BROKER_CONTROL,
    RetailDashboardForbiddenInteractionKind.ORDER_BUTTON,
    RetailDashboardForbiddenInteractionKind.APPROVAL_CONTROL,
    RetailDashboardForbiddenInteractionKind.OVERRIDE_CONTROL,
}


def _interaction(**overrides: object) -> RetailDashboardForbiddenInteraction:
    data = {
        "interaction_id": "interaction-test",
        "kind": RetailDashboardForbiddenInteractionKind.RECOMMENDATION_CARD,
        "name": "Recommendation card",
        "description": "Recommendation cards remain forbidden.",
    }
    data.update(overrides)
    return RetailDashboardForbiddenInteraction(**data)


def test_default_retail_dashboard_forbidden_interactions_validate() -> None:
    interactions = default_retail_dashboard_forbidden_interactions()

    assert interactions
    assert REQUIRED_INTERACTIONS.issubset({interaction.kind for interaction in interactions})
    assert all(interaction.forbidden_now is True for interaction in interactions)
    assert all(interaction.requires_future_prompt is True for interaction in interactions)
    assert all(interaction.requires_audit_before_unlock is True for interaction in interactions)


@pytest.mark.parametrize(
    "field_name",
    ["forbidden_now", "requires_future_prompt", "requires_audit_before_unlock"],
)
def test_retail_dashboard_forbidden_interaction_enforces_fail_closed_fields(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _interaction(**{field_name: False})


def test_retail_dashboard_forbidden_interaction_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _interaction(kind=RetailDashboardForbiddenInteractionKind.UNKNOWN)
