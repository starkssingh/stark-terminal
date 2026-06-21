import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import EventSource, EventType, TopicNamespace
from stark_terminal_data_platform.event_backbone.consumer import EventBackboneConsumer
from stark_terminal_data_platform.event_backbone.envelopes import create_durable_event_envelope
from stark_terminal_data_platform.event_backbone.memory import InMemoryEventBackbone
from stark_terminal_data_platform.event_backbone.producer import (
    EventBackboneProducer,
    EventBackboneUnavailableError,
)
from stark_terminal_data_platform.event_backbone.topics import build_topic_name


def test_default_settings_use_memory_fallback() -> None:
    producer = EventBackboneProducer(Settings())

    assert producer.backend == "memory"
    assert producer.memory_backbone is not None


def test_producer_consumer_memory_roundtrip() -> None:
    settings = Settings()
    topic = build_topic_name(TopicNamespace.SYSTEM, settings=settings)
    memory = InMemoryEventBackbone()
    producer = EventBackboneProducer(settings, memory)
    consumer = EventBackboneConsumer(settings, memory)
    envelope = create_durable_event_envelope(
        EventType.SYSTEM_HEALTH_RECORDED,
        EventSource.TEST,
        topic,
        {"status": "ok"},
        settings=settings,
    )

    event_id = producer.publish(envelope)
    events = consumer.consume(topic)

    assert events[0].event_id == event_id
    assert events[0].payload["status"] == "ok"


def test_publish_event_helper() -> None:
    settings = Settings()
    memory = InMemoryEventBackbone()
    producer = EventBackboneProducer(settings, memory)
    consumer = EventBackboneConsumer(settings, memory)
    topic = build_topic_name(TopicNamespace.AUDIT, settings=settings)

    event_id = producer.publish_event(
        EventType.AUDIT_RECORDED,
        EventSource.SYSTEM,
        TopicNamespace.AUDIT,
        {"audit_id": "audit-1"},
        key="audit-1",
    )

    events = consumer.consume(topic)
    assert events[0].event_id == event_id
    assert events[0].key == "audit-1"


def test_fallback_disabled_without_kafka_returns_safe_unavailable_behavior() -> None:
    settings = Settings(kafka_use_memory_fallback=False)
    producer = EventBackboneProducer(settings)
    consumer = EventBackboneConsumer(settings)

    assert producer.backend == "none"
    with pytest.raises(EventBackboneUnavailableError):
        producer.publish_event(
            EventType.SYSTEM_HEALTH_RECORDED,
            EventSource.TEST,
            TopicNamespace.SYSTEM,
            {"status": "ok"},
        )
    with pytest.raises(EventBackboneUnavailableError):
        consumer.consume("stark.development.system")


def test_errors_do_not_include_raw_kafka_bootstrap_or_credentials() -> None:
    settings = Settings(
        kafka_enabled=True,
        kafka_bootstrap_servers="bad://secret-bootstrap",
        kafka_sasl_username="secret-user",
        kafka_sasl_password="secret-password",
        kafka_use_memory_fallback=False,
    )
    producer = EventBackboneProducer(settings)

    with pytest.raises(EventBackboneUnavailableError) as exc_info:
        producer.publish_event(
            EventType.SYSTEM_HEALTH_RECORDED,
            EventSource.TEST,
            TopicNamespace.SYSTEM,
            {"status": "ok"},
        )

    message = str(exc_info.value)
    assert "secret-bootstrap" not in message
    assert "secret-user" not in message
    assert "secret-password" not in message

