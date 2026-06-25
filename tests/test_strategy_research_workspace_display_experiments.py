import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayExperimentKind,
)
from stark_terminal_core.strategy_research_workspace_display.experiments import (
    StrategyResearchWorkspaceDisplayExperimentPlaceholder,
    default_strategy_research_workspace_display_experiment_placeholders,
)


def _experiment_kwargs(**overrides):
    base = {
        "experiment_id": "experiment-placeholder-test",
        "experiment_kind": StrategyResearchWorkspaceDisplayExperimentKind.EXPERIMENT_PLAN_VISUAL_PLACEHOLDER,
        "title": "Experiment Placeholder",
        "description": "Display contract only.",
    }
    base.update(overrides)
    return base


def test_strategy_research_workspace_display_experiment_placeholder_validates():
    experiment = StrategyResearchWorkspaceDisplayExperimentPlaceholder(**_experiment_kwargs())

    assert experiment.display_contract_only is True
    assert experiment.rendered_now is False
    assert experiment.executable is False
    assert experiment.backtest_executable is False
    assert experiment.optimization_executable is False
    assert experiment.strategy_executable is False
    assert experiment.live_ready is False
    assert experiment.recommendation_ready is False
    assert experiment.execution_ready is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("experiment_kind", StrategyResearchWorkspaceDisplayExperimentKind.UNKNOWN),
        ("display_contract_only", False),
        ("rendered_now", True),
        ("executable", True),
        ("backtest_executable", True),
        ("optimization_executable", True),
        ("strategy_executable", True),
        ("live_ready", True),
        ("recommendation_ready", True),
        ("execution_ready", True),
    ],
)
def test_strategy_research_workspace_display_experiment_rejects_unsafe_values(field, value):
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayExperimentPlaceholder(**_experiment_kwargs(**{field: value}))


def test_default_strategy_research_workspace_display_experiments_validate():
    experiments = default_strategy_research_workspace_display_experiment_placeholders()

    assert experiments
    assert all(experiment.display_contract_only for experiment in experiments)
    assert all(not experiment.executable and not experiment.execution_ready for experiment in experiments)

