from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.event_backbone.producer import (
    EventBackboneProducer,
    _bootstrap_looks_invalid,
)
from stark_terminal_data_platform.event_backbone.topics import list_default_topic_names


class EventBackboneHealthStatus(BaseModel):
    configured: bool
    enabled: bool
    reachable: bool
    backend: str
    mode: str
    memory_fallback_enabled: bool
    bootstrap_servers_present: bool
    client_id: str
    schema_version: str
    default_topic_count: int
    error: str | None = None


def check_event_backbone_health(settings: Settings | None = None) -> EventBackboneHealthStatus:
    resolved_settings = settings or get_settings()
    configured = bool(resolved_settings.kafka_bootstrap_servers)
    enabled = resolved_settings.kafka_enabled
    topic_count = len(list_default_topic_names(resolved_settings))

    if enabled and configured:
        if _bootstrap_looks_invalid(resolved_settings.kafka_bootstrap_servers):
            return EventBackboneHealthStatus(
                configured=configured,
                enabled=enabled,
                reachable=False,
                backend="kafka",
                mode=resolved_settings.event_backbone_mode,
                memory_fallback_enabled=resolved_settings.kafka_use_memory_fallback,
                bootstrap_servers_present=configured,
                client_id=resolved_settings.kafka_client_id,
                schema_version=resolved_settings.durable_event_schema_version,
                default_topic_count=topic_count,
                error="InvalidKafkaBootstrapServers",
            )

        producer = EventBackboneProducer(resolved_settings)
        try:
            producer.kafka_producer.list_topics(
                timeout=resolved_settings.kafka_request_timeout_seconds
            )
            return EventBackboneHealthStatus(
                configured=configured,
                enabled=enabled,
                reachable=True,
                backend="kafka",
                mode=resolved_settings.event_backbone_mode,
                memory_fallback_enabled=resolved_settings.kafka_use_memory_fallback,
                bootstrap_servers_present=configured,
                client_id=resolved_settings.kafka_client_id,
                schema_version=resolved_settings.durable_event_schema_version,
                default_topic_count=topic_count,
            )
        except Exception as exc:
            return EventBackboneHealthStatus(
                configured=configured,
                enabled=enabled,
                reachable=False,
                backend="kafka",
                mode=resolved_settings.event_backbone_mode,
                memory_fallback_enabled=resolved_settings.kafka_use_memory_fallback,
                bootstrap_servers_present=configured,
                client_id=resolved_settings.kafka_client_id,
                schema_version=resolved_settings.durable_event_schema_version,
                default_topic_count=topic_count,
                error=exc.__class__.__name__,
            )
        finally:
            producer.close()

    if resolved_settings.kafka_use_memory_fallback:
        return EventBackboneHealthStatus(
            configured=configured,
            enabled=enabled,
            reachable=True,
            backend="memory",
            mode=resolved_settings.event_backbone_mode,
            memory_fallback_enabled=True,
            bootstrap_servers_present=configured,
            client_id=resolved_settings.kafka_client_id,
            schema_version=resolved_settings.durable_event_schema_version,
            default_topic_count=topic_count,
        )

    return EventBackboneHealthStatus(
        configured=configured,
        enabled=enabled,
        reachable=False,
        backend="none",
        mode=resolved_settings.event_backbone_mode,
        memory_fallback_enabled=False,
        bootstrap_servers_present=configured,
        client_id=resolved_settings.kafka_client_id,
        schema_version=resolved_settings.durable_event_schema_version,
        default_topic_count=topic_count,
        error="EventBackboneBackendDisabled",
    )
