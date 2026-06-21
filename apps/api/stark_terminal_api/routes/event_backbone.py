from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_data_platform.event_backbone.health import check_event_backbone_health
from stark_terminal_data_platform.event_backbone.topics import list_default_topic_names

router = APIRouter()


@router.get("/event-backbone/health")
def event_backbone_health() -> dict[str, Any]:
    status = check_event_backbone_health()
    return {
        "service": "stark-terminal-event-backbone",
        **status.model_dump(),
    }


@router.get("/event-backbone/topics")
def event_backbone_topics() -> dict[str, Any]:
    settings = get_settings()
    topics = list_default_topic_names(settings)
    return {
        "service": "stark-terminal-event-backbone",
        "mode": settings.event_backbone_mode,
        "schema_version": settings.durable_event_schema_version,
        "topics": topics,
        "count": len(topics),
    }
