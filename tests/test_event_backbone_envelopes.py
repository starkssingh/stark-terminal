from datetime import datetime, timezone

from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import EventPriority, EventSource, EventType, StreamNamespace, TopicNamespace
from stark_terminal_data_platform.event_backbone.envelopes import (
    DurableEventEnvelope,
    create_durable_event_envelope,
    durable_event_from_message,
    durable_event_to_message,
    from_stream_event,
    to_stream_event,
)
from stark_terminal_data_platform.event_backbone.topics import build_topic_name
from stark_terminal_data_platform.streams.events import create_event_envelope
from stark_terminal_data_platform.streams.names import build_stream_name


def test_valid_durable_event_envelope_creation() -> None:
    envelope = DurableEventEnvelope(
        event_type=EventType.SYSTEM_HEALTH_RECORDED,
        source=EventSource.TEST,
        schema_version="v1",
        topic="stark.development.system",
        payload={"status": "ok"},
    )

    assert envelope.event_id
    assert envelope.priority == EventPriority.NORMAL
    assert envelope.created_at.tzinfo is not None


def test_durable_event_helper_creates_uuid_and_utc_timestamp() -> None:
    envelope = create_durable_event_envelope(
        EventType.AUDIT_RECORDED,
        EventSource.SYSTEM,
        build_topic_name(TopicNamespace.AUDIT, settings=Settings()),
        {"audit_id": "audit-1"},
        settings=Settings(),
        key="audit-1",
    )

    assert envelope.event_id
    assert envelope.schema_version == "v1"
    assert envelope.created_at.utcoffset() == timezone.utc.utcoffset(envelope.created_at)


def test_durable_event_payload_must_be_json_serializable() -> None:
    with pytest.raises(ValidationError):
        DurableEventEnvelope(
            event_type=EventType.SYSTEM_HEALTH_RECORDED,
            source=EventSource.TEST,
            schema_version="v1",
            topic="stark.development.system",
            payload={"bad": object()},
        )


@pytest.mark.parametrize("payload", [{"kafka_bootstrap_servers": "localhost:9092"}, {"job": "order_placement"}])
def test_durable_event_rejects_forbidden_payloads(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        create_durable_event_envelope(
            EventType.SYSTEM_HEALTH_RECORDED,
            EventSource.TEST,
            "stark.development.system",
            payload,
            settings=Settings(),
        )


def test_durable_event_partition_validation() -> None:
    with pytest.raises(ValidationError):
        create_durable_event_envelope(
            EventType.SYSTEM_HEALTH_RECORDED,
            EventSource.TEST,
            "stark.development.system",
            {"status": "ok"},
            settings=Settings(),
            partition=-1,
        )


def test_durable_event_message_roundtrip() -> None:
    envelope = DurableEventEnvelope(
        event_id="event-1",
        event_type=EventType.AUDIT_RECORDED,
        source=EventSource.SYSTEM,
        schema_version="v1",
        topic="stark.development.audit",
        payload={"audit_id": "audit-1"},
        key="audit-1",
        partition=0,
        correlation_id="corr-1",
        causation_id="cause-1",
        audit_id="audit-1",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    restored = durable_event_from_message(durable_event_to_message(envelope))

    assert restored == envelope


def test_stream_event_compatibility_roundtrip_preserves_identity() -> None:
    stream_event = create_event_envelope(
        EventType.FEATURE_COMPUTATION_REQUESTED,
        EventSource.API,
        build_stream_name(StreamNamespace.FEATURES, settings=Settings()),
        {"feature_set": "sample"},
        settings=Settings(),
        correlation_id="corr-1",
        causation_id="cause-1",
        audit_id="audit-1",
    )

    durable = from_stream_event(
        stream_event,
        build_topic_name(TopicNamespace.FEATURES, settings=Settings()),
        key="feature-set",
        settings=Settings(),
    )
    restored = to_stream_event(durable, stream_event.stream, settings=Settings())

    assert durable.event_id == stream_event.event_id
    assert restored.event_id == stream_event.event_id
    assert restored.correlation_id == "corr-1"
    assert restored.causation_id == "cause-1"
    assert restored.audit_id == "audit-1"

