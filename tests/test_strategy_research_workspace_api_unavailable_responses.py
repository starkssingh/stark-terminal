import pytest

from stark_terminal_core.strategy_research_workspace_api.requests import (
    StrategyResearchWorkspaceAPIUnavailableReason,
)
from stark_terminal_core.strategy_research_workspace_api.unavailable import (
    StrategyResearchWorkspaceAPIUnavailableResponse,
    default_strategy_research_workspace_api_unavailable_response,
)


def test_strategy_research_workspace_api_unavailable_response_validates():
    response = default_strategy_research_workspace_api_unavailable_response()

    assert response.unavailable is True
    assert response.api_contract_skeleton_only is True
    assert response.reason == StrategyResearchWorkspaceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY
    assert response.execution_allowed is False


def test_strategy_research_workspace_api_unavailable_response_enforces_unavailable_true():
    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIUnavailableResponse(
            response_id="unavailable",
            unavailable=False,
            reason=StrategyResearchWorkspaceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
            message="Blocked",
        )


def test_strategy_research_workspace_api_unavailable_response_rejects_unknown_reason():
    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIUnavailableResponse(
            response_id="unavailable",
            reason=StrategyResearchWorkspaceAPIUnavailableReason.UNKNOWN,
            message="Blocked",
        )


@pytest.mark.parametrize(
    "field",
    [
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
    ],
)
def test_strategy_research_workspace_api_unavailable_response_rejects_dangerous_flags(field):
    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIUnavailableResponse(
            response_id="unavailable",
            reason=StrategyResearchWorkspaceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
            message="Blocked",
            **{field: True},
        )


def test_strategy_research_workspace_api_unavailable_response_enforces_contract_only():
    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIUnavailableResponse(
            response_id="unavailable",
            reason=StrategyResearchWorkspaceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
            message="Blocked",
            api_contract_skeleton_only=False,
        )
