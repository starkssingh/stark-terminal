import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import EventSource, EventType, StreamNamespace
from stark_terminal_data_platform.streams.consumer import StreamConsumer
from stark_terminal_data_platform.streams.events import create_event_envelope
from stark_terminal_data_platform.streams.memory import InMemoryStreamStore
from stark_terminal_data_platform.streams.names import build_stream_name
from stark_terminal_data_platform.streams.producer import StreamProducer, StreamUnavailableError


def test_stream_producer_and_consumer_use_memory_fallback_by_default() -> None:
    producer = StreamProducer(Settings())
    consumer = StreamConsumer(Settings())

    assert producer.backend == "memory"
    assert consumer.backend == "memory"


def test_stream_producer_publish_and_consumer_read_roundtrip() -> None:
    settings = Settings()
    store = InMemoryStreamStore()
    stream = build_stream_name(StreamNamespace.SYSTEM, settings=settings)
    envelope = create_event_envelope(
        EventType.SYSTEM_HEALTH_RECORDED,
        EventSource.TEST,
        stream,
        {"status": "ok"},
        settings=settings,
    )

    record_id = StreamProducer(settings, store).publish(envelope)
    events = StreamConsumer(settings, store).read(stream)

    assert record_id == "1-0"
    assert events[0][2].event_id == envelope.event_id
    assert events[0][2].payload == {"status": "ok"}


def test_stream_producer_publish_event_helper() -> None:
    settings = Settings()
    store = InMemoryStreamStore()

    record_id = StreamProducer(settings, store).publish_event(
        EventType.FEATURE_COMPUTATION_REQUESTED,
        EventSource.API,
        StreamNamespace.FEATURES,
        {"dataset_id": "dataset-1"},
    )
    events = StreamConsumer(settings, store).read(build_stream_name(StreamNamespace.FEATURES, settings=settings))

    assert record_id == "1-0"
    assert events[0][2].event_type == EventType.FEATURE_COMPUTATION_REQUESTED
    assert events[0][2].payload["dataset_id"] == "dataset-1"


def test_stream_consumer_read_group_and_ack() -> None:
    settings = Settings()
    store = InMemoryStreamStore()
    stream = build_stream_name(StreamNamespace.AUDIT, settings=settings)
    envelope = create_event_envelope(
        EventType.AUDIT_RECORDED,
        EventSource.SYSTEM,
        stream,
        {"audit_id": "audit-1"},
        settings=settings,
    )

    StreamProducer(settings, store).publish(envelope)
    consumer = StreamConsumer(settings, store)
    entries = consumer.read_group(stream, group="group", consumer="consumer")

    assert entries[0][2].event_id == envelope.event_id
    assert consumer.ack(stream, "group", entries[0][1]) == 1


def test_stream_fallback_disabled_without_redis_is_safe() -> None:
    settings = Settings(redis_streams_use_memory_fallback=False)
    producer = StreamProducer(settings)
    consumer = StreamConsumer(settings)

    assert producer.backend == "none"
    assert consumer.backend == "none"
    with pytest.raises(StreamUnavailableError, match="Stream backend unavailable"):
        producer.publish_event(EventType.SYSTEM_HEALTH_RECORDED, EventSource.TEST, StreamNamespace.SYSTEM, {})
    with pytest.raises(StreamUnavailableError, match="Stream backend unavailable"):
        consumer.read("stark:development:system")


def test_stream_errors_do_not_include_raw_redis_url() -> None:
    settings = Settings(
        redis_streams_enabled=True,
        redis_url="redis://:secret@127.0.0.1:1/0",
        redis_streams_use_memory_fallback=False,
    )

    with pytest.raises(StreamUnavailableError) as exc_info:
        StreamProducer(settings).publish_event(
            EventType.SYSTEM_HEALTH_RECORDED,
            EventSource.TEST,
            StreamNamespace.SYSTEM,
            {"status": "ok"},
        )

    assert "secret" not in str(exc_info.value)
    assert "redis://" not in str(exc_info.value)

