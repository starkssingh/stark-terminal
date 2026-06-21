from __future__ import annotations

from typing import Any

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.streams.events import EventEnvelope, event_from_stream_fields
from stark_terminal_data_platform.streams.memory import InMemoryStreamStore
from stark_terminal_data_platform.streams.producer import StreamUnavailableError


def _decode_entry_id(entry_id: Any) -> str:
    if isinstance(entry_id, bytes | bytearray):
        return bytes(entry_id).decode("utf-8")
    return str(entry_id)


class StreamConsumer:
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

    def _parse_read_result(
        self,
        result: list[tuple[Any, list[tuple[Any, dict[Any, Any]]]]],
    ) -> list[tuple[str, str, EventEnvelope]]:
        parsed: list[tuple[str, str, EventEnvelope]] = []
        for stream_name, entries in result:
            decoded_stream = (
                stream_name.decode("utf-8") if isinstance(stream_name, bytes) else str(stream_name)
            )
            for entry_id, fields in entries:
                parsed.append(
                    (
                        decoded_stream,
                        _decode_entry_id(entry_id),
                        event_from_stream_fields(fields),
                    )
                )
        return parsed

    def read(
        self,
        stream: str,
        count: int | None = None,
        block_ms: int | None = None,
    ) -> list[tuple[str, str, EventEnvelope]]:
        resolved_count = self.settings.stream_read_count if count is None else count
        resolved_block = self.settings.stream_block_ms if block_ms is None else block_ms
        if resolved_count <= 0:
            raise ValueError("count must be positive")
        if resolved_block < 0:
            raise ValueError("block_ms must be non-negative")

        if self.backend == "memory":
            store = self.memory_store
            assert store is not None
            return self._parse_read_result(
                store.xread({stream: "0-0"}, count=resolved_count, block=resolved_block)
            )
        if self.backend == "redis":
            try:
                return self._parse_read_result(
                    self.redis_client.xread(
                        {stream: "0-0"},
                        count=resolved_count,
                        block=resolved_block,
                    )
                )
            except Exception as exc:
                raise StreamUnavailableError(f"stream read failed: {exc.__class__.__name__}") from exc
        raise StreamUnavailableError("Stream backend unavailable")

    def read_group(
        self,
        stream: str,
        group: str | None = None,
        consumer: str | None = None,
        count: int | None = None,
        block_ms: int | None = None,
    ) -> list[tuple[str, str, EventEnvelope]]:
        resolved_group = group or self.settings.stream_consumer_group
        resolved_consumer = consumer or "stark-terminal-consumer"
        resolved_count = self.settings.stream_read_count if count is None else count
        resolved_block = self.settings.stream_block_ms if block_ms is None else block_ms

        if self.backend == "memory":
            store = self.memory_store
            assert store is not None
            return self._parse_read_result(
                store.xreadgroup(
                    resolved_group,
                    resolved_consumer,
                    {stream: ">"},
                    count=resolved_count,
                    block=resolved_block,
                )
            )
        if self.backend == "redis":
            try:
                try:
                    self.redis_client.xgroup_create(stream, resolved_group, id="0-0", mkstream=True)
                except Exception:
                    pass
                return self._parse_read_result(
                    self.redis_client.xreadgroup(
                        resolved_group,
                        resolved_consumer,
                        {stream: ">"},
                        count=resolved_count,
                        block=resolved_block,
                    )
                )
            except Exception as exc:
                raise StreamUnavailableError(
                    f"stream group read failed: {exc.__class__.__name__}"
                ) from exc
        raise StreamUnavailableError("Stream backend unavailable")

    def ack(self, stream: str, group: str, *event_ids: str) -> int:
        if self.backend == "memory":
            store = self.memory_store
            assert store is not None
            return store.xack(stream, group, *event_ids)
        if self.backend == "redis":
            try:
                return int(self.redis_client.xack(stream, group, *event_ids))
            except Exception as exc:
                raise StreamUnavailableError(f"stream ack failed: {exc.__class__.__name__}") from exc
        return 0

    def close(self) -> None:
        if self._redis_client is not None:
            try:
                self._redis_client.close()
            finally:
                self._redis_client = None

    def __enter__(self) -> StreamConsumer:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

