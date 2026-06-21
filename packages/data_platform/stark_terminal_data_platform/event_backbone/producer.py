from __future__ import annotations

from typing import Any

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import EventPriority, EventSource, EventType, TopicNamespace
from stark_terminal_data_platform.event_backbone.envelopes import (
    DurableEventEnvelope,
    create_durable_event_envelope,
    durable_event_message_bytes,
)
from stark_terminal_data_platform.event_backbone.memory import InMemoryEventBackbone
from stark_terminal_data_platform.event_backbone.topics import build_topic_name


class EventBackboneError(RuntimeError):
    """Base event-backbone error."""


class EventBackboneUnavailableError(EventBackboneError):
    """Raised when no event-backbone backend is available."""


def _kafka_config(settings: Settings) -> dict[str, Any]:
    config: dict[str, Any] = {
        "bootstrap.servers": settings.kafka_bootstrap_servers or "",
        "client.id": settings.kafka_client_id,
        "security.protocol": settings.kafka_security_protocol,
        "request.timeout.ms": settings.kafka_request_timeout_seconds * 1000,
    }
    if settings.kafka_sasl_username:
        config["sasl.username"] = settings.kafka_sasl_username
    if settings.kafka_sasl_password:
        config["sasl.password"] = settings.kafka_sasl_password
    return config


def _bootstrap_looks_invalid(value: str | None) -> bool:
    if not value:
        return False
    return "://" in value or any(part.strip() == "" for part in value.split(","))


class EventBackboneProducer:
    def __init__(
        self,
        settings: Settings | None = None,
        memory_backbone: InMemoryEventBackbone | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self._memory_backbone = memory_backbone
        self._kafka_producer: Any | None = None

    @property
    def backend(self) -> str:
        if self.settings.kafka_enabled and self.settings.kafka_bootstrap_servers:
            return "kafka"
        if self.settings.kafka_use_memory_fallback:
            return "memory"
        return "none"

    @property
    def memory_backbone(self) -> InMemoryEventBackbone | None:
        if self.backend != "memory":
            return None
        if self._memory_backbone is None:
            self._memory_backbone = InMemoryEventBackbone()
        return self._memory_backbone

    @property
    def kafka_producer(self) -> Any:
        if self.backend != "kafka":
            raise EventBackboneUnavailableError("Kafka/Redpanda backend is not configured")
        if _bootstrap_looks_invalid(self.settings.kafka_bootstrap_servers):
            raise EventBackboneUnavailableError("Kafka/Redpanda backend unavailable: invalid bootstrap")
        if self._kafka_producer is None:
            try:
                from confluent_kafka import Producer

                self._kafka_producer = Producer(_kafka_config(self.settings))
            except Exception as exc:
                raise EventBackboneUnavailableError(
                    f"Kafka/Redpanda backend unavailable: {exc.__class__.__name__}"
                ) from exc
        return self._kafka_producer

    def publish(self, envelope: DurableEventEnvelope) -> str:
        if self.backend == "memory":
            backbone = self.memory_backbone
            assert backbone is not None
            return backbone.publish(envelope.topic, envelope, key=envelope.key, partition=envelope.partition)
        if self.backend == "kafka":
            try:
                self.kafka_producer.produce(
                    topic=envelope.topic,
                    key=envelope.key,
                    value=durable_event_message_bytes(envelope),
                    partition=envelope.partition if envelope.partition is not None else -1,
                )
                return envelope.event_id
            except Exception as exc:
                raise EventBackboneUnavailableError(
                    f"event-backbone publish failed: {exc.__class__.__name__}"
                ) from exc
        raise EventBackboneUnavailableError("Event backbone unavailable")

    def publish_event(
        self,
        event_type: EventType,
        source: EventSource,
        namespace: TopicNamespace | str,
        payload: dict[str, object],
        priority: EventPriority = EventPriority.NORMAL,
        key: str | None = None,
        partition: int | None = None,
        correlation_id: str | None = None,
        causation_id: str | None = None,
        audit_id: str | None = None,
    ) -> str:
        topic = build_topic_name(namespace, settings=self.settings)
        envelope = create_durable_event_envelope(
            event_type=event_type,
            source=source,
            topic=topic,
            payload=payload,
            settings=self.settings,
            priority=priority,
            key=key,
            partition=partition,
            correlation_id=correlation_id,
            causation_id=causation_id,
            audit_id=audit_id,
        )
        return self.publish(envelope)

    def flush(self, timeout: float | None = None) -> None:
        if self._kafka_producer is not None:
            self._kafka_producer.flush(timeout if timeout is not None else 0)

    def close(self) -> None:
        try:
            self.flush(timeout=0)
        finally:
            self._kafka_producer = None

    def __enter__(self) -> EventBackboneProducer:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()
