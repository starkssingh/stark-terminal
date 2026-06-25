from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_display.unavailable import (
    RetailTraderExperienceDisplayUnavailableResponse,
    default_retail_trader_experience_display_unavailable_response,
)


def _unavailable_kwargs(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "response_id": "display-unavailable-test",
        "message": "Unavailable display response.",
    }
    values.update(overrides)
    return values


def test_default_retail_trader_experience_display_unavailable_response_validates() -> None:
    response = default_retail_trader_experience_display_unavailable_response()

    assert response.unavailable is True
    assert response.display_contract_only is True
    assert response.active_ui_allowed is False
    assert response.execution_allowed is False
    assert response.suitability_profiling_allowed is False


@pytest.mark.parametrize(
    "field",
    [
        "unavailable",
        "display_contract_only",
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_granted",
        "override_granted",
        "suitability_profiling_allowed",
    ],
)
def test_retail_trader_experience_display_unavailable_response_rejects_unsafe_flags(
    field: str,
) -> None:
    value = False if field in {"unavailable", "display_contract_only"} else True
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayUnavailableResponse(**_unavailable_kwargs(**{field: value}))
