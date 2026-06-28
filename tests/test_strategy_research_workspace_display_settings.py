import pytest

from stark_terminal_core.config.settings import Settings


DISPLAY_FLAG_FIELDS = [
    "strategy_research_workspace_display_allow_active_ui",
    "strategy_research_workspace_display_allow_frontend_components",
    "strategy_research_workspace_display_allow_desktop_components",
    "strategy_research_workspace_display_allow_paper_ingestion",
    "strategy_research_workspace_display_allow_paper_parsing",
    "strategy_research_workspace_display_allow_strategy_generation",
    "strategy_research_workspace_display_allow_strategy_code_generation",
    "strategy_research_workspace_display_allow_backtesting",
    "strategy_research_workspace_display_allow_optimization",
    "strategy_research_workspace_display_allow_recommendations",
    "strategy_research_workspace_display_allow_action_generation",
    "strategy_research_workspace_display_allow_confidence_scoring",
    "strategy_research_workspace_display_allow_decision_object_generation",
    "strategy_research_workspace_display_allow_readiness_to_trade",
    "strategy_research_workspace_display_allow_broker_controls",
    "strategy_research_workspace_display_allow_execution",
    "strategy_research_workspace_display_allow_approval",
    "strategy_research_workspace_display_allow_override",
]


def test_strategy_research_workspace_display_settings_defaults_are_safe():
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.strategy_research_workspace_display_enabled is True
    assert settings.strategy_research_workspace_display_schema_version == "v1"
    for field in DISPLAY_FLAG_FIELDS:
        assert getattr(settings, field) is False
    assert settings.strategy_research_workspace_display_return_unavailable_by_default is True
    assert settings.strategy_research_workspace_display_stage == "display_contract_skeleton"


def test_safe_settings_snapshot_exposes_strategy_research_workspace_display_settings():
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["prompt_number"] == "107"
    assert snapshot["strategy_research_workspace_display_enabled"] is True
    assert snapshot["strategy_research_workspace_display_allow_strategy_generation"] is False
    assert snapshot["strategy_research_workspace_display_allow_backtesting"] is False
    assert snapshot["strategy_research_workspace_display_allow_execution"] is False
    assert snapshot["strategy_research_workspace_display_stage"] == "display_contract_skeleton"


@pytest.mark.parametrize("field", DISPLAY_FLAG_FIELDS)
def test_strategy_research_workspace_display_settings_reject_unsafe_flags(field):
    with pytest.raises(ValueError):
        Settings(**{field: True})


def test_strategy_research_workspace_display_settings_reject_available_by_default_disabled():
    with pytest.raises(ValueError):
        Settings(strategy_research_workspace_display_return_unavailable_by_default=False)
