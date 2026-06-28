from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_event_backbone_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "107"
    assert settings.event_backbone_mode == "memory"
    assert settings.kafka_enabled is False
    assert settings.kafka_use_memory_fallback is True
    assert settings.kafka_default_partitions == 3
    assert settings.kafka_replication_factor == 1
    assert settings.durable_event_schema_version == "v1"


def test_kafka_secrets_are_not_exposed_in_safe_snapshot() -> None:
    settings = Settings(
        kafka_bootstrap_servers="localhost:9092",
        kafka_sasl_username="user-secret",
        kafka_sasl_password="password-secret",
    )

    snapshot = settings.safe_settings_snapshot()
    snapshot_text = repr(snapshot)

    assert "kafka_bootstrap_servers" not in snapshot
    assert "kafka_sasl_username" not in snapshot
    assert "kafka_sasl_password" not in snapshot
    assert "user-secret" not in snapshot_text
    assert "password-secret" not in snapshot_text
    assert snapshot["kafka_configured"] is True
    assert snapshot["kafka_enabled"] is False
    assert snapshot["event_backbone_mode"] == "memory"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("kafka_default_partitions", 0),
        ("kafka_replication_factor", 0),
        ("kafka_request_timeout_seconds", 0),
        ("kafka_topic_prefix", ""),
        ("kafka_environment_namespace", ""),
        ("durable_event_schema_version", ""),
        ("event_backbone_mode", "unsupported"),
        ("kafka_topic_prefix", "../bad"),
    ],
)
def test_event_backbone_settings_validation(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})


@pytest.mark.parametrize("mode", ["memory", "kafka", "redpanda", "disabled"])
def test_event_backbone_supported_modes(mode: str) -> None:
    assert Settings(event_backbone_mode=mode).event_backbone_mode == mode
