from __future__ import annotations

from typing import Any

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import EventPriority, EventSource, EventType, StreamNamespace
from stark_terminal_data_platform.streams.events import (
    EventEnvelope,
    create_event_envelope,
    event_to_stream_fields,
)
from stark_terminal_data_platform.streams.memory import InMemoryStreamStore
from stark_terminal_data_platform.streams.names import build_stream_name


class StreamError(RuntimeError):
    """Base stream error."""


class StreamUnavailableError(StreamError):
    """Raised when no stream backend is available for a required operation."""


class StreamProducer:
    def __init__(
        self,
        settings: Settings | None = None,
        memory_store: InMemoryStreamStore | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self._memory_store = memory_store
        self._redis_client: Any | None = None

    @property
    def backend(self) -> str:
        if self.settings.redis_streams_enabled and self.settings.redis_url:
            return "redis"
        if self.settings.redis_streams_use_memory_fallback:
            return "memory"
        return "none"

    @property
    def memory_store(self) -> InMemoryStreamStore | None:
        if self.backend != "memory":
            return None
        if self._memory_store is None:
            self._memory_store = InMemoryStreamStore()
        return self._memory_store

    @property
    def redis_client(self) -> Any:
        if self.backend != "redis":
            raise StreamUnavailableError("Redis Streams backend is not configured")
        if self._redis_client is None:
            try:
                import redis

                self._redis_client = redis.Redis.from_url(
                    self.settings.redis_url or "",
                    socket_timeout=self.settings.redis_socket_timeout_seconds,
                    socket_connect_timeout=self.settings.redis_connect_timeout_seconds,
                    health_check_interval=self.settings.redis_health_check_interval_seconds,
                    decode_responses=False,
                )
            except Exception as exc:
                raise StreamUnavailableError(
                    f"Redis Streams backend unavailable: {exc.__class__.__name__}"
                ) from exc
        return self._redis_client

    def publish(self, envelope: EventEnvelope, max_len: int | None = None) -> str:
        fields = event_to_stream_fields(envelope)
        resolved_max_len = self.settings.stream_max_len if max_len is None else max_len
        if resolved_max_len <= 0:
            raise ValueError("max_len must be positive")

        if self.backend == "memory":
            store = self.memory_store
            assert store is not None
            return store.xadd(
                envelope.stream,
                fields,
                maxlen=resolved_max_len,
                approximate=self.settings.stream_approximate_trim,
            )
        if self.backend == "redis":
            try:
                result = self.redis_client.xadd(
                    envelope.stream,
                    fields,
                    maxlen=resolved_max_len,
                    approximate=self.settings.stream_approximate_trim,
                )
                return result.decode("utf-8") if isinstance(result, bytes) else str(result)
            except Exception as exc:
                raise StreamUnavailableError(
                    f"stream publish failed: {exc.__class__.__name__}"
                ) from exc
        raise StreamUnavailableError("Stream backend unavailable")

    def publish_event(
        self,
        event_type: EventType,
        source: EventSource,
        namespace: StreamNamespace | str,
        payload: dict[str, object],
        priority: EventPriority = EventPriority.NORMAL,
        correlation_id: str | None = None,
        causation_id: str | None = None,
        audit_id: str | None = None,
    ) -> str:
        stream = build_stream_name(namespace, settings=self.settings)
        envelope = create_event_envelope(
            event_type=event_type,
            source=source,
            stream=stream,
            payload=payload,
            settings=self.settings,
            priority=priority,
            correlation_id=correlation_id,
            causation_id=causation_id,
            audit_id=audit_id,
        )
        return self.publish(envelope)

    def close(self) -> None:
        if self._redis_client is not None:
            try:
                self._redis_client.close()
            finally:
                self._redis_client = None

    def __enter__(self) -> StreamProducer:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

