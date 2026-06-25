import pytest

from stark_terminal_core.strategy_research_workspace_api.responses import (
    StrategyResearchWorkspaceAPIResponsePlaceholder,
    default_strategy_research_workspace_api_response_placeholder,
)


def test_strategy_research_workspace_api_response_placeholder_validates():
    placeholder = default_strategy_research_workspace_api_response_placeholder(request_id="request-id")

    assert placeholder.request_id == "request-id"
    assert placeholder.api_contract_skeleton_only is True
    assert placeholder.workspace_reference.reference_id
    assert placeholder.artifact_reference.reference_id
    assert placeholder.paper_reference.reference_id
    assert placeholder.hypothesis_reference.reference_id
    assert placeholder.dataset_reference.reference_id
    assert placeholder.experiment_reference.reference_id
    assert placeholder.safety_reference.reference_id
    assert placeholder.unavailable_response.unavailable is True
    assert placeholder.strategy_generated is False
    assert placeholder.execution_ready is False


def test_strategy_research_workspace_api_response_placeholder_requires_references():
    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIResponsePlaceholder(response_id="response-placeholder")


def test_strategy_research_workspace_api_response_placeholder_enforces_contract_only():
    base = default_strategy_research_workspace_api_response_placeholder().model_dump()
    base["api_contract_skeleton_only"] = False

    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIResponsePlaceholder(**base)


@pytest.mark.parametrize(
    "field",
    [
        "active_ui_generated",
        "frontend_component_generated",
        "desktop_component_generated",
        "paper_ingested",
        "paper_parsed",
        "strategy_generated",
        "strategy_code_generated",
        "backtest_generated",
        "optimization_generated",
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "broker_control_generated",
        "execution_ready",
        "approval_granted",
        "override_granted",
    ],
)
def test_strategy_research_workspace_api_response_placeholder_rejects_generated_flags(field):
    base = default_strategy_research_workspace_api_response_placeholder().model_dump()
    base[field] = True

    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIResponsePlaceholder(**base)
