from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import EventPriority, EventSource, EventType
from stark_terminal_data_platform.streams.serialization import (
    ensure_stream_jsonable,
    stream_dumps,
    stream_loads,
)


class EventValidationError(ValueError):
    """Raised when an event envelope cannot be validated."""


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EventEnvelope(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: EventType
    source: EventSource
    priority: EventPriority = EventPriority.NORMAL
    schema_version: str
    stream: str
    payload: dict[str, object]
    correlation_id: str | None = None
    causation_id: str | None = None
    audit_id: str | None = None
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("event_id", "schema_version", "stream")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("event envelope text fields cannot be empty")
        return normalized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @field_validator("payload")
    @classmethod
    def payload_must_be_safe_json(cls, value: dict[str, object]) -> dict[str, object]:
        try:
            ensure_stream_jsonable(value)
        except ValueError as exc:
            raise EventValidationError(str(exc)) from exc
        return value


def create_event_envelope(
    event_type: EventType,
    source: EventSource,
    stream: str,
    payload: dict[str, object],
    settings: Settings | None = None,
    priority: EventPriority = EventPriority.NORMAL,
    correlation_id: str | None = None,
    causation_id: str | None = None,
    audit_id: str | None = None,
) -> EventEnvelope:
    resolved_settings = settings or get_settings()
    return EventEnvelope(
        event_type=event_type,
        source=source,
        priority=priority,
        schema_version=resolved_settings.event_schema_version,
        stream=stream,
        payload=payload,
        correlation_id=correlation_id,
        causation_id=causation_id,
        audit_id=audit_id,
    )


def _optional_text(value: str | None) -> str:
    return "" if value is None else value


def event_to_stream_fields(envelope: EventEnvelope) -> dict[str, str]:
    return {
        "event_id": envelope.event_id,
        "event_type": envelope.event_type.value,
        "source": envelope.source.value,
        "priority": envelope.priority.value,
        "schema_version": envelope.schema_version,
        "stream": envelope.stream,
        "payload": stream_dumps(envelope.payload),
        "correlation_id": _optional_text(envelope.correlation_id),
        "causation_id": _optional_text(envelope.causation_id),
        "audit_id": _optional_text(envelope.audit_id),
        "created_at": envelope.created_at.isoformat(),
    }


def _decode_stream_field(value: Any) -> str:
    if isinstance(value, bytes | bytearray):
        return bytes(value).decode("utf-8")
    return str(value)


def event_from_stream_fields(fields: dict[str, Any]) -> EventEnvelope:
    decoded = {_decode_stream_field(key): _decode_stream_field(value) for key, value in fields.items()}
    return EventEnvelope(
        event_id=decoded["event_id"],
        event_type=EventType(decoded["event_type"]),
        source=EventSource(decoded["source"]),
        priority=EventPriority(decoded["priority"]),
        schema_version=decoded["schema_version"],
        stream=decoded["stream"],
        payload=stream_loads(decoded["payload"]),
        correlation_id=decoded.get("correlation_id") or None,
        causation_id=decoded.get("causation_id") or None,
        audit_id=decoded.get("audit_id") or None,
        created_at=datetime.fromisoformat(decoded["created_at"]),
    )
