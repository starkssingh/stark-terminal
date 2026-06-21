from datetime import datetime, timezone

import pytest

from stark_terminal_core.domain.enums import EventType
from stark_terminal_data_platform.event_backbone.serialization import (
    EventBackboneSerializationError,
    event_backbone_dumps,
    event_backbone_loads,
)


def test_event_backbone_serializes_primitives_and_collections() -> None:
    payload = {"count": 1, "items": ["a", "b"], "active": True}

    assert event_backbone_loads(event_backbone_dumps(payload)) == payload


def test_event_backbone_serializes_enums_and_datetimes() -> None:
    restored = event_backbone_loads(
        event_backbone_dumps(
            {
                "event_type": EventType.AUDIT_RECORDED,
                "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
            }
        )
    )

    assert restored["event_type"] == "AUDIT_RECORDED"
    assert restored["created_at"] == "2026-01-01T00:00:00+00:00"


def test_event_backbone_rejects_unserializable_objects() -> None:
    with pytest.raises(EventBackboneSerializationError):
        event_backbone_dumps({"bad": object()})


@pytest.mark.parametrize(
    "payload",
    [
        {"password": "secret"},
        {"api_key": "secret"},
        {"kafka_bootstrap_servers": "localhost:9092"},
        {"broker_secret": "secret"},
        {"job": "live_trading"},
    ],
)
def test_event_backbone_rejects_secret_or_execution_like_payloads(payload: dict[str, object]) -> None:
    with pytest.raises(EventBackboneSerializationError):
        event_backbone_dumps(payload)

