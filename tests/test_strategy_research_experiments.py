import pytest

from stark_terminal_core.strategy_research_workspace.experiments import (
    StrategyResearchExperimentPlaceholder,
    default_strategy_research_experiment_placeholders,
)
from stark_terminal_core.strategy_research_workspace.planning import StrategyResearchExperimentKind


def test_strategy_research_experiment_placeholders_validate():
    experiments = default_strategy_research_experiment_placeholders()

    assert experiments
    for experiment in experiments:
        assert experiment.planning_only is True
        assert experiment.executable is False
        assert experiment.backtest_executable is False
        assert experiment.optimization_executable is False
        assert experiment.strategy_executable is False
        assert experiment.live_ready is False
        assert experiment.recommendation_ready is False
        assert experiment.execution_ready is False


@pytest.mark.parametrize(
    "field",
    [
        "executable",
        "backtest_executable",
        "optimization_executable",
        "strategy_executable",
        "live_ready",
        "recommendation_ready",
        "execution_ready",
    ],
)
def test_strategy_research_experiment_rejects_executable_or_ready_flags(field):
    payload = default_strategy_research_experiment_placeholders()[0].model_dump()
    payload[field] = True

    with pytest.raises(ValueError):
        StrategyResearchExperimentPlaceholder(**payload)


def test_strategy_research_experiment_rejects_unknown_kind():
    payload = default_strategy_research_experiment_placeholders()[0].model_dump()
    payload["experiment_kind"] = StrategyResearchExperimentKind.UNKNOWN

    with pytest.raises(ValueError):
        StrategyResearchExperimentPlaceholder(**payload)
