from datetime import datetime, timezone

import pytest

from stark_terminal_core.domain.decision_object import DecisionObject
from stark_terminal_core.domain.enums import ActionState, EventType, MarketSegment, RiskLevel
from stark_terminal_data_platform.streams.serialization import (
    StreamSerializationError,
    stream_dumps,
    stream_loads,
)


def test_stream_serializes_primitives_and_collections() -> None:
    payload = {"count": 1, "items": ["a", "b"], "active": True}

    assert stream_loads(stream_dumps(payload)) == payload


def test_stream_serializes_enums_datetimes_and_pydantic_models() -> None:
    decision = DecisionObject(
        instrument="RELIANCE",
        exchange="NSE",
        segment=MarketSegment.NSE_EQUITY,
        timeframe="DAILY",
        regime=None,
        state=None,
        action_state=ActionState.WATCH,
        confidence=55.0,
        risk=RiskLevel.MEDIUM,
        evidence=[],
        invalidation=None,
        horizon=None,
        source_data_reference=None,
        generated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    restored = stream_loads(stream_dumps({"decision": decision, "event_type": EventType.AUDIT_RECORDED}))

    assert restored["event_type"] == "AUDIT_RECORDED"
    assert restored["decision"]["instrument"] == "RELIANCE"
    assert restored["decision"]["generated_at"] == "2026-01-01T00:00:00+00:00"


def test_stream_rejects_unserializable_objects() -> None:
    with pytest.raises(StreamSerializationError):
        stream_dumps({"bad": object()})


@pytest.mark.parametrize("key", ["password", "secret_value", "api_key", "database_url", "broker_token"])
def test_stream_rejects_secret_like_payload_keys(key: str) -> None:
    with pytest.raises(StreamSerializationError):
        stream_dumps({key: "value"})

