import pytest

from stark_terminal_core.strategy_research_workspace.datasets import (
    StrategyResearchDatasetReferencePlaceholder,
    default_strategy_research_dataset_reference_placeholders,
)
from stark_terminal_core.strategy_research_workspace.planning import StrategyResearchDatasetReferenceKind


def test_strategy_research_dataset_reference_placeholders_validate():
    datasets = default_strategy_research_dataset_reference_placeholders()

    assert datasets
    for dataset in datasets:
        assert dataset.planning_only is True
        assert dataset.real_market_data is False
        assert dataset.live_data is False
        assert dataset.validated_for_research is False
        assert dataset.validated_for_backtest is False
        assert dataset.validated_for_execution is False


@pytest.mark.parametrize(
    "field",
    ["real_market_data", "live_data", "validated_for_research", "validated_for_backtest", "validated_for_execution"],
)
def test_strategy_research_dataset_reference_rejects_live_or_validated_flags(field):
    payload = default_strategy_research_dataset_reference_placeholders()[0].model_dump()
    payload[field] = True

    with pytest.raises(ValueError):
        StrategyResearchDatasetReferencePlaceholder(**payload)


def test_strategy_research_dataset_reference_rejects_unknown_kind():
    payload = default_strategy_research_dataset_reference_placeholders()[0].model_dump()
    payload["dataset_kind"] = StrategyResearchDatasetReferenceKind.UNKNOWN

    with pytest.raises(ValueError):
        StrategyResearchDatasetReferencePlaceholder(**payload)
