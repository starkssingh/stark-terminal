import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayHypothesisKind,
)
from stark_terminal_core.strategy_research_workspace_display.hypotheses import (
    StrategyResearchWorkspaceDisplayHypothesisPlaceholder,
    default_strategy_research_workspace_display_hypothesis_placeholders,
)


def _hypothesis_kwargs(**overrides):
    base = {
        "hypothesis_id": "hypothesis-placeholder-test",
        "hypothesis_kind": StrategyResearchWorkspaceDisplayHypothesisKind.STRATEGY_HYPOTHESIS_VISUAL_PLACEHOLDER,
        "title": "Hypothesis Placeholder",
        "description": "Display contract only.",
    }
    base.update(overrides)
    return base


def test_strategy_research_workspace_display_hypothesis_placeholder_validates():
    hypothesis = StrategyResearchWorkspaceDisplayHypothesisPlaceholder(**_hypothesis_kwargs())

    assert hypothesis.display_contract_only is True
    assert hypothesis.rendered_now is False
    assert hypothesis.generated_strategy is False
    assert hypothesis.generated_signal is False
    assert hypothesis.generated_factor is False
    assert hypothesis.generated_code is False
    assert hypothesis.backtest_ready is False
    assert hypothesis.recommendation_ready is False
    assert hypothesis.execution_ready is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("hypothesis_kind", StrategyResearchWorkspaceDisplayHypothesisKind.UNKNOWN),
        ("display_contract_only", False),
        ("rendered_now", True),
        ("generated_strategy", True),
        ("generated_signal", True),
        ("generated_factor", True),
        ("generated_code", True),
        ("backtest_ready", True),
        ("recommendation_ready", True),
        ("execution_ready", True),
    ],
)
def test_strategy_research_workspace_display_hypothesis_rejects_unsafe_values(field, value):
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayHypothesisPlaceholder(**_hypothesis_kwargs(**{field: value}))


def test_default_strategy_research_workspace_display_hypotheses_validate():
    hypotheses = default_strategy_research_workspace_display_hypothesis_placeholders()

    assert hypotheses
    assert all(hypothesis.display_contract_only for hypothesis in hypotheses)
    assert all(not hypothesis.generated_strategy and not hypothesis.execution_ready for hypothesis in hypotheses)

