from __future__ import annotations

from typing import Any

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.event_backbone.envelopes import (
    DurableEventEnvelope,
    durable_event_from_message,
)
from stark_terminal_data_platform.event_backbone.memory import InMemoryEventBackbone
from stark_terminal_data_platform.event_backbone.producer import (
    EventBackboneUnavailableError,
    _kafka_config,
)


class EventBackboneConsumer:
    def __init__(
        self,
        settings: Settings | None = None,
        memory_backbone: InMemoryEventBackbone | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self._memory_backbone = memory_backbone
        self._kafka_consumer: Any | None = None
        self._subscriptions: list[str] = []

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
    def kafka_consumer(self) -> Any:
        if self.backend != "kafka":
            raise EventBackboneUnavailableError("Kafka/Redpanda backend is not configured")
        if self._kafka_consumer is None:
            try:
                from confluent_kafka import Consumer

                config = _kafka_config(self.settings)
                config.update(
                    {
                        "group.id": f"{self.settings.kafka_client_id}-foundation",
                        "auto.offset.reset": "earliest",
                        "enable.auto.commit": False,
                    }
                )
                self._kafka_consumer = Consumer(config)
            except Exception as exc:
                raise EventBackboneUnavailableError(
                    f"Kafka/Redpanda backend unavailable: {exc.__class__.__name__}"
                ) from exc
        return self._kafka_consumer

    def subscribe(self, topics: list[str]) -> None:
        self._subscriptions = list(topics)
        if self.backend == "kafka":
            try:
                self.kafka_consumer.subscribe(self._subscriptions)
            except Exception as exc:
                raise EventBackboneUnavailableError(
                    f"event-backbone subscribe failed: {exc.__class__.__name__}"
                ) from exc

    def consume(
        self,
        topic: str,
        offset: int = 0,
        limit: int | None = None,
    ) -> list[DurableEventEnvelope]:
        if self.backend == "memory":
            backbone = self.memory_backbone
            assert backbone is not None
            return backbone.consume(topic, offset=offset, limit=limit)
        if self.backend == "kafka":
            self.subscribe([topic])
            event = self.poll(timeout=0)
            return [] if event is None else [event]
        raise EventBackboneUnavailableError("Event backbone unavailable")

    def poll(self, timeout: float | None = None) -> DurableEventEnvelope | None:
        if self.backend == "memory":
            if not self._subscriptions:
                return None
            backbone = self.memory_backbone
            assert backbone is not None
            events = backbone.consume(self._subscriptions[0], offset=0, limit=1)
            return events[0] if events else None
        if self.backend == "kafka":
            try:
                message = self.kafka_consumer.poll(timeout if timeout is not None else 0)
                if message is None:
                    return None
                if message.error():
                    raise EventBackboneUnavailableError(
                        f"event-backbone poll failed: {message.error().__class__.__name__}"
                    )
                return durable_event_from_message({"value": message.value()})
            except EventBackboneUnavailableError:
                raise
            except Exception as exc:
                raise EventBackboneUnavailableError(
                    f"event-backbone poll failed: {exc.__class__.__name__}"
                ) from exc
        raise EventBackboneUnavailableError("Event backbone unavailable")

    def close(self) -> None:
        if self._kafka_consumer is not None:
            try:
                self._kafka_consumer.close()
            finally:
                self._kafka_consumer = None

    def __enter__(self) -> EventBackboneConsumer:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

