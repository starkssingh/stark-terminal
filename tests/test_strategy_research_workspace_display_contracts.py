import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    STRATEGY_RESEARCH_WORKSPACE_DISPLAY_FORBIDDEN_OUTPUTS,
    StrategyResearchWorkspaceDisplayContractMetadata,
    StrategyResearchWorkspaceDisplayStage,
    default_strategy_research_workspace_display_contract_metadata,
)


DANGEROUS_CONTRACT_FLAGS = [
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
]


def _contract_kwargs(**overrides):
    base = default_strategy_research_workspace_display_contract_metadata().model_dump()
    base.update(overrides)
    return base


def test_default_strategy_research_workspace_display_contract_metadata_validates():
    contract = default_strategy_research_workspace_display_contract_metadata()

    assert isinstance(contract, StrategyResearchWorkspaceDisplayContractMetadata)
    assert contract.stage == StrategyResearchWorkspaceDisplayStage.DISPLAY_CONTRACT_SKELETON
    assert contract.returns_unavailable_by_default is True
    assert contract.workspace_kinds
    assert contract.artifact_kinds
    assert contract.paper_kinds
    assert contract.hypothesis_kinds
    assert contract.dataset_kinds
    assert contract.experiment_kinds
    assert contract.badge_kinds


@pytest.mark.parametrize("field", DANGEROUS_CONTRACT_FLAGS)
def test_strategy_research_workspace_display_contract_rejects_dangerous_flags(field):
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayContractMetadata(**_contract_kwargs(**{field: True}))


def test_strategy_research_workspace_display_contract_requires_unavailable_by_default():
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayContractMetadata(
            **_contract_kwargs(returns_unavailable_by_default=False)
        )


def test_strategy_research_workspace_display_contract_forbidden_outputs_are_complete():
    contract = default_strategy_research_workspace_display_contract_metadata()
    normalized = " ".join(contract.forbidden_outputs).lower().replace("_", " ")
    for phrase in [
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
    ]:
        assert phrase in normalized
    assert contract.forbidden_outputs == STRATEGY_RESEARCH_WORKSPACE_DISPLAY_FORBIDDEN_OUTPUTS

