import pytest

from stark_terminal_core.strategy_research_workspace.artifacts import (
    StrategyResearchArtifactPlaceholder,
    default_strategy_research_artifact_placeholders,
)
from stark_terminal_core.strategy_research_workspace.planning import StrategyResearchArtifactKind


def test_strategy_research_artifact_placeholders_validate():
    artifacts = default_strategy_research_artifact_placeholders()

    assert artifacts
    for artifact in artifacts:
        assert artifact.planning_only is True
        assert artifact.validated is False
        assert artifact.strategy_ready is False
        assert artifact.recommendation_ready is False
        assert artifact.execution_ready is False
        assert artifact.paper_parsed is False
        assert artifact.backtest_ready is False


@pytest.mark.parametrize(
    "field",
    ["validated", "strategy_ready", "recommendation_ready", "execution_ready", "paper_parsed", "backtest_ready"],
)
def test_strategy_research_artifact_rejects_ready_or_validated_flags(field):
    payload = default_strategy_research_artifact_placeholders()[0].model_dump()
    payload[field] = True

    with pytest.raises(ValueError):
        StrategyResearchArtifactPlaceholder(**payload)


def test_strategy_research_artifact_rejects_unknown_kind():
    payload = default_strategy_research_artifact_placeholders()[0].model_dump()
    payload["artifact_kind"] = StrategyResearchArtifactKind.UNKNOWN

    with pytest.raises(ValueError):
        StrategyResearchArtifactPlaceholder(**payload)
