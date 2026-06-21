from __future__ import annotations

from stark_terminal_data_platform.event_backbone.envelopes import DurableEventEnvelope
from stark_terminal_data_platform.event_backbone.topics import validate_topic_part


class InMemoryEventBackbone:
    """Local/test event backbone subset. This is not durable storage."""

    def __init__(self) -> None:
        self._topics: dict[str, list[DurableEventEnvelope]] = {}

    def publish(
        self,
        topic: str,
        envelope: DurableEventEnvelope,
        key: str | None = None,
        partition: int | None = None,
    ) -> str:
        for part in topic.split("."):
            validate_topic_part(part)
        stored = envelope.model_copy(
            deep=True,
            update={
                "topic": topic,
                "key": key if key is not None else envelope.key,
                "partition": partition if partition is not None else envelope.partition,
            },
        )
        self._topics.setdefault(topic, []).append(stored)
        return stored.event_id

    def consume(
        self,
        topic: str,
        offset: int = 0,
        limit: int | None = None,
    ) -> list[DurableEventEnvelope]:
        if offset < 0:
            raise ValueError("offset must be non-negative")
        if limit is not None and limit <= 0:
            raise ValueError("limit must be positive")
        events = self._topics.get(topic, [])[offset:]
        if limit is not None:
            events = events[:limit]
        return [event.model_copy(deep=True) for event in events]

    def list_topics(self) -> list[str]:
        return sorted(self._topics)

    def clear(self) -> None:
        self._topics.clear()

    def count(self, topic: str | None = None) -> int:
        if topic is not None:
            return len(self._topics.get(topic, []))
        return sum(len(events) for events in self._topics.values())

