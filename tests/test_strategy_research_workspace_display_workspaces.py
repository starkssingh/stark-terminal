import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayWorkspaceKind,
)
from stark_terminal_core.strategy_research_workspace_display.workspaces import (
    StrategyResearchWorkspaceDisplayWorkspacePlaceholder,
    default_strategy_research_workspace_display_workspace_placeholders,
)


def _workspace_kwargs(**overrides):
    base = {
        "workspace_id": "workspace-placeholder-test",
        "workspace_kind": StrategyResearchWorkspaceDisplayWorkspaceKind.PAPER_RESEARCH_VISUAL_PLACEHOLDER,
        "title": "Workspace Placeholder",
        "description": "Display contract only.",
    }
    base.update(overrides)
    return base


def test_strategy_research_workspace_display_workspace_placeholder_validates():
    workspace = StrategyResearchWorkspaceDisplayWorkspacePlaceholder(**_workspace_kwargs())

    assert workspace.display_contract_only is True
    assert workspace.active_ui is False
    assert workspace.rendered_now is False
    assert workspace.unavailable is True


@pytest.mark.parametrize(
    "field,value",
    [
        ("workspace_kind", StrategyResearchWorkspaceDisplayWorkspaceKind.UNKNOWN),
        ("display_contract_only", False),
        ("active_ui", True),
        ("rendered_now", True),
        ("unavailable", False),
        ("paper_ingestion_allowed", True),
        ("paper_parsing_allowed", True),
        ("strategy_generation_allowed", True),
        ("backtesting_allowed", True),
        ("recommendations_allowed", True),
        ("execution_allowed", True),
    ],
)
def test_strategy_research_workspace_display_workspace_rejects_unsafe_values(field, value):
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayWorkspacePlaceholder(**_workspace_kwargs(**{field: value}))


def test_default_strategy_research_workspace_display_workspaces_validate():
    workspaces = default_strategy_research_workspace_display_workspace_placeholders()

    assert workspaces
    assert all(workspace.display_contract_only for workspace in workspaces)
    assert all(not workspace.active_ui and not workspace.rendered_now for workspace in workspaces)

