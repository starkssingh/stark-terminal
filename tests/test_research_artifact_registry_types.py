from __future__ import annotations

from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactKind,
    ResearchArtifactLifecycleStatus,
)


def test_expected_research_artifact_kinds_exist() -> None:
    expected = {
        "PAPER_REFERENCE",
        "DATASET_REFERENCE",
        "HYPOTHESIS_REFERENCE",
        "EXPERIMENT_REFERENCE",
        "NOTEBOOK_REFERENCE",
        "CODE_REFERENCE",
        "REPORT_REFERENCE",
        "BACKTEST_REFERENCE_PLACEHOLDER",
        "STRATEGY_REFERENCE_PLACEHOLDER",
        "UNKNOWN",
    }

    assert expected.issubset({kind.value for kind in ResearchArtifactKind})
    assert "PLACEHOLDER" in ResearchArtifactKind.BACKTEST_REFERENCE_PLACEHOLDER.value
    assert "PLACEHOLDER" in ResearchArtifactKind.STRATEGY_REFERENCE_PLACEHOLDER.value


def test_lifecycle_statuses_do_not_include_trading_ready_states() -> None:
    lifecycle_values = {status.value.lower() for status in ResearchArtifactLifecycleStatus}
    joined = " ".join(lifecycle_values)

    assert "approved_strategy" not in joined
    assert "validated_strategy" not in joined
    assert "recommendation" not in joined
    assert "readiness_to_trade" not in joined
    assert "execution_ready" not in joined

