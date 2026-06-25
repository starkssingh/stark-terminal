import pytest

from stark_terminal_core.strategy_research_workspace.planning import StrategyResearchHypothesisKind
from stark_terminal_core.strategy_research_workspace.strategies import (
    StrategyResearchHypothesisPlaceholder,
    default_strategy_research_hypothesis_placeholders,
)


def test_strategy_research_hypothesis_placeholders_validate():
    hypotheses = default_strategy_research_hypothesis_placeholders()

    assert hypotheses
    for hypothesis in hypotheses:
        assert hypothesis.planning_only is True
        assert hypothesis.generated_strategy is False
        assert hypothesis.generated_signal is False
        assert hypothesis.generated_factor is False
        assert hypothesis.generated_code is False
        assert hypothesis.backtest_ready is False
        assert hypothesis.recommendation_ready is False
        assert hypothesis.execution_ready is False


@pytest.mark.parametrize(
    "field",
    [
        "generated_strategy",
        "generated_signal",
        "generated_factor",
        "generated_code",
        "backtest_ready",
        "recommendation_ready",
        "execution_ready",
    ],
)
def test_strategy_research_hypothesis_rejects_generated_or_ready_flags(field):
    payload = default_strategy_research_hypothesis_placeholders()[0].model_dump()
    payload[field] = True

    with pytest.raises(ValueError):
        StrategyResearchHypothesisPlaceholder(**payload)


def test_strategy_research_hypothesis_rejects_unknown_kind():
    payload = default_strategy_research_hypothesis_placeholders()[0].model_dump()
    payload["hypothesis_kind"] = StrategyResearchHypothesisKind.UNKNOWN

    with pytest.raises(ValueError):
        StrategyResearchHypothesisPlaceholder(**payload)
