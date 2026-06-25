import pytest

from stark_terminal_core.strategy_research_workspace_api.contracts import (
    StrategyResearchWorkspaceAPIContractMetadata,
    default_strategy_research_workspace_api_contract_metadata,
)


def test_strategy_research_workspace_api_contract_metadata_validates():
    metadata = default_strategy_research_workspace_api_contract_metadata()

    assert metadata.service_name == "stark-terminal-strategy-research-workspace-api"
    assert metadata.returns_unavailable_by_default is True
    assert metadata.request_kinds
    assert metadata.unavailable_reasons
    assert metadata.forbidden_outputs


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
def test_strategy_research_workspace_api_contract_metadata_rejects_dangerous_flags(field):
    base = default_strategy_research_workspace_api_contract_metadata().model_dump()
    base[field] = True

    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIContractMetadata(**base)


def test_strategy_research_workspace_api_contract_metadata_enforces_unavailable_by_default():
    base = default_strategy_research_workspace_api_contract_metadata().model_dump()
    base["returns_unavailable_by_default"] = False

    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIContractMetadata(**base)


def test_strategy_research_workspace_api_contract_forbidden_outputs_are_complete():
    metadata = default_strategy_research_workspace_api_contract_metadata()
    normalized = " ".join(metadata.forbidden_outputs).lower().replace("_", " ")

    required = [
        "active ui",
        "frontend",
        "desktop",
        "paper ingestion",
        "paper parsing",
        "strategy generation",
        "strategy code generation",
        "backtesting",
        "optimization",
        "recommendation",
        "action",
        "confidence",
        "decisionobject",
        "readiness-to-trade",
        "broker",
        "execution",
        "approval",
        "override",
    ]
    for term in required:
        assert term in normalized


def test_strategy_research_workspace_api_contract_rejects_incomplete_forbidden_outputs():
    base = default_strategy_research_workspace_api_contract_metadata().model_dump()
    base["forbidden_outputs"] = ["active UI"]

    with pytest.raises(ValueError):
        StrategyResearchWorkspaceAPIContractMetadata(**base)
