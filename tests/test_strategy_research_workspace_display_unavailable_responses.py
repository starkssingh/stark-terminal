import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_display.unavailable import (
    StrategyResearchWorkspaceDisplayUnavailableResponse,
    default_strategy_research_workspace_display_unavailable_response,
)


DANGEROUS_UNAVAILABLE_FLAGS = [
    "active_ui_allowed",
    "frontend_components_allowed",
    "desktop_components_allowed",
    "paper_ingestion_allowed",
    "paper_parsing_allowed",
    "strategy_generation_allowed",
    "strategy_code_generation_allowed",
    "backtesting_allowed",
    "optimization_allowed",
    "recommendations_allowed",
    "action_generation_allowed",
    "confidence_scoring_allowed",
    "decision_object_generation_allowed",
    "readiness_to_trade_allowed",
    "broker_controls_allowed",
    "execution_allowed",
    "approval_granted",
    "override_granted",
]


def _unavailable_kwargs(**overrides):
    base = {
        "response_id": "display-unavailable-test",
        "message": "Unavailable by default.",
    }
    base.update(overrides)
    return base


def test_strategy_research_workspace_display_unavailable_response_validates():
    response = StrategyResearchWorkspaceDisplayUnavailableResponse(**_unavailable_kwargs())

    assert response.unavailable is True
    assert response.display_contract_only is True
    for field in DANGEROUS_UNAVAILABLE_FLAGS:
        assert getattr(response, field) is False


@pytest.mark.parametrize(
    "field,value",
    [("unavailable", False), ("display_contract_only", False)]
    + [(field, True) for field in DANGEROUS_UNAVAILABLE_FLAGS],
)
def test_strategy_research_workspace_display_unavailable_response_rejects_unsafe_values(
    field, value
):
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayUnavailableResponse(**_unavailable_kwargs(**{field: value}))


def test_default_strategy_research_workspace_display_unavailable_response_validates():
    response = default_strategy_research_workspace_display_unavailable_response()

    assert response.unavailable is True
    assert response.display_contract_only is True
    assert response.execution_allowed is False

