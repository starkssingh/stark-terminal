from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import EventSource, EventType, TopicNamespace
from stark_terminal_data_platform.event_backbone.envelopes import create_durable_event_envelope
from stark_terminal_data_platform.event_backbone.memory import InMemoryEventBackbone
from stark_terminal_data_platform.event_backbone.topics import build_topic_name


def _event(topic: str, symbol: str = "RELIANCE"):
    return create_durable_event_envelope(
        EventType.INGESTION_REQUESTED,
        EventSource.TEST,
        topic,
        {"symbol": symbol},
        settings=Settings(),
    )


def test_memory_backbone_publish_consume_count_and_topics() -> None:
    topic = build_topic_name(TopicNamespace.INGESTION, settings=Settings())
    backbone = InMemoryEventBackbone()
    envelope = _event(topic)

    event_id = backbone.publish(topic, envelope)

    assert event_id == envelope.event_id
    assert backbone.count() == 1
    assert backbone.count(topic) == 1
    assert backbone.list_topics() == [topic]
    assert backbone.consume(topic)[0].event_id == envelope.event_id


def test_memory_backbone_offset_limit_and_clear() -> None:
    topic = build_topic_name(TopicNamespace.INGESTION, settings=Settings())
    backbone = InMemoryEventBackbone()
    backbone.publish(topic, _event(topic, "A"))
    backbone.publish(topic, _event(topic, "B"))
    backbone.publish(topic, _event(topic, "C"))

    events = backbone.consume(topic, offset=1, limit=1)

    assert len(events) == 1
    assert events[0].payload["symbol"] == "B"
    backbone.clear()
    assert backbone.count() == 0


def test_memory_backbone_has_no_shared_global_state() -> None:
    topic = build_topic_name(TopicNamespace.SYSTEM, settings=Settings())
    first = InMemoryEventBackbone()
    second = InMemoryEventBackbone()

    first.publish(topic, _event(topic))

    assert first.count() == 1
    assert second.count() == 0

