import pytest

from stark_terminal_core.config.settings import Settings


def test_strategy_research_workspace_settings_defaults_are_safe():
    settings = Settings()

    assert settings.strategy_research_workspace_enabled is True
    assert settings.strategy_research_workspace_schema_version == "v1"
    assert settings.strategy_research_workspace_allow_active_ui is False
    assert settings.strategy_research_workspace_allow_frontend_components is False
    assert settings.strategy_research_workspace_allow_desktop_components is False
    assert settings.strategy_research_workspace_allow_paper_ingestion is False
    assert settings.strategy_research_workspace_allow_paper_parsing is False
    assert settings.strategy_research_workspace_allow_strategy_generation is False
    assert settings.strategy_research_workspace_allow_strategy_code_generation is False
    assert settings.strategy_research_workspace_allow_backtesting is False
    assert settings.strategy_research_workspace_allow_optimization is False
    assert settings.strategy_research_workspace_allow_recommendations is False
    assert settings.strategy_research_workspace_allow_action_generation is False
    assert settings.strategy_research_workspace_allow_confidence_scoring is False
    assert settings.strategy_research_workspace_allow_decision_object_generation is False
    assert settings.strategy_research_workspace_allow_readiness_to_trade is False
    assert settings.strategy_research_workspace_allow_broker_controls is False
    assert settings.strategy_research_workspace_allow_execution is False
    assert settings.strategy_research_workspace_allow_approval is False
    assert settings.strategy_research_workspace_allow_override is False
    assert settings.strategy_research_workspace_return_unavailable_by_default is True
    assert settings.strategy_research_workspace_stage == "planning_and_guardrails"


def test_safe_settings_snapshot_exposes_strategy_research_workspace_settings():
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["prompt_number"] == "107"
    assert snapshot["strategy_research_workspace_enabled"] is True
    assert snapshot["strategy_research_workspace_allow_strategy_generation"] is False
    assert snapshot["strategy_research_workspace_allow_backtesting"] is False
    assert snapshot["strategy_research_workspace_allow_execution"] is False
    assert snapshot["strategy_research_workspace_stage"] == "planning_and_guardrails"


@pytest.mark.parametrize(
    "field",
    [
        "strategy_research_workspace_allow_active_ui",
        "strategy_research_workspace_allow_frontend_components",
        "strategy_research_workspace_allow_desktop_components",
        "strategy_research_workspace_allow_paper_ingestion",
        "strategy_research_workspace_allow_paper_parsing",
        "strategy_research_workspace_allow_strategy_generation",
        "strategy_research_workspace_allow_strategy_code_generation",
        "strategy_research_workspace_allow_backtesting",
        "strategy_research_workspace_allow_optimization",
        "strategy_research_workspace_allow_recommendations",
        "strategy_research_workspace_allow_action_generation",
        "strategy_research_workspace_allow_confidence_scoring",
        "strategy_research_workspace_allow_decision_object_generation",
        "strategy_research_workspace_allow_readiness_to_trade",
        "strategy_research_workspace_allow_broker_controls",
        "strategy_research_workspace_allow_execution",
        "strategy_research_workspace_allow_approval",
        "strategy_research_workspace_allow_override",
    ],
)
def test_strategy_research_workspace_settings_reject_unsafe_flags(field):
    with pytest.raises(ValueError):
        Settings(**{field: True})


def test_strategy_research_workspace_settings_reject_available_by_default_disabled():
    with pytest.raises(ValueError):
        Settings(strategy_research_workspace_return_unavailable_by_default=False)
