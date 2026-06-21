from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.streams.producer import StreamProducer


class StreamsHealthStatus(BaseModel):
    configured: bool
    enabled: bool
    reachable: bool
    backend: str
    memory_fallback_enabled: bool
    redis_url_present: bool
    consumer_group: str
    stream_schema_version: str
    error: str | None = None


def check_streams_health(settings: Settings | None = None) -> StreamsHealthStatus:
    resolved_settings = settings or get_settings()
    configured = bool(resolved_settings.redis_url)
    enabled = resolved_settings.redis_streams_enabled

    if enabled and configured:
        producer = StreamProducer(resolved_settings)
        try:
            reachable = bool(producer.redis_client.ping())
            return StreamsHealthStatus(
                configured=configured,
                enabled=enabled,
                reachable=reachable,
                backend="redis",
                memory_fallback_enabled=resolved_settings.redis_streams_use_memory_fallback,
                redis_url_present=configured,
                consumer_group=resolved_settings.stream_consumer_group,
                stream_schema_version=resolved_settings.event_schema_version,
                error=None if reachable else "RedisPingFailed",
            )
        except Exception as exc:
            return StreamsHealthStatus(
                configured=configured,
                enabled=enabled,
                reachable=False,
                backend="redis",
                memory_fallback_enabled=resolved_settings.redis_streams_use_memory_fallback,
                redis_url_present=configured,
                consumer_group=resolved_settings.stream_consumer_group,
                stream_schema_version=resolved_settings.event_schema_version,
                error=exc.__class__.__name__,
            )
        finally:
            producer.close()

    if resolved_settings.redis_streams_use_memory_fallback:
        return StreamsHealthStatus(
            configured=configured,
            enabled=enabled,
            reachable=True,
            backend="memory",
            memory_fallback_enabled=True,
            redis_url_present=configured,
            consumer_group=resolved_settings.stream_consumer_group,
            stream_schema_version=resolved_settings.event_schema_version,
        )

    return StreamsHealthStatus(
        configured=configured,
        enabled=enabled,
        reachable=False,
        backend="none",
        memory_fallback_enabled=False,
        redis_url_present=configured,
        consumer_group=resolved_settings.stream_consumer_group,
        stream_schema_version=resolved_settings.event_schema_version,
        error="StreamsBackendDisabled",
    )

