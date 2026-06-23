from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard.references import (
    RetailDashboardDataSourceReference,
    RetailDashboardDecisionReference,
    default_retail_dashboard_data_source_references,
    default_retail_dashboard_decision_reference,
)


def test_retail_dashboard_data_source_reference_validates() -> None:
    reference = RetailDashboardDataSourceReference(reference_id="source-test", source_name="placeholder-source")

    assert reference.real_market_data is False
    assert reference.display_ready is False
    assert default_retail_dashboard_data_source_references()


@pytest.mark.parametrize("field_name", ["real_market_data", "display_ready"])
def test_retail_dashboard_data_source_reference_rejects_unsafe_fields(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailDashboardDataSourceReference(
            reference_id="source-test",
            source_name="placeholder-source",
            **{field_name: True},
        )


def test_retail_dashboard_decision_reference_validates() -> None:
    reference = default_retail_dashboard_decision_reference()

    assert reference.active_decision_object is False
    assert reference.recommendation_available is False
    assert reference.readiness_to_trade_available is False
    assert reference.display_ready is False


@pytest.mark.parametrize(
    "field_name",
    ["active_decision_object", "recommendation_available", "readiness_to_trade_available", "display_ready"],
)
def test_retail_dashboard_decision_reference_rejects_unsafe_fields(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailDashboardDecisionReference(reference_id="decision-test", **{field_name: True})
