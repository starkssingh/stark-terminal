from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.event_backbone.health import check_event_backbone_health
from stark_terminal_data_platform.event_backbone.topics import list_default_topic_names


def test_event_backbone_health_default_memory_fallback_is_reachable() -> None:
    status = check_event_backbone_health(Settings())

    assert status.reachable is True
    assert status.backend == "memory"
    assert status.memory_fallback_enabled is True
    assert status.default_topic_count == len(list_default_topic_names(Settings()))


def test_event_backbone_health_disabled_fallback_reports_none() -> None:
    status = check_event_backbone_health(Settings(kafka_use_memory_fallback=False))

    assert status.reachable is False
    assert status.backend == "none"
    assert status.error == "EventBackboneBackendDisabled"


def test_invalid_enabled_kafka_config_returns_unreachable() -> None:
    status = check_event_backbone_health(
        Settings(
            kafka_enabled=True,
            kafka_bootstrap_servers="bad://secret",
            kafka_sasl_username="secret-user",
            kafka_sasl_password="secret-password",
        )
    )

    payload = status.model_dump()
    assert status.reachable is False
    assert status.backend == "kafka"
    assert payload["bootstrap_servers_present"] is True
    assert "bad://secret" not in repr(payload)
    assert "secret-user" not in repr(payload)
    assert "secret-password" not in repr(payload)

