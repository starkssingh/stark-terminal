import pytest

from stark_terminal_core.strategy_research_workspace_api.requests import (
    StrategyResearchWorkspaceAPIRequestKind,
    StrategyResearchWorkspaceAPIRequestPlaceholder,
    default_strategy_research_workspace_api_request_placeholder,
)


def test_valid_strategy_research_workspace_api_request_placeholder():
    placeholder = StrategyResearchWorkspaceAPIRequestPlaceholder(
        request_id="request-placeholder",
        request_kind=StrategyResearchWorkspaceAPIRequestKind.WORKSPACE_OVERVIEW_REQUEST,
    )

    assert placeholder.safety_reference_required is True
    assert placeholder.active_ui_allowed is False
    assert placeholder.strategy_generation_allowed is False
    assert placeholder.execution_allowed is False


def test_strategy_research_workspace_api_request_unknown_kind_rejected():
    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIRequestPlaceholder(
            request_id="request-placeholder",
            request_kind=StrategyResearchWorkspaceAPIRequestKind.UNKNOWN,
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
        "approval_allowed",
        "override_allowed",
    ],
)
def test_strategy_research_workspace_api_request_rejects_dangerous_flags(field):
    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIRequestPlaceholder(
            request_id="request-placeholder",
            request_kind=StrategyResearchWorkspaceAPIRequestKind.WORKSPACE_OVERVIEW_REQUEST,
            **{field: True},
        )


def test_default_strategy_research_workspace_api_request_placeholder_validates():
    placeholder = default_strategy_research_workspace_api_request_placeholder()

    assert placeholder.request_id == "strategy-research-workspace-api-request-placeholder-v1"
    assert placeholder.safety_reference_required is True
    assert placeholder.requested_workspaces
    assert placeholder.requested_artifacts
    assert placeholder.requested_paper_references
    assert placeholder.requested_hypotheses
    assert placeholder.requested_dataset_references
    assert placeholder.requested_experiments
