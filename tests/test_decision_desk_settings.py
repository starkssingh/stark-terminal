import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_decision_desk_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "67"
    assert settings.retail_decision_desk_enabled is True
    assert settings.retail_decision_desk_schema_version == "v1"
    assert settings.retail_decision_desk_allow_real_data is False
    assert settings.retail_decision_desk_allow_recommendations is False
    assert settings.retail_decision_desk_allow_action_generation is False
    assert settings.retail_decision_desk_allow_confidence_scoring is False
    assert settings.retail_decision_desk_allow_decision_objects is False
    assert settings.retail_decision_desk_allow_execution is False
    assert settings.retail_decision_desk_require_evidence is True
    assert settings.retail_decision_desk_require_human_review is True
    assert settings.retail_decision_desk_planning_stage == "planning_only"


def test_safe_settings_snapshot_exposes_decision_desk_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["retail_decision_desk_enabled"] is True
    assert snapshot["retail_decision_desk_schema_version"] == "v1"
    assert snapshot["retail_decision_desk_allow_real_data"] is False
    assert snapshot["retail_decision_desk_allow_recommendations"] is False
    assert snapshot["retail_decision_desk_allow_action_generation"] is False
    assert snapshot["retail_decision_desk_allow_confidence_scoring"] is False
    assert snapshot["retail_decision_desk_allow_decision_objects"] is False
    assert snapshot["retail_decision_desk_allow_execution"] is False
    assert snapshot["retail_decision_desk_require_evidence"] is True
    assert snapshot["retail_decision_desk_require_human_review"] is True
    assert snapshot["retail_decision_desk_planning_stage"] == "planning_only"


@pytest.mark.parametrize(
    "override",
    [
        {"retail_decision_desk_schema_version": " "},
        {"retail_decision_desk_allow_real_data": True},
        {"retail_decision_desk_allow_recommendations": True},
        {"retail_decision_desk_allow_action_generation": True},
        {"retail_decision_desk_allow_confidence_scoring": True},
        {"retail_decision_desk_allow_decision_objects": True},
        {"retail_decision_desk_allow_execution": True},
        {"retail_decision_desk_require_evidence": False},
        {"retail_decision_desk_require_human_review": False},
        {"retail_decision_desk_planning_stage": "unsafe"},
    ],
)
def test_decision_desk_unsafe_settings_fail_closed(override: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        Settings(**override)
