import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_display.artifacts import (
    StrategyResearchWorkspaceDisplayArtifactPlaceholder,
    default_strategy_research_workspace_display_artifact_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayArtifactKind,
)


def _artifact_kwargs(**overrides):
    base = {
        "artifact_id": "artifact-placeholder-test",
        "artifact_kind": StrategyResearchWorkspaceDisplayArtifactKind.PAPER_REFERENCE_VISUAL_PLACEHOLDER,
        "title": "Artifact Placeholder",
        "description": "Display contract only.",
    }
    base.update(overrides)
    return base


def test_strategy_research_workspace_display_artifact_placeholder_validates():
    artifact = StrategyResearchWorkspaceDisplayArtifactPlaceholder(**_artifact_kwargs())

    assert artifact.display_contract_only is True
    assert artifact.rendered_now is False
    assert artifact.validated is False
    assert artifact.strategy_ready is False
    assert artifact.recommendation_ready is False
    assert artifact.execution_ready is False
    assert artifact.paper_parsed is False
    assert artifact.backtest_ready is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", StrategyResearchWorkspaceDisplayArtifactKind.UNKNOWN),
        ("display_contract_only", False),
        ("rendered_now", True),
        ("validated", True),
        ("strategy_ready", True),
        ("recommendation_ready", True),
        ("execution_ready", True),
        ("paper_parsed", True),
        ("backtest_ready", True),
    ],
)
def test_strategy_research_workspace_display_artifact_rejects_unsafe_values(field, value):
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayArtifactPlaceholder(**_artifact_kwargs(**{field: value}))


def test_default_strategy_research_workspace_display_artifacts_validate():
    artifacts = default_strategy_research_workspace_display_artifact_placeholders()

    assert artifacts
    assert all(artifact.display_contract_only for artifact in artifacts)
    assert all(not artifact.strategy_ready and not artifact.execution_ready for artifact in artifacts)

