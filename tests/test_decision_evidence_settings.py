from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_decision_evidence_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "67"
    assert settings.decision_evidence_enabled is True
    assert settings.decision_evidence_schema_version == "v1"
    assert settings.decision_evidence_allow_real_data is False
    assert settings.decision_evidence_allow_recommendations is False
    assert settings.decision_evidence_allow_action_generation is False
    assert settings.decision_evidence_allow_confidence_scoring is False
    assert settings.decision_evidence_allow_decision_object_generation is False
    assert settings.decision_evidence_allow_execution is False
    assert settings.decision_evidence_require_source_reference is True
    assert settings.decision_evidence_require_validation_checklist is True
    assert settings.decision_evidence_require_human_review_attachment is True
    assert settings.decision_evidence_planning_stage == "contracts_only"


def test_decision_evidence_settings_fail_closed() -> None:
    unsafe_fields = [
        "decision_evidence_allow_real_data",
        "decision_evidence_allow_recommendations",
        "decision_evidence_allow_action_generation",
        "decision_evidence_allow_confidence_scoring",
        "decision_evidence_allow_decision_object_generation",
        "decision_evidence_allow_execution",
    ]

    for field in unsafe_fields:
        with pytest.raises(ValidationError):
            Settings(**{field: True})


def test_decision_evidence_settings_requirements_and_stage_validation() -> None:
    with pytest.raises(ValidationError):
        Settings(decision_evidence_require_source_reference=False)
    with pytest.raises(ValidationError):
        Settings(decision_evidence_require_validation_checklist=False)
    with pytest.raises(ValidationError):
        Settings(decision_evidence_require_human_review_attachment=False)
    with pytest.raises(ValidationError):
        Settings(decision_evidence_planning_stage="production")


def test_safe_settings_snapshot_exposes_decision_evidence_settings() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["decision_evidence_enabled"] is True
    assert snapshot["decision_evidence_schema_version"] == "v1"
    assert snapshot["decision_evidence_allow_real_data"] is False
    assert snapshot["decision_evidence_allow_recommendations"] is False
    assert snapshot["decision_evidence_allow_action_generation"] is False
    assert snapshot["decision_evidence_allow_confidence_scoring"] is False
    assert snapshot["decision_evidence_allow_decision_object_generation"] is False
    assert snapshot["decision_evidence_allow_execution"] is False
    assert snapshot["decision_evidence_require_source_reference"] is True
    assert snapshot["decision_evidence_require_validation_checklist"] is True
    assert snapshot["decision_evidence_require_human_review_attachment"] is True
    assert snapshot["decision_evidence_planning_stage"] == "contracts_only"
