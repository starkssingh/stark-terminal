from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_strategy_research_workspace_boundary_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.strategy_research_workspace_boundary_enabled is True
    assert settings.strategy_research_workspace_boundary_schema_version == "v1"
    assert settings.strategy_research_workspace_boundary_allow_active_ui is False
    assert settings.strategy_research_workspace_boundary_allow_frontend_components is False
    assert settings.strategy_research_workspace_boundary_allow_desktop_components is False
    assert settings.strategy_research_workspace_boundary_allow_paper_ingestion is False
    assert settings.strategy_research_workspace_boundary_allow_paper_parsing is False
    assert settings.strategy_research_workspace_boundary_allow_strategy_generation is False
    assert settings.strategy_research_workspace_boundary_allow_strategy_code_generation is False
    assert settings.strategy_research_workspace_boundary_allow_backtesting is False
    assert settings.strategy_research_workspace_boundary_allow_optimization is False
    assert settings.strategy_research_workspace_boundary_allow_recommendations is False
    assert settings.strategy_research_workspace_boundary_allow_action_generation is False
    assert settings.strategy_research_workspace_boundary_allow_confidence_scoring is False
    assert settings.strategy_research_workspace_boundary_allow_decision_object_generation is False
    assert settings.strategy_research_workspace_boundary_allow_readiness_to_trade is False
    assert settings.strategy_research_workspace_boundary_allow_broker_controls is False
    assert settings.strategy_research_workspace_boundary_allow_execution is False
    assert settings.strategy_research_workspace_boundary_allow_approval is False
    assert settings.strategy_research_workspace_boundary_allow_override is False
    assert settings.strategy_research_workspace_boundary_stage == "boundary_hardening"


def test_strategy_research_workspace_boundary_settings_snapshot_is_safe() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["strategy_research_workspace_boundary_enabled"] is True
    assert snapshot["strategy_research_workspace_boundary_schema_version"] == "v1"
    assert snapshot["strategy_research_workspace_boundary_stage"] == "boundary_hardening"
    for key, value in snapshot.items():
        if key.startswith("strategy_research_workspace_boundary_allow_"):
            assert value is False


@pytest.mark.parametrize(
    "field_name",
    [
        "strategy_research_workspace_boundary_allow_active_ui",
        "strategy_research_workspace_boundary_allow_frontend_components",
        "strategy_research_workspace_boundary_allow_desktop_components",
        "strategy_research_workspace_boundary_allow_paper_ingestion",
        "strategy_research_workspace_boundary_allow_paper_parsing",
        "strategy_research_workspace_boundary_allow_strategy_generation",
        "strategy_research_workspace_boundary_allow_strategy_code_generation",
        "strategy_research_workspace_boundary_allow_backtesting",
        "strategy_research_workspace_boundary_allow_optimization",
        "strategy_research_workspace_boundary_allow_recommendations",
        "strategy_research_workspace_boundary_allow_action_generation",
        "strategy_research_workspace_boundary_allow_confidence_scoring",
        "strategy_research_workspace_boundary_allow_decision_object_generation",
        "strategy_research_workspace_boundary_allow_readiness_to_trade",
        "strategy_research_workspace_boundary_allow_broker_controls",
        "strategy_research_workspace_boundary_allow_execution",
        "strategy_research_workspace_boundary_allow_approval",
        "strategy_research_workspace_boundary_allow_override",
    ],
)
def test_strategy_research_workspace_boundary_rejects_dangerous_allow_flags(
    field_name: str,
) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field_name: True})


def test_strategy_research_workspace_boundary_stage_validation() -> None:
    assert Settings(
        strategy_research_workspace_boundary_stage="audit_only"
    ).strategy_research_workspace_boundary_stage == "audit_only"
    with pytest.raises(ValidationError):
        Settings(strategy_research_workspace_boundary_stage="active_ui")
