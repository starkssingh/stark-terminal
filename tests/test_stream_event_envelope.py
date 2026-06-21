from datetime import datetime, timezone

from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import EventPriority, EventSource, EventType, StreamNamespace
from stark_terminal_data_platform.streams.events import (
    EventEnvelope,
    create_event_envelope,
    event_from_stream_fields,
    event_to_stream_fields,
)
from stark_terminal_data_platform.streams.names import build_stream_name


def test_valid_event_envelope_creation() -> None:
    envelope = EventEnvelope(
        event_type=EventType.SYSTEM_HEALTH_RECORDED,
        source=EventSource.TEST,
        schema_version="v1",
        stream="stark:development:system",
        payload={"status": "ok"},
    )

    assert envelope.event_id
    assert envelope.priority == EventPriority.NORMAL
    assert envelope.created_at.tzinfo is not None


def test_event_envelope_helper_creates_uuid_and_utc_timestamp() -> None:
    envelope = create_event_envelope(
        EventType.INGESTION_REQUESTED,
        EventSource.API,
        build_stream_name(StreamNamespace.INGESTION, settings=Settings()),
        {"symbol": "RELIANCE"},
        settings=Settings(),
    )

    assert envelope.event_id
    assert envelope.schema_version == "v1"
    assert envelope.created_at.tzinfo is not None
    assert envelope.created_at.utcoffset() == timezone.utc.utcoffset(envelope.created_at)


def test_event_envelope_payload_must_be_json_serializable() -> None:
    with pytest.raises(ValidationError):
        EventEnvelope(
            event_type=EventType.SYSTEM_HEALTH_RECORDED,
            source=EventSource.TEST,
            schema_version="v1",
            stream="stark:development:system",
            payload={"bad": object()},
        )


def test_event_envelope_rejects_forbidden_secret_like_payload_keys() -> None:
    with pytest.raises(ValidationError):
        create_event_envelope(
            EventType.SYSTEM_HEALTH_RECORDED,
            EventSource.TEST,
            "stark:development:system",
            {"redis_url": "redis://:secret@localhost:6379"},
            settings=Settings(),
        )


def test_event_to_stream_fields_roundtrip() -> None:
    envelope = EventEnvelope(
        event_id="event-1",
        event_type=EventType.AUDIT_RECORDED,
        source=EventSource.SYSTEM,
        schema_version="v1",
        stream="stark:development:audit",
        payload={"audit_id": "audit-1"},
        correlation_id="corr-1",
        causation_id="cause-1",
        audit_id="audit-1",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    restored = event_from_stream_fields(event_to_stream_fields(envelope))

    assert restored == envelope

