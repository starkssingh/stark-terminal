from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import EventPriority, EventSource, EventType
from stark_terminal_data_platform.event_backbone.serialization import (
    ensure_event_backbone_jsonable,
    event_backbone_dumps,
    event_backbone_loads,
)
from stark_terminal_data_platform.streams.events import EventEnvelope, create_event_envelope


class DurableEventValidationError(ValueError):
    """Raised when a durable event envelope cannot be validated."""


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_optional_key(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        raise DurableEventValidationError("durable event key cannot be empty")
    lowered = normalized.lower()
    if "://" in lowered or any(
        token in lowered
        for token in ("password", "secret", "token", "api_key", "broker", "credential")
    ):
        raise DurableEventValidationError("durable event key cannot contain secrets")
    ensure_event_backbone_jsonable({"key": normalized})
    return normalized


class DurableEventEnvelope(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: EventType
    source: EventSource
    priority: EventPriority = EventPriority.NORMAL
    schema_version: str
    topic: str
    payload: dict[str, object]
    key: str | None = None
    partition: int | None = None
    correlation_id: str | None = None
    causation_id: str | None = None
    audit_id: str | None = None
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("event_id", "schema_version", "topic")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise DurableEventValidationError("durable event text fields cannot be empty")
        return normalized

    @field_validator("key")
    @classmethod
    def key_must_be_safe(cls, value: str | None) -> str | None:
        return _safe_optional_key(value)

    @field_validator("partition")
    @classmethod
    def partition_must_be_non_negative(cls, value: int | None) -> int | None:
        if value is not None and value < 0:
            raise DurableEventValidationError("partition must be non-negative")
        return value

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
            ensure_event_backbone_jsonable(value)
        except ValueError as exc:
            raise DurableEventValidationError(str(exc)) from exc
        return value


def create_durable_event_envelope(
    event_type: EventType,
    source: EventSource,
    topic: str,
    payload: dict[str, object],
    settings: Settings | None = None,
    priority: EventPriority = EventPriority.NORMAL,
    key: str | None = None,
    partition: int | None = None,
    correlation_id: str | None = None,
    causation_id: str | None = None,
    audit_id: str | None = None,
) -> DurableEventEnvelope:
    resolved_settings = settings or get_settings()
    return DurableEventEnvelope(
        event_type=event_type,
        source=source,
        priority=priority,
        schema_version=resolved_settings.durable_event_schema_version,
        topic=topic,
        payload=payload,
        key=key,
        partition=partition,
        correlation_id=correlation_id,
        causation_id=causation_id,
        audit_id=audit_id,
    )


def durable_event_to_message(envelope: DurableEventEnvelope) -> dict[str, object]:
    return {
        "event_id": envelope.event_id,
        "event_type": envelope.event_type.value,
        "source": envelope.source.value,
        "priority": envelope.priority.value,
        "schema_version": envelope.schema_version,
        "topic": envelope.topic,
        "payload": envelope.payload,
        "key": envelope.key,
        "partition": envelope.partition,
        "correlation_id": envelope.correlation_id,
        "causation_id": envelope.causation_id,
        "audit_id": envelope.audit_id,
        "created_at": envelope.created_at.isoformat(),
    }


def durable_event_from_message(message: dict[str, Any]) -> DurableEventEnvelope:
    if "value" in message and "event_id" not in message:
        decoded = event_backbone_loads(message["value"])
        if not isinstance(decoded, dict):
            raise DurableEventValidationError("durable event message value must decode to a dict")
        message = decoded

    payload = message.get("payload")
    if isinstance(payload, str):
        payload = event_backbone_loads(payload)
    if not isinstance(payload, dict):
        raise DurableEventValidationError("durable event payload must be a dict")

    created_at = message.get("created_at")
    return DurableEventEnvelope(
        event_id=str(message["event_id"]),
        event_type=EventType(str(message["event_type"])),
        source=EventSource(str(message["source"])),
        priority=EventPriority(str(message.get("priority", EventPriority.NORMAL.value))),
        schema_version=str(message["schema_version"]),
        topic=str(message["topic"]),
        payload=payload,
        key=message.get("key") or None,
        partition=message.get("partition"),
        correlation_id=message.get("correlation_id") or None,
        causation_id=message.get("causation_id") or None,
        audit_id=message.get("audit_id") or None,
        created_at=(
            datetime.fromisoformat(created_at)
            if isinstance(created_at, str)
            else created_at or _utc_now()
        ),
    )


def durable_event_message_bytes(envelope: DurableEventEnvelope) -> bytes:
    return event_backbone_dumps(durable_event_to_message(envelope))


def from_stream_event(
    envelope: EventEnvelope,
    topic: str,
    key: str | None = None,
    partition: int | None = None,
    settings: Settings | None = None,
) -> DurableEventEnvelope:
    resolved_settings = settings or get_settings()
    return DurableEventEnvelope(
        event_id=envelope.event_id,
        event_type=envelope.event_type,
        source=envelope.source,
        priority=envelope.priority,
        schema_version=resolved_settings.durable_event_schema_version,
        topic=topic,
        payload=envelope.payload,
        key=key,
        partition=partition,
        correlation_id=envelope.correlation_id,
        causation_id=envelope.causation_id,
        audit_id=envelope.audit_id,
        created_at=envelope.created_at,
    )


def to_stream_event(
    envelope: DurableEventEnvelope,
    stream: str,
    settings: Settings | None = None,
) -> EventEnvelope:
    return create_event_envelope(
        event_type=envelope.event_type,
        source=envelope.source,
        stream=stream,
        payload=envelope.payload,
        settings=settings,
        priority=envelope.priority,
        correlation_id=envelope.correlation_id,
        causation_id=envelope.causation_id,
        audit_id=envelope.audit_id,
    ).model_copy(
        update={
            "event_id": envelope.event_id,
            "created_at": envelope.created_at,
        }
    )
