import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayDatasetKind,
)
from stark_terminal_core.strategy_research_workspace_display.datasets import (
    StrategyResearchWorkspaceDisplayDatasetPlaceholder,
    default_strategy_research_workspace_display_dataset_placeholders,
)


def _dataset_kwargs(**overrides):
    base = {
        "dataset_reference_id": "dataset-placeholder-test",
        "dataset_kind": StrategyResearchWorkspaceDisplayDatasetKind.SYNTHETIC_DATASET_VISUAL_PLACEHOLDER,
        "title": "Dataset Placeholder",
    }
    base.update(overrides)
    return base


def test_strategy_research_workspace_display_dataset_placeholder_validates():
    dataset = StrategyResearchWorkspaceDisplayDatasetPlaceholder(**_dataset_kwargs())

    assert dataset.display_contract_only is True
    assert dataset.rendered_now is False
    assert dataset.real_market_data is False
    assert dataset.live_data is False
    assert dataset.validated_for_research is False
    assert dataset.validated_for_backtest is False
    assert dataset.validated_for_execution is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("dataset_kind", StrategyResearchWorkspaceDisplayDatasetKind.UNKNOWN),
        ("display_contract_only", False),
        ("rendered_now", True),
        ("real_market_data", True),
        ("live_data", True),
        ("validated_for_research", True),
        ("validated_for_backtest", True),
        ("validated_for_execution", True),
    ],
)
def test_strategy_research_workspace_display_dataset_rejects_unsafe_values(field, value):
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayDatasetPlaceholder(**_dataset_kwargs(**{field: value}))


def test_default_strategy_research_workspace_display_datasets_validate():
    datasets = default_strategy_research_workspace_display_dataset_placeholders()

    assert datasets
    assert all(dataset.display_contract_only for dataset in datasets)
    assert all(not dataset.real_market_data and not dataset.live_data for dataset in datasets)

