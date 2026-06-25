import pytest

from stark_terminal_core.strategy_research_workspace_api.references import (
    StrategyResearchWorkspaceAPIArtifactReference,
    StrategyResearchWorkspaceAPIDatasetReference,
    StrategyResearchWorkspaceAPIExperimentReference,
    StrategyResearchWorkspaceAPIHypothesisReference,
    StrategyResearchWorkspaceAPIPaperReference,
    StrategyResearchWorkspaceAPISafetyReference,
    StrategyResearchWorkspaceAPIWorkspaceReference,
    default_strategy_research_workspace_api_artifact_reference,
    default_strategy_research_workspace_api_dataset_reference,
    default_strategy_research_workspace_api_experiment_reference,
    default_strategy_research_workspace_api_hypothesis_reference,
    default_strategy_research_workspace_api_paper_reference,
    default_strategy_research_workspace_api_safety_reference,
    default_strategy_research_workspace_api_workspace_reference,
)


@pytest.mark.parametrize(
    ("model", "default_factory", "dangerous_fields"),
    [
        (
            StrategyResearchWorkspaceAPIWorkspaceReference,
            default_strategy_research_workspace_api_workspace_reference,
            [
                "active_workspace",
                "active_ui",
                "paper_ingestion_available",
                "paper_parsing_available",
                "strategy_generation_available",
                "backtesting_available",
                "recommendation_available",
                "execution_available",
                "display_ready",
            ],
        ),
        (
            StrategyResearchWorkspaceAPIArtifactReference,
            default_strategy_research_workspace_api_artifact_reference,
            [
                "validated_artifact",
                "parsed_paper_artifact",
                "strategy_ready_artifact",
                "backtest_ready_artifact",
                "recommendation_ready_artifact",
                "execution_ready_artifact",
                "display_ready",
            ],
        ),
        (
            StrategyResearchWorkspaceAPIPaperReference,
            default_strategy_research_workspace_api_paper_reference,
            [
                "paper_ingested",
                "paper_parsed",
                "method_extracted",
                "strategy_extracted",
                "code_generated",
                "backtest_generated",
                "recommendation_generated",
                "display_ready",
            ],
        ),
        (
            StrategyResearchWorkspaceAPIHypothesisReference,
            default_strategy_research_workspace_api_hypothesis_reference,
            [
                "generated_strategy",
                "generated_signal",
                "generated_factor",
                "generated_code",
                "backtest_ready",
                "recommendation_ready",
                "execution_ready",
                "display_ready",
            ],
        ),
        (
            StrategyResearchWorkspaceAPIDatasetReference,
            default_strategy_research_workspace_api_dataset_reference,
            [
                "real_market_data",
                "live_data",
                "validated_for_research",
                "validated_for_backtest",
                "validated_for_execution",
                "display_ready",
            ],
        ),
        (
            StrategyResearchWorkspaceAPIExperimentReference,
            default_strategy_research_workspace_api_experiment_reference,
            [
                "executable",
                "backtest_executable",
                "optimization_executable",
                "strategy_executable",
                "live_ready",
                "recommendation_ready",
                "execution_ready",
                "display_ready",
            ],
        ),
        (
            StrategyResearchWorkspaceAPISafetyReference,
            default_strategy_research_workspace_api_safety_reference,
            [
                "safety_passed",
                "approval_granted",
                "override_granted",
                "readiness_to_trade_allowed",
                "broker_controls_allowed",
                "execution_allowed",
            ],
        ),
    ],
)
def test_strategy_research_workspace_api_references_validate_and_reject_dangerous_flags(
    model,
    default_factory,
    dangerous_fields,
):
    reference = default_factory()

    assert reference.reference_id
    for field in dangerous_fields:
        assert getattr(reference, field) is False
        with pytest.raises(ValueError):
            model(reference_id="reference-placeholder", **{field: True})
