from __future__ import annotations

from stark_terminal_core.config.settings import Settings


def test_decision_evidence_validation_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.decision_evidence_validation_enabled is True
    assert settings.decision_evidence_validation_schema_version == "v1"
    assert settings.decision_evidence_validation_allow_recommendations is False
    assert settings.decision_evidence_validation_allow_action_generation is False
    assert settings.decision_evidence_validation_allow_confidence_scoring is False
    assert settings.decision_evidence_validation_allow_decision_object_generation is False
    assert settings.decision_evidence_validation_allow_execution is False
    assert settings.decision_evidence_validation_allow_approval is False
    assert settings.decision_evidence_validation_allow_override is False
    assert settings.decision_evidence_validation_allow_readiness_to_trade is False
    assert settings.decision_evidence_validation_stage == "validation_v0"


def test_decision_evidence_validation_safe_snapshot_exposes_only_safe_fields() -> None:
    snapshot = Settings().safe_settings_snapshot()

    expected = {
        "decision_evidence_validation_enabled": True,
        "decision_evidence_validation_schema_version": "v1",
        "decision_evidence_validation_allow_recommendations": False,
        "decision_evidence_validation_allow_action_generation": False,
        "decision_evidence_validation_allow_confidence_scoring": False,
        "decision_evidence_validation_allow_decision_object_generation": False,
        "decision_evidence_validation_allow_execution": False,
        "decision_evidence_validation_allow_approval": False,
        "decision_evidence_validation_allow_override": False,
        "decision_evidence_validation_allow_readiness_to_trade": False,
        "decision_evidence_validation_stage": "validation_v0",
    }
    for key, value in expected.items():
        assert snapshot[key] == value

    assert "password" not in snapshot
    assert "secret" not in snapshot

