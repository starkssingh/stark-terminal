import pytest

from stark_terminal_core.strategy_research_workspace.planning import StrategyResearchWorkspaceKind
from stark_terminal_core.strategy_research_workspace.workspaces import (
    StrategyResearchWorkspacePlaceholder,
    default_strategy_research_workspace_placeholders,
)


def test_strategy_research_workspace_placeholders_validate():
    placeholders = default_strategy_research_workspace_placeholders()

    assert placeholders
    for placeholder in placeholders:
        assert placeholder.planning_only is True
        assert placeholder.active_ui is False
        assert placeholder.unavailable is True
        assert placeholder.paper_ingestion_allowed is False
        assert placeholder.paper_parsing_allowed is False
        assert placeholder.strategy_generation_allowed is False
        assert placeholder.backtesting_allowed is False
        assert placeholder.recommendations_allowed is False
        assert placeholder.execution_allowed is False


@pytest.mark.parametrize(
    "field",
    [
        "active_ui",
        "paper_ingestion_allowed",
        "paper_parsing_allowed",
        "strategy_generation_allowed",
        "backtesting_allowed",
        "recommendations_allowed",
        "execution_allowed",
    ],
)
def test_strategy_research_workspace_placeholder_rejects_dangerous_flags(field):
    payload = default_strategy_research_workspace_placeholders()[0].model_dump()
    payload[field] = True

    with pytest.raises(ValueError):
        StrategyResearchWorkspacePlaceholder(**payload)


def test_strategy_research_workspace_placeholder_rejects_unknown_kind():
    payload = default_strategy_research_workspace_placeholders()[0].model_dump()
    payload["workspace_kind"] = StrategyResearchWorkspaceKind.UNKNOWN

    with pytest.raises(ValueError):
        StrategyResearchWorkspacePlaceholder(**payload)
